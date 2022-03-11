from django import forms
from .models import *

class StatusForm(forms.ModelForm):
    textUpdate = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "What's happening today?",
                "class": "textarea"
            }
        ),
        label="",
    )

    class Meta:
        model = StatusList
        exclude = ("author", )