from enum import Enum
from .models import *

def get_friend_request(sender, receiver):
    try:
        return FriendRequest.objects.get(sender=sender, receiver=receiver, pending_request_status=True)
    except FriendRequest.DoesNotExist:
        return False

class FriendRequestStatus(Enum):
    no_request = 0
    user_sent = 1
    friend_sent = 2