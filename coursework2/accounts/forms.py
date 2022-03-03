from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate
from .models import *

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(max_length=256)
    
    class Meta:
        model = Account
        fields = ['email', 'username' ,'name', 'phone', 'date_of_birth', 'password1', 'password2']

        #validation, must have clean infront for django to know.
        def clean_email(self):
            email = self.cleaned_data.get("email").lower()
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is alreade in use' % account)

        def clean_username(self):
            username = self.cleaned_data.get("username")
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is alreade in use' % username)

        def clean_password2(self):
            # Check that the two password entries match
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            return password2