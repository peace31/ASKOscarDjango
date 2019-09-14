from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=30)
    password = forms.CharField(max_length=30)
    referralcode = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


def ValidateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
