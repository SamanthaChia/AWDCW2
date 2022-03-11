from email.errors import StartBoundaryNotFoundDefect
from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from accounts.models import *
from friends.friend_request_status import *

# Create your views here.
def status_profile(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        user_id = kwargs.get("user_id")
        if user_id != None:
            # retrieve user that i'm looking at
            try:
                account = Account.objects.get(pk=user_id)
                context['account'] = account
            except Account.DoesNotExist:
                return HttpResponse("User doesn't exist")
            
            try:
                account_statuses_list = StatusList.objects.filter(author=user_id)
                context['account_statuses_list'] = account_statuses_list
            except StatusList.DoesNotExist:
                return HttpResponse("Statuses do not exist")
            
            # statuses = []
            # for status in account_statuses_list:
            #     statuses.append(status)
            # context['statuses'] = status

        return render(request, 'status/status_profile.html', context)