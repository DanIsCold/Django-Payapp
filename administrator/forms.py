from django import forms
from django.contrib.auth.forms import UserCreationForm
from register.models import AppUser


class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ('username', 'email', 'password1', 'password2')
