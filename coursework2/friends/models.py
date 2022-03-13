from django.db import models
from django.conf import settings

# Create your models here.
class FriendsList(models.Model):
    # 1 user can only have 1 friend list
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    # list of friends, contain pk of friends
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friendsList")

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        # check if friend is not in friends list
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()
    
    def remove_friend(self, account):
        # check if friend is in friends list
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()

    # action to remove friend
    def unfriend(self, account):
        user_friend_list = self
        # remove friend from initiator friend list
        user_friend_list.remove_friend(account)
        friends_list = FriendsList.objects.get(user=account)
        # remove initiator from friends' friend list
        friends_list.remove_friend(self.user)

    def check_mutual_friends(self, friend):
        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    # 1 user can send many friend requests
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "sender")
    # 1 user can have receive many friend requests
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "receiver")
    # is friend request status still active
    pending_request_status = models.BooleanField(blank=True, null=False, default=True)

    def __str__(self):
        return self.sender.username

    def accept_friend_request(self):
        #get receiver friend list
        receiver_friend_list = FriendsList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            # get sender friend list
            sender_friend_list = FriendsList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.pending_request_status = False
                self.save()

    def decline_friend_request(self):
        # change the request status 
        self.pending_request_status = False
        self.save()
    
    def cancel_friend_request(self):
        self.pending_request_status = False
        self.save()