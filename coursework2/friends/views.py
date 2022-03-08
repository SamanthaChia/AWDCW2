from ast import Try
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from accounts.models import *

import json
# Create your views here.

def send_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = Account.objects.get(pk=user_id)
            try:
                # retrieve all the friend requests
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
                try:
                    for request in friend_requests:
                        if request.pending_request_status:
                            raise Exception("Friend request already sent.")
                    friend_requests = FriendRequest(sender=user, receiver=receiver)
                    friend_requests.save()
                    payload['response'] = "Sent friend request"
                except Exception as e:
                    payload['response'] = str(e)
            # determines that friend request object doesnt exist 
            except FriendRequest.DoesNotExist:
                friend_requests = FriendRequest(sender=user, receiver=receiver)
                friend_requests.save()
                payload['response'] = "Sent friend request"
            
            if payload['response'] == None:
                payload['response'] = "Issue"
        else:
            payload['response'] = "Unable to send request, receiver does not have a user id"
    else:
        payload['response'] = "Unable to send request, user is not authenticated"
    
    return HttpResponse(json.dumps(payload), content_type="application/json")