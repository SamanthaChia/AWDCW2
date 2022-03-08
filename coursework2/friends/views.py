from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from accounts.models import *

import json

def friend_requests_view(request, *aregs, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        #retrieve from url
        user_id = kwargs.get("user_id")
        account = Account.objects.get(pk=user_id)
        if account == user:
            friend_requests = FriendRequest.objects.filter(receiver=account, is_active=True)
            context['friend_requests'] = friend_requests
        else:
            return HttpResponse("You are only allowed to see your own friend requests")
    else:
        redirect("login")
    return render(request, "friends/friend_request.html", context)

def send_friend_request_view(request, *args, **kwargs):
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
                    payload['results'] = "success"
                    payload['response'] = "Sent friend request"
                except Exception as e:
                    payload['results'] = "error"
                    payload['response'] = str(e)
            # determines that friend request object doesnt exist 
            except FriendRequest.DoesNotExist:
                friend_requests = FriendRequest(sender=user, receiver=receiver)
                friend_requests.save()
                payload['results'] = "success"
                payload['response'] = "Sent friend request"
            
            if payload['response'] == None:
                payload['results'] = "error"
                payload['response'] = "Issue"
        else:
            payload['results'] = "error"
            payload['response'] = "Unable to send request, receiver does not have a user id"
    else:
        payload['results'] = "error"
        payload['response'] = "Unable to send request, user is not authenticated"
    
    return HttpResponse(json.dumps(payload), content_type="application/json")