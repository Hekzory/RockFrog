# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.username = self.user.username
            self.room_group_name = "notifications_"+self.username
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()

    def disconnect(self, close_code):
        if self.user.is_authenticated and self.room_group_name is not None:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

    def receive(self, text_data):
        pass

    def notification(self, event):
        message = event['message']
        header = event['header']
        href = event['href']
        self.send(text_data=json.dumps({
            'message': message,
            'href': href,
            'header': header
        }))
