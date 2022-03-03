from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from .forms import *
from .models import *

# Create your views here.
def register(request, *args, **kwargs):
    context = {}

    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        print(registration_form.data)
        if registration_form.is_valid():
            #Creates account
            registration_form.save()
            #retrieve the needed things to automatically login for the user
            email = registration_form.cleaned_data.get('email').lower()
            password1 = registration_form.cleaned_data.get('password1')
            account = authenticate(email=email,password=password1)
            login(request, account)
            # after logging in redirect to login
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect("home")
        else:
            context['registration_form'] = registration_form
    else:
        registration_form = RegistrationForm()
        context['registration_form'] = registration_form

    return render(request, 'accounts/register.html', context)