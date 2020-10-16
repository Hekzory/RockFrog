from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import *
from django.utils.html import strip_tags
from django.core.exceptions import ObjectDoesNotExist
import datetime
from notifications import models as notifications
from channels.layers import get_channel_layer


class PMConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            user_talking_with_id = self.scope["url_route"]["kwargs"]["user_id"]
            user_talking_with = User.objects.get(pk=user_talking_with_id)
            self.dialog_id = self.user.dialog_list.dialogs.get(user=user_talking_with).id
            self.username = self.user.username
            self.room_group_name = "personal_messages_" + str(self.username) + "_" + str(self.dialog_id)

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            if self.dialog_id is not None:
                self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = strip_tags(text_data_json['type'])
        if type == "message":
            message = strip_tags(text_data_json['message'])
            user = self.user
            user_messaging_with_id = int(text_data_json['user_messaging_with_id'])
            user_messaging_with = User.objects.get(pk=user_messaging_with_id)
            # Проверка на нахождение в чёрном списке
            user_blacklist = user.profile.blacklist
            viewed_user_blacklist = user_messaging_with.profile.blacklist
            if viewed_user_blacklist.filter(pk=user.pk).exists() or user_blacklist.filter(
                    pk=user_messaging_with.pk).exists():
                return None
            # Последние проверки сообщения
            if message is not None and message.strip() != "":
                # Создаем сообщение и кладём в переписку
                new_message = DialogMessage(user=user, text=message,
                                                               date_time=datetime.datetime.now())
                new_message.save()
                add_message_to_dialog(user, user_messaging_with, new_message)
                #  Создаём уведомление о сообщении, если пользователь хочет получать уведомления
                if user_messaging_with.profile.notificationsettings.personal_message_notifications:
                    notifications.create_notification_on_pm(user, user_messaging_with)
                # Обновляем список диалогов обоим пользователям, создавая событие в WebSocket'ах
                channel_layer_temp = get_channel_layer()
                async_to_sync(channel_layer_temp.group_send)("dialog_list_" + user.username, {"type": "update_dialogs"})
                async_to_sync(channel_layer_temp.group_send)("dialog_list_" + user_messaging_with.username,
                                                             {"type": "update_dialogs"})
                # Отправляем событие создания сообщения
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'pm_message',
                        'message': message,
                        'message_id': new_message.id,
                        'username': str(new_message.user.username),
                        'datetime': str(new_message.date_time.strftime('%d.%m.%Y %H:%M')),
                        'avatar_url': new_message.user.profile.get_avatar_url()
                    }
                )
        elif type == "delete":
            id = text_data_json['id']
            user_messaging_with = text_data_json['user_messaging_with']
            try:
                message = DialogMessage.objects.get(id=id)
            except ConversationMessage.DoesNotExist:
                message = "ok"
            if message == "ok":
                # Обновляем список диалогов обоим пользователям, создавая событие в WebSocket'ах
                channel_layer_temp = get_channel_layer()
                async_to_sync(channel_layer_temp.group_send)("dialog_list_" + self.user.username,
                                                             {"type": "update_dialogs"})
                async_to_sync(channel_layer_temp.group_send)("dialog_list_" + user_messaging_with,
                                                             {"type": "update_dialogs"})
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'delete_message',
                        'message_id': id,
                    }
                )
        elif type == "edit":
            id = text_data_json['id']
            user_messaging_with = text_data_json['user_messaging_with']
            try:
                message = DialogMessage.objects.get(id=id)
            except ConversationMessage.DoesNotExist:
                message = "error"
            if message != "error" and self.user.id == message.user.id and message.is_earlier_24():
                # Обновляем список диалогов обоим пользователям, создавая событие в WebSocket'ах
                channel_layer_temp = get_channel_layer()
                async_to_sync(channel_layer_temp.group_send)("dialog_list_" + self.user.username,
                                                             {"type": "update_dialogs"})
                async_to_sync(channel_layer_temp.group_send)("dialog_list_" + user_messaging_with,
                                                             {"type": "update_dialogs"})
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'edit_message',
                        'message_id': id,
                    }
                )

    def pm_message(self, event):
        type = "message"
        message = event['message']
        username = event['username']
        datetime = event['datetime']
        id = event['message_id']
        avatar_url = event['avatar_url']
        self.send(text_data=json.dumps({
            'type': type,
            'message': message,
            'username': username,
            'datetime': datetime,
            'message_id': id,
            'avatar_url': avatar_url,
        }))

    def delete_message(self, event):
        type = "delete"
        id = event['message_id']
        self.send(text_data=json.dumps({
            'type': type,
            'message_id': id,
        }))

    def edit_message(self, event):
        type = "edit"
        id = event['message_id']
        message = ConversationMessage.objects.get(id=id)
        self.send(text_data=json.dumps({
            'type': type,
            'message_id': id,
            'message': message.text,
        }))


class DialogListConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.username = self.user.username
            self.room_group_name = "dialog_list_" + self.username

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        pass

    def update_dialogs(self, event):
        self.send(text_data=json.dumps({
            'list': True,
        }))
