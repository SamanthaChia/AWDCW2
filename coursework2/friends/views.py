from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from accounts.models import *

import json

def friend_requests(request, *aregs, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        #retrieve from url
        user_id = kwargs.get("user_id")
        account = Account.objects.get(pk=user_id)
        if account == user:
            friend_requests = FriendRequest.objects.filter(receiver=account, pending_request_status=True)
            context['friend_requests'] = friend_requests
        else:
            return HttpResponse("You are only allowed to see your own friend requests")
    else:
        redirect("login")
    return render(request, "friends/friend_requests.html", context)

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

def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user:
                if friend_request:
                    friend_request.accept_friend_request()
                    payload['results'] = "success"
                    payload['response'] = "Friend Request has been accepted"
                else:
                    payload['results'] = "error"
                    payload['response'] = "Could not find friend request"
        else:
            payload['results'] = "error"
            payload['response'] = " Not able to accept friend request because its not yours"
    else:
        payload['results'] = "error"
        payload['response'] = "Must be authenticated to accept friend request"
    return HttpResponse(json.dumps(payload), content_type="application/json")            

def remove_friend(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            try:
                user_getting_removed = Account.objects.get(pk=user_id)
                # user requesting for remove's friend list
                friend_list = FriendsList.objects.get(user=user)
                friend_list.unfriend(user_getting_removed)
                payload['results'] = "success"
                payload['response'] = "Removed friend"
            except Exception as e:
                payload['results'] = "error"
                payload['response'] = "Issue"
        else:
            payload['results'] = "error"
            payload['response'] = "Unable to remove friend"
    else:
        payload['results'] = "error"
        payload['response'] = "Must be authenticated first"
    return HttpResponse(json.dumps(payload), content_type="application/json")            

def decline_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user:
                if friend_request:
                    friend_request.decline_friend_request()
                    payload['results'] = "success"
                    payload['response'] = "Friend Request has been declined"
                else:
                    payload['results'] = "error"
                    payload['response'] = "Could not find friend request"
        else:
            payload['results'] = "error"
            payload['response'] = " Not able to decline friend request because it is not yours"
    else:
        payload['results'] = "error"
        payload['response'] = "Must be authenticated to decline friend request"
    return HttpResponse(json.dumps(payload), content_type="application/json")  

def cancel_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            user_getting_removed = FriendRequest.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=user_getting_removed, pending_request_status=True)
            except Exception as e:
                payload['response'] = "Friend request doesn't exist. Can't cancel"

            if len(friend_requests) > 1:
                for request in friend_requests:
                    request.cancel_friend_request()
                payload['results'] = "success"
                payload['response'] = "Cancelled friend request"
            else:
                friend_requests.first().cancel_friend_request()
                payload['results'] = "success"
                payload['response'] = "Cancelled friend request"
        else:
            payload['results'] = "error"
            payload['response'] = "Can't cancel friend request"
    else:
        payload['results'] = "error"
        payload['response'] = "Must be authenticated to cancel friend request"
            
    return HttpResponse(json.dumps(payload), content_type="application/json")  