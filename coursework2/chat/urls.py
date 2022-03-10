from django.urls import path
from . import views

urlpatterns = [
    path('chat/index', views.index, name='chat-index'),
    path('chat/<str:room_name>/', views.room , name='chat-room'),
]