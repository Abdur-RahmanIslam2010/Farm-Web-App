from typing import Any, Mapping
from django import forms
from django.contrib.auth.models import User
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=64, min_length=8)
    password_confirm = forms.CharField(widget=forms.PasswordInput, max_length=64, min_length=8, label="Confirm Password")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ""

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm']

    def clean(self): # type: ignore
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    