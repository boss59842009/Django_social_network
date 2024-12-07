from django.db import models
from django.conf import settings
from django.db.models import Q


class Chat(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats_invited')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'recipient')
        ordering = ['-created_at']

    def __str__(self):
        return f'Chat between {self.sender.username} and {self.recipient.username}'

    @classmethod
    def get_or_create_chat(cls, user1_id, user2_id):
        chat = cls.objects.filter(
                (Q(sender_id=user1_id) & Q(recipient_id=user2_id)) | (Q(sender_id=user2_id) & Q(recipient_id=user1_id))
            ).first()
        if chat:
            return chat

        chat = cls.objects.create(sender_id=user1_id, recipient_id=user2_id)
        return chat

    def is_user_in_chat(self, user_id):
        return self.sender.id == user_id or self.recipient.id == user_id


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=1024)
    media = models.FileField(upload_to='chat/media', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f'Message from {self.sender.username} in chat {self.chat.id}'

