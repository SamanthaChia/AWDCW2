from django.contrib import admin

from .models import *

# Register your models here.
class FriendsListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']
    
    class Meta:
        model = FriendsList

admin.site.register(FriendsList, FriendsListAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']
    # sender is a account object, so have to indicate what to search from the object
    search_fields = ['sender__username', 'sender__email', 'receiver__username', 'receiver__email']

    class Meta:
        model = FriendRequest

admin.site.register(FriendRequest, FriendRequestAdmin)