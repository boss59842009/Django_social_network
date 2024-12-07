from django.urls import path

from . import views


urlpatterns = [
    path("chats/", views.chats_view, name="chats"),
    path("chat/<int:recipient_id>", views.chat_view, name="chat"),
]
