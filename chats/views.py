from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Chat, Message


@login_required
def chats_view(request):
    if request.method == 'GET':
        chats = Chat.objects.filter(Q(sender_id=request.user.id) | Q(recipient_id=request.user.id))
        return render(request, "chats/chats.html", {'chats': chats})


@login_required
def chat_view(request, recipient_id):
    if request.method == 'GET':
        try:
            chat = Chat.get_or_create_chat(request.user.id, recipient_id)
        except IntegrityError:
            return redirect('all-posts')
        if chat.is_user_in_chat(request.user.id):
            messages = Message.objects.filter(chat=chat)
            context = {
                'chat_id': chat.id,
                'messages': messages
            }
            return render(request, "chats/chat.html", context)
        return redirect('all-posts')
