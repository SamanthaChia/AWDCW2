from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.
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