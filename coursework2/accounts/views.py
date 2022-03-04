import email
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate , logout

from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.

# Register View
def register(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))
    
    context = {}

    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        print(registration_form.data)
        if registration_form.is_valid():
            #Creates account
            registration_form.save()
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
    return render(request, "account/login.html", context)

# Logout view
def user_logout(request):
    logout(request)
    return redirect("home")