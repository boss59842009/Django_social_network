import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

from chats import models


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat_name = f"chat_{self.chat_id}"

        async_to_sync(self.channel_layer.group_add)(self.chat_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        if hasattr(self, 'chat_name'):
            async_to_sync(self.channel_layer.group_discard)(self.chat_name, self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.chat_name, {"type": "chat.message", "message": message}
        )

    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
