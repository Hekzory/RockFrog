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
            self.user = self.scope["user"]
            self.conversation_id = get_conversation_and_create_if_not(self.user, user_talking_with).pk
            self.username = self.user.username
            self.room_group_name = "personal_messages_"+str(self.conversation_id)

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
        text_data_json = json.loads(text_data)
        type = strip_tags(text_data_json['type'])
        if type == "message":
            message = strip_tags(text_data_json['message'])
            user = self.user
            user_messaging_with_id = int(strip_tags(text_data_json['user_messaging_with_id']))
            user_messaging_with = None
            try:
                user_messaging_with = User.objects.get(pk=user_messaging_with_id)
            except:
                pass
            # Проверка на нахождение в чёрном списке
            check = True
            user_blacklist = user.profile.blacklist
            viewed_user_blacklist = user_messaging_with.profile.blacklist
            if viewed_user_blacklist.filter(pk=user.pk).exists() or user_blacklist.filter(pk=user_messaging_with.pk).exists():
                check = False
            # Последние проверки на само сообщение и авторизацию
            if message is not None and message.strip() != "" and check:
                if user.is_authenticated and user_messaging_with is not None:
                    # Создаем сообщение и кладём в переписку
                    new_conversation_message = ConversationMessage(user=user, text=message, date_time=datetime.datetime.now())
                    new_conversation_message.save()
                    current_conversation = get_conversation_and_create_if_not(user, user_messaging_with)
                    current_conversation.messages.add(new_conversation_message)
                    current_conversation.save()
                    current_conversation.update_interaction()
                    # Если пользователь отправил сообщение, считаем, что он просмотрел предыдущие.
                    # Выбираем нужного пользователя и обновляем время последнего прочтения
                    if current_conversation.user1.username == user.username:
                        current_conversation.update_last_view_user1()
                    else:
                        current_conversation.update_last_view_user2()
                    #  Создаём уведомление о сообщении
                    notifications.create_notification_on_pm(user, user_messaging_with)
                    # Обновляем список диалогов обоим пользователям, создавая событие в WebSocket'ах
                    channel_layer_temp = get_channel_layer()
                    async_to_sync(channel_layer_temp.group_send)("dialog_list_" + user.username, {"type": "update_dialogs"})
                    async_to_sync(channel_layer_temp.group_send)("dialog_list_" + user_messaging_with.username, {"type": "update_dialogs"})
                    # Отправляем событие создания сообщения
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'pm_message',
                            'message': message,
                            'message_id': new_conversation_message.id,
                            'username': str(new_conversation_message.user.username),
                            'datetime': str(new_conversation_message.date_time.strftime('%d.%m.%Y %H:%M'))
                        }
                    )
        elif type == "delete":
            id = text_data_json['id']
            user_messaging_with = text_data_json['user_messaging_with']
            try:
                message = ConversationMessage.objects.get(id=id)
            except ConversationMessage.DoesNotExist:
                message = "ok"
            if message == "ok" and self.user.is_authenticated:
                # Обновляем список диалогов обоим пользователям, создавая событие в WebSocket'ах
                channel_layer_temp = get_channel_layer()
                async_to_sync(channel_layer_temp.group_send)("dialog_list_" + self.user.username, {"type": "update_dialogs"})
                async_to_sync(channel_layer_temp.group_send)("dialog_list_" + user_messaging_with, {"type": "update_dialogs"})
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
                message = ConversationMessage.objects.get(id=id)
            except ConversationMessage.DoesNotExist:
                message = "error"
            if message != "error" and self.user.is_authenticated and self.user.id == message.user.id and message.is_earlier_24():
                # Обновляем список диалогов обоим пользователям, создавая событие в WebSocket'ах
                channel_layer_temp = get_channel_layer()
                async_to_sync(channel_layer_temp.group_send)("dialog_list_" + self.user.username, {"type": "update_dialogs"})
                async_to_sync(channel_layer_temp.group_send)("dialog_list_" + user_messaging_with, {"type": "update_dialogs"})
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
        self.send(text_data=json.dumps({
            'type': type,
            'message': message,
            'username': username,
            'datetime': datetime,
            'message_id': id
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
            'message' : message.text,
        }))



class DialogListConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.username = self.user.username
            self.room_group_name = "dialog_list_"+self.username

            print(self.user.username+" connected in dialog list")

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
        conv_list = self.user.conversationlist.conversations.all().order_by('last_interaction')[::-1]
        self.send(text_data=json.dumps({
            'list': True,
        }))