from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('chatroom/', views.index, name='chat-index'),
    path('chatroom/<str:room_name>/', views.room , name='chat-room'),
]