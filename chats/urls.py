from django.urls import path

from . import views


urlpatterns = [
    path("chats/", views.index, name="index"),
    path("chat/<int:chat_id>/", views.room, name="room"),
]
