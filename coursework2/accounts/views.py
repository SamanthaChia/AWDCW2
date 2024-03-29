import datetime
import os
import cv2 #opencv
import json
import base64
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth import login, authenticate , logout
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.core import files

from friends.models import *
from .forms import *
from .models import *
from friends.friend_request_status import *

TEMP_PROFILE_IMAGE_NAME = "temp_profile_image.png"

# Create your views here.

# Register View
def user_register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))
    
    context = {}
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            # validates the data and creates the account
            print(registration_form.cleaned_data)
            registration_form.save()
            messages.success(request,'Your account has been successfully created!')
        else:
            context['registration_form'] = registration_form
    else:
        registration_form = RegistrationForm()
        context['registration_form'] = registration_form

    return render(request, 'accounts/register.html', context)

# Login View
def user_login_view(request):
    context={}

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect("home")
                else:
                    return HttpResponse("Your account is disabled")
            else:
                return HttpResponse('Invalid login')
    else:
        login_form = LoginForm()
    
    context['login_form'] = login_form
    return render(request, "accounts/login.html", context)

# Logout view
def user_logout_view(request):
    logout(request)
    return redirect("home")

# Account view
def user_view(request, *args, **kwargs):
    context = {}
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
    except:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = account.id
        context['full_name'] = account.full_name
        context['username'] = account.username
        context['email'] = account.email
        context['date_of_birth'] = account.date_of_birth
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

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

        # Template vars
        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.no_request.value
        friend_requests = None
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
            # search through person friend list to check for user
            if friends.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
                # Friend send to you
                if get_friend_request(sender=account, receiver=user) != False:
                    request_sent = FriendRequestStatus.friend_sent.value
                    # retrieve the primary key
                    context['friend_request_id'] = get_friend_request(sender=account, receiver=user).pk
                # You send to friend
                elif get_friend_request(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.user_sent.value
                # no request
                else:
                    request_sent = FriendRequestStatus.no_request.value
        elif not user.is_authenticated:
            is_self = False
        # Looking at own account, check friend requests
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=user, pending_request_status=True)
            except:
                pass
        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL
        context['request_sent'] = request_sent
        context['friend_requests'] = friend_requests
        return render(request, "accounts/account.html", context)

# Search Friends View
def user_search_view(request, *args, **kwargs):
    context = {}

    if request.method == 'GET':
        #searching for variable q
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            # filter to get multiple rows because can have more than 1 result
            search_results = Account.objects.filter(full_name__icontains=search_query).filter(
                username__icontains=search_query).filter(email__icontains=search_query).distinct()
            user = request.user
            # in array store account details and if you are friends or not
            accounts = []
            if user.is_authenticated:
                user_friend_list = FriendsList.objects.get(user=user)
                for account in search_results:
                    accounts.append((account, user_friend_list.check_mutual_friends(account)))
                context['accounts'] = accounts
            else:
                for account in search_results:
                    accounts.append((account, False))
                context['accounts'] = accounts

    return render(request, "accounts/search.html", context)

# Edit Particulars View
def edit_particulars_view(request, *args, **kwargs):
    context = {}

    # check if user is logged in
    if not request.user.is_authenticated:
        return redirect("account:login")
    user_id = kwargs.get("user_id")
    try:
        account = Account.objects.get(pk=user_id)
    except Account.DoesNotExist:
        return HttpResponse("Something went wrong")

    # check if user editing own profile    
    if account.pk != request.user.pk:
        return HttpResponse("This is not your account, you are not allowed to edit this profile!")
    
    if request.method == "POST":
        update_form = EditParticularsForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            #delete old profile image so keep the name
            account.profile_image.delete()
            update_form.save()
            return redirect("account:user_view", user_id=account.pk)
        else:
            if(account.date_of_birth == None ):
                date_time_val = account.date_of_birth
            else:
                date_time_val = datetime.datetime.strptime(str(account.date_of_birth), '%Y-%m-%d').strftime('%Y-%m-%d')

            update_form = EditParticularsForm(request.POST, instance=request.user,
                initial={
                    "id": account.pk,
                    "email": account.email,
                    "username": account.username,
                    "full_name": account.full_name,
                    "date_of_birth": date_time_val,
                    "profile_image":account.profile_image,
                    "hide_email": account.hide_email,
                }
            )
            context['update_form'] = update_form

    else:
        if(account.date_of_birth == None):
            date_time_val = account.date_of_birth
        else:
            date_time_val = datetime.datetime.strptime(str(account.date_of_birth), '%Y-%m-%d').strftime('%Y-%m-%d')
        
        update_form = EditParticularsForm(
                    initial={
                        "id": account.pk,
                        "email": account.email,
                        "username": account.username,
                        "full_name": account.full_name,
                        "date_of_birth": date_time_val,
                        "profile_image":account.profile_image,
                        "hide_email": account.hide_email,
                    }
        )

        context['update_form'] = update_form
    return render(request, "accounts/update_particulars.html", context)

def save_temp_profile_image_from_base64String(imageString, user):
    try:
        # all users have a unique temp profile image depending on primary key
        if not os.path.exists(settings.TEMP):
            os.mkdir(settings.TEMP)
        if not os.path.exists(settings.TEMP + "/" + str(user.pk)):
            os.mkdir(settings.TEMP + "/" + str(user.pk))
        url = os.path.join(settings.TEMP + "/" + str(user.pk), TEMP_PROFILE_IMAGE_NAME)
        storage = FileSystemStorage(location=url)
        image = base64.b64decode(imageString)
        with storage.open('', 'wb+') as destination:
            destination.write(image)
            destination.close()
        return url

    except Exception as e:
        if str(e) == "Incorrect padding":
            imageString += "=" * ((4 - len(imageString) % 4) % 4)
            return save_temp_profile_image_from_base64String(imageString, user)
        return None

# called asynchronously through AJAX
def crop_image_view(request, *args, **kwargs):
    payload = {}
    user = request.user
    if request.POST and user.is_authenticated:
        try:
            imageString = request.POST.get("image")
            # user upload image, we take image and convert it into base 64 String
            url = save_temp_profile_image_from_base64String(imageString, user)
            # load image
            img = cv2.imread(url)

            #convert into an integer for crop values
            cropX = int(float(str(request.POST.get("cropX"))))
            cropY = int(float(str(request.POST.get("cropY"))))
            cropWidth = int(float(str(request.POST.get("cropWidth"))))
            cropHeight = int(float(str(request.POST.get("cropHeight"))))

            if cropX < 0:
                cropX = 0
            if cropY < 0:
                cropY = 0

            crop_img = img[cropY:cropY + cropHeight, cropX:cropX+cropWidth]
            cv2.imwrite(url, crop_img)
            user.profile_image.delete()

            user.profile_image.save("profile_image.png", files.File(open(url, 'rb')))
            user.save()

            payload['result'] = "success"
            payload['cropped_profile_image'] = user.profile_image.url

            os.remove(url)

        except Exception as e:
            payload['result'] = "error"
            payload['exception'] = str(e)

    return HttpResponse(json.dumps(payload), content_type="application/json")