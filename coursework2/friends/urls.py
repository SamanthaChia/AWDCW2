from django.urls import path
from .views import *

app_name = "friends"

urlpatterns = [
    path('friend_request/', send_friend_request, name="friend-request"),
    path('friend_request/<user_id>', friend_requests, name="friend-requests"),
    path('accept_friend_request/<friend_request_id>', accept_friend_request, name="friend-request-accept"), 
    path('remove_friend/', remove_friend, name="remove-friend"),
    path('decline_friend_request/<friend_request_id>', decline_friend_request, name="friend-request-decline"), 
    path('cancel_friend_request/', cancel_friend_request, name="friend-request-cancel"),    
    path('friends_list/<user_id>', friends_list, name="friends-list"),    

]