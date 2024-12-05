import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

from chats import models


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        chat = models.Chat.objects.get(id=self.chat_id)
        if not chat.is_user_in_chat(user):
            self.close()
        else:
            self.room_group_name = f"chat_{self.chat_id}"
            async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
