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

    def get_or_create_chat(self, user1, user2):
        chat = self.objects.filter(
            (Q(sender=user1) & Q(recipient=user2)) | (Q(sender=user2) & Q(recipient=user1))
        ).first()
        if chat:
            return chat

        chat = self.objects.create(sender=user1, recipient=user2)
        return chat

    def is_user_in_chat(self, user):
        return self.sender == user or self.recipient == user


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

