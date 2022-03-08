from django.urls import path
from . import views

app_name = "friends"

urlpatterns = [
    path('friend_request/', views.send_friend_request, name="friend-request"),
    path('friend_request/<user_id>', views.friend_requests, name="friend-requests"),
    path('accept_friend_request/<friend_request_id>', views.accept_friend_request, name="friend-request-accept"), 
    path('remove_friend/', views.remove_friend, name="remove-friend"),
]