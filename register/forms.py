from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import AppUser
import requests


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    firstname = forms.CharField(max_length=50, required=True)
    lastname = forms.CharField(max_length=50, required=True)
    currency_choices = [
        ("GBP", "British Pound"),
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
    ]
    currency = forms.ChoiceField(choices=currency_choices, required=True)

    class Meta:
        model = AppUser
        fields = ["username", "firstname", "lastname", "email", "currency", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["firstname"]
        user.last_name = self.cleaned_data["lastname"]
        user.email = self.cleaned_data["email"]
        user.currency = self.cleaned_data["currency"]
        user.set_password(self.cleaned_data["password1"])
        currency = self.cleaned_data["currency"]

        base_amount = 1000  #base value for balance
        if currency != 'GBP':
            conversion_url = f"{settings.BASE_URL}/api/conversion/GBP/{currency}/{base_amount}"
            response = requests.get(conversion_url)
            if response.status_code == 200:
                converted_amount = response.json()['converted_amount']
            else:
                #set user currency to base amount in GBP if conversion fails
                converted_amount = base_amount
                user.currency = 'GBP'
        else:
            converted_amount = base_amount

        user.balance = converted_amount
        if commit:
            user.save()
        return user
