from django.shortcuts import render
from django.http import HttpResponse

from accounts.models import *

# Create your views here.
def index(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return HttpResponse("Something went wrong.")

    if account:
            context['username'] = account.username
    return render(request, 'chat/index.html', context)

def room(request, room_name):
    username = request.GET.get('username', 'Anonymous')
    return render(request, 'chat/room.html', {'room_name': room_name, 'username': username})


# def room(request, *args, **kwargs):
#     context = {}
#     user_id = kwargs.get("user_id")
#     try:
#         account = Account.objects.get(pk=user_id)
#     except:
#         return HttpResponse("Something went wrong.")

#     if account:
#             context['username'] = account.username

#     return render(request, 'chat/room.html', context)