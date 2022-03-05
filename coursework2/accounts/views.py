import email
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate , logout
from django.contrib import messages
from django.conf import settings

from .forms import *
from .models import *

# Create your views here.

# Register View
def user_register(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))
    
    context = {}
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            # validates the data and creates the account
            registration_form.save()
            print(registration_form.cleaned_data)
            messages.success(request,'Your account has been successfully created!')
        else:
            context['registration_form'] = registration_form
    else:
        registration_form = RegistrationForm()
        context['registration_form'] = registration_form

    return render(request, 'accounts/register.html', context)

# Login View
def user_login(request):
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
def user_logout(request):
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
        context['id'] = account. id
        context['username'] = account.username
        context['email'] = account.email
        context['date_of_birth'] = account.date_of_birth
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

        # Define template variables
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False
            
        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL
        return render(request, "accounts/account.html", context)

# Search Friends View
def user_search(request, *args, **kwargs):
    context = {}

    if request.method == 'GET':
        #searching for variable q
        search_query = request.GET.get("q")
        if len(search_query) > 0:
            # filter to get multiple rows because can have more than 1 result
            search_results = Account.objects.filter(full_name__icontains=search_query).filter(
                username__icontains=search_query).filter(email__icontains=search_query).distinct()
            # in array store account details and if you are friends or not
            accounts = []
            for account in search_results:
                accounts.append((account, False))
            context['accounts'] = accounts

    return render(request, "accounts/search.html", context)