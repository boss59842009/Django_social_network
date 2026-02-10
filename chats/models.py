from django.db import models
from django.conf import settings


class ChatParticipant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_participations', verbose_name='Користувач')
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='chat_participants', verbose_name='Чат')
    is_admin = models.BooleanField(default=False, verbose_name='Адміністратор')

class Chat(models.Model):
    is_group = models.BooleanField(default=False, verbose_name='Груповий чат')
    title = models.CharField(max_length=100, blank=True, verbose_name='Назва')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ChatParticipant', related_name='chats', verbose_name='Учасники')

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages', verbose_name='Чат')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Відправник', related_name='messages')
    text = models.TextField(max_length=1024, verbose_name='Текст')
    media = models.FileField(upload_to='chat/media', blank=True, null=True, verbose_name='Медіа')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата відправлення')
    read_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата прочитання')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f'Повідомлення від {self.sender.username} в чаті {self.chat.id}'

