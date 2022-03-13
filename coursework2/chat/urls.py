from django.urls import path
from .views import *

app_name = "chat"

urlpatterns = [
    path('<user_id>/', index_view, name='chat-index'),
    path('chatroom/<str:room_name>/', room_view , name='chat-room'),
]