from django.db import models
from register.models import AppUser


# Create your models here.
class Transaction(models.Model):
    sender = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='sent_transactions')
    recipient = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='received_transactions')
    sentAmount = models.DecimalField(max_digits=10, decimal_places=2)
    sentCurrency = models.CharField(max_length=3)
    receiveAmount = models.DecimalField(max_digits=10, decimal_places=2)
    receiveCurrency = models.CharField(max_length=3)
    timestamp = models.DateTimeField(auto_now_add=True)


class PaymentRequest(models.Model):
    requester = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='sent_requests')
    recipient = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='received_requests')
    sentAmount = models.DecimalField(max_digits=10, decimal_places=2)
    sentCurrency = models.CharField(max_length=3)
    receiveAmount = models.DecimalField(max_digits=10, decimal_places=2)
    receiveCurrency = models.CharField(max_length=3)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='pending')
