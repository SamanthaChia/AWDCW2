from django.db import models
from django.conf import settings

# Create your models here.
class FriendsList(models.Model):
    # the user id
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    # list of friends, contain pk of friends
    friendsList = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friendsList")

    def __str__(self):
        return self.user.username


