from django.shortcuts import render


def index(request):
    return render(request, "chats/index.html")


def room(request, chat_id):
    return render(request, "chats/chat.html", {"chat_id": chat_id})
