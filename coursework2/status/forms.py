from django import forms
from .models import *

class StatusForm(forms.ModelForm):
    textUpdate = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "What's happening today?",
                "class": "textarea"
            }
        ),
        label="",
    )

    image = forms.ImageField(
        required=False,
        widget=forms.widgets.ClearableFileInput(
            attrs={
                "multiple": True
            }
        ),
        label="Upload Image ",
    )

    class Meta:
        model = StatusList
        fields = ['textUpdate']
        exclude = ("author", )