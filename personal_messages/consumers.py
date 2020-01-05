from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import *
from django.utils.html import strip_tags
from django.core.exceptions import ObjectDoesNotExist
import datetime
from notifications import models as notifications

class PMConsumer(WebsocketConsumer):
    def connect(self):
        user_talking_with_id = self.scope["url_route"]["kwargs"]["user_id"]
        user_talking_with = User.objects.get(pk=user_talking_with_id)
        self.user = self.scope["user"]
        self.conversation_id = get_conversation_id_and_create_if_not(self.user, user_talking_with)
        self.username = self.user.username
        self.room_group_name = "personal_messages_"+str(self.conversation_id)

        print(self.user.username+" connected in PM's")

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

        message = strip_tags(text_data_json['message'])
        user = self.user
        user_messaging_with_id = int(strip_tags(text_data_json['user_messaging_with_id']))
        user_messaging_with = None
        new_conversation_message = None

        if message is not None:
            if message != '':
                if user.is_authenticated:
                    try:
                        user_messaging_with = User.objects.get(pk=user_messaging_with_id)
                    except:
                        pass
                    if user_messaging_with is not None:
                        current_conversation = None
                        for conversation in user.conversationlist.conversations.all():
                            if conversation.user1.id == user_messaging_with.id or conversation.user2.id == user_messaging_with.id:
                                current_conversation = conversation
                        new_conversation_message = ConversationMessage(user=user, text=message, date_time=datetime.datetime.now())
                        new_conversation_message.save()
                        if current_conversation == None:
                            new_conversation = Conversation(user1=user, user2=user_messaging_with)
                            new_conversation.save()
                            new_conversation.messages.add(new_conversation_message)
                            new_conversation.save()
                            user.conversationlist.conversations.add(new_conversation)
                            user_messaging_with.conversationlist.conversations.add(new_conversation)
                            current_conversation = new_conversation
                        else:
                            current_conversation.messages.add(new_conversation_message)
        if user_messaging_with is not None:
            notifications.create_notification_on_pm(user, user_messaging_with)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'pm_message',
                    'message': message,
                    'username': str(new_conversation_message.user.username),
                    'datetime': str(new_conversation_message.date_time.strftime('%d.%m.%Y %H:%M'))
                }
            )

    def pm_message(self, event):
        message = event['message']
        username = event['username']
        datetime = event['datetime']
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'datetime': datetime
        }))