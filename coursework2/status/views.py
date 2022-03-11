from email.errors import StartBoundaryNotFoundDefect
from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.db.models import Q

from .models import *
from .forms import *
from accounts.models import *
from friends.models import *

# Create your views here.
def timeline(request, *args, **kwargs):
    context={}
    all_statuses_list = []

    user = request.user
    if user.is_authenticated:

        if request.method == 'POST':
            update_status_form = StatusForm(request.POST, request.FILES)
            if update_status_form.is_valid():
                status = update_status_form.save(commit=False)
                status.author = request.user
                status.save()
                return redirect("status:timeline")

        account = Account.objects.get(pk=user.id)
        context['account'] = account
        try:
            # retrieve the friend list
            friends_list = FriendsList.objects.get(user=account)
        except FriendsList.DoesNotExist:
            #if friend list does not exist create one
            friends_list = FriendsList(user=account)
            friends_list.save()
        # retrieve all friends of the user
        friends = friends_list.friends.all()
        context['friends'] = friends
        if friends:
            for friend in friends:
                account_statuses = StatusList.objects.filter(Q(author=friend.id) | Q(author=account.id)).order_by("-created_at")
                all_statuses_list.append(account_statuses)
        else:
            account_statuses = StatusList.objects.filter(author=account.id).order_by("-created_at")
            all_statuses_list.append(account_statuses)

        update_status_form = StatusForm()
        context['update_status_form'] = update_status_form
        context['all_statuses_list'] = all_statuses_list

    return render(request, 'status/home_timeline.html', context)


def status_profile(request, *args, **kwargs):
    context = {}
    is_self = True
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        if user_id != None:
            # retrieve user that i'm looking at
            try:
                account = Account.objects.get(pk=user_id)
                context['account'] = account
                if user != account:
                    is_self = False

            except Account.DoesNotExist:
                return HttpResponse("User doesn't exist")

            try:
                # newest to oldest
                account_statuses_list = StatusList.objects.filter(author=user_id).order_by("-created_at")
            except StatusList.DoesNotExist:
                return HttpResponse("Statuses do not exist")

        if request.method == 'POST':
            update_status_form = StatusForm(request.POST, request.FILES)
            if update_status_form.is_valid():
                status = update_status_form.save(commit=False)
                status.author = request.user
                status.save()
                return redirect("status:status-profile", user_id=account.pk)

        update_status_form = StatusForm()
        context['is_self'] = is_self
        context['account_statuses_list'] = account_statuses_list
        context['update_status_form'] = update_status_form
        
        return render(request, 'status/status_profile.html', context)
    else:
        HttpResponse("Must be authenticated to view")