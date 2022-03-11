from django import forms
from .models import *

class StatusForm(forms.ModelForm):
    textUpdate = forms.CharField(required=True)

    class Meta:
        model = StatusList
        exclude = ("author", )