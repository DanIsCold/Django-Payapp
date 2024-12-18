from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    currency_choices = [
        ("GBP", "British Pound"),
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
    ]
    currency = models.CharField(max_length=3, choices=currency_choices, default="GBP")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
