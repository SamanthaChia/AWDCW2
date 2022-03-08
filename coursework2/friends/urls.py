from django.urls import path
from . import views

app_name = "friends"

urlpatterns = [
    path('friend_request/', views.send_friend_request, name="friend-request"),
    path('friend_request/<user_id>', views.friend_requests, name="friend-requests"),
]