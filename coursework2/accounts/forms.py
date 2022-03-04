from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate
from .models import *

# For Registration
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=256)
    date_of_birth = forms.DateField()

    class Meta:
        model = Account
        fields = ('email', 'username', 'full_name', 'date_of_birth' , 'password1', 'password2')

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

# For Login
class LoginForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    
    class Meta:
        model = Account
        fields = ('email', 'password')
    
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Not a valid login.")