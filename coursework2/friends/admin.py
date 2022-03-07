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