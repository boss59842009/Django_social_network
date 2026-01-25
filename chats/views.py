from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect

from .models import Chat, Message


@login_required
def chats_view(request, chat_id=None):
    if request.method == 'GET':
        context = {}
        recipients = []
        chats = Chat.objects.filter(Q(sender_id=request.user.id) | Q(recipient_id=request.user.id))
        for chat in chats:
            if chat.sender == request.user:
                recipients.append({
                    'chat_id': chat.id,
                    'chat_recipient': chat.recipient,
                })
            else:
                recipients.append({
                    'chat_id': chat.id,
                    'chat_recipient': chat.sender
                })
            context.update({"recipients": recipients})
        if chat_id:
            try:
                chat = Chat.objects.filter(
                    (Q(sender_id=request.user.id) | Q(recipient_id=request.user.id)) & (Q(id=chat_id))).first()
                messages = Message.objects.filter(chat=chat)[:5]
                messages_data = []
                for message in messages:
                    sender_avatar_url = message.sender.userprofile.avatar.url if message.sender.userprofile.avatar.url \
                        else None
                    message_media_url = message.media if message.media else None
                    messages_data.append({
                        'sender': {
                            'first_name': message.sender.first_name,
                            'last_name': message.sender.last_name,
                            'avatar': sender_avatar_url,
                        },
                        'text': message.text,
                        'media': message_media_url,
                        'sent_at': message.sent_at,
                        'read_at': message.read_at
                    })
                print(messages_data)
                context.update({
                    'messages': messages_data,
                    'chat': chat
                })

            except IntegrityError:
                return redirect('chats')

        return render(request, "chats/chat_new.html", context)


@login_required
def chat_view(request, recipient_id):
    if request.method == 'GET':
        if not recipient_id == request.user.id:
            chats = Chat.objects.filter(Q(sender_id=request.user.id) | Q(recipient_id=request.user.id))
            try:
                chat = Chat.get_or_create_chat(request.user.id, recipient_id)
            except IntegrityError:
                return redirect('chats')
            if chat.is_user_in_chat(request.user.id):
                messages = Message.objects.filter(chat=chat)[:5]
                context = {
                    'chats': chats,
                    'chat_id': chat.id,
                    'messages': messages,
                    'sender_id': request.user.id,
                }
                print(context)
                return render(request, "chats/chat_new.html", context)
        return redirect('chats')
    else:
        return redirect('chat', recipient_id)