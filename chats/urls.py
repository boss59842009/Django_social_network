from django.urls import path

from . import views


urlpatterns = [
    path("chats/", views.chats_view, name="chats_list"),
    path("chat/<int:chat_id>", views.chats_view, name="chat_detail"),
    # path("chat/<int:recipient_id>", views.chat_view, name="chat"),
]
