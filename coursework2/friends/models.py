from django.db import models
from django.conf import settings

# Create your models here.
class FriendsList(models.Model):
    # the user id
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

    def unfriend(self, account):
        user_friend_list = self
        user_friend_list.remove_friend(account)
        friends_list = FriendList.objects.get(user=account)
        friends_list.remove_friend(self.user)

    