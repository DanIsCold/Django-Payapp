from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, PaymentRequest
from register.models import AppUser
from django.db import transaction
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import requests
from django.conf import settings
from decimal import Decimal
from django.shortcuts import get_object_or_404


# Create your views here.
@login_required
def home(request):
    sent_transactions = Transaction.objects.filter(sender=request.user)
    received_transactions = Transaction.objects.filter(recipient=request.user)
    payment_requests = PaymentRequest.objects.filter(recipient=request.user, status='pending')
    context = {
        'balance': request.user.balance,
        'currency': request.user.currency,
        'sent_transactions': sent_transactions,
        'received_transactions': received_transactions,
        'payment_requests': payment_requests
    }
    return render(request, 'payapp/home.html', context)


@login_required
@csrf_protect
def make_payment(request):
    context = {
        'balance': request.user.balance,
        'currency': request.user.currency
    }
    if request.method == 'POST':
        recipient_user = request.POST['recipient_username']
        amount = Decimal(request.POST['amount'])
        try:
            recipient = AppUser.objects.get(username=recipient_user)
            if request.user.balance >= amount:
                if request.user.currency != recipient.currency:
                    conversion_url = f"{settings.BASE_URL}/api/conversion/{request.user.currency}/{recipient.currency}/{amount}"
                    response = requests.get(conversion_url)
                    if response.status_code == 200:
                        converted_amount = Decimal(response.json()['converted_amount'])
                    else:
                        messages.error(request, 'Error converting currency')
                        return redirect('make_payment')
                else:
                    converted_amount = amount

                with transaction.atomic():
                    request.user.balance -= amount
                    recipient.balance += converted_amount
                    request.user.save()
                    recipient.save()
                    Transaction.objects.create(
                        sender=request.user,
                        recipient=recipient,
                        sentAmount=amount,
                        sentCurrency=request.user.currency,
                        receiveAmount=converted_amount,
                        receiveCurrency=recipient.currency
                    )
                return redirect('home')
            else:
                messages.error(request, 'Insufficient funds!')
        except AppUser.DoesNotExist:
            messages.error(request, 'Invalid recipient')
    return render(request, 'payapp/make_payment.html', context)


@login_required
@csrf_protect
def request_payment(request):
    context = {
        'balance': request.user.balance,
        'currency': request.user.currency
    }
    if request.method == 'POST':
        recipient_username = request.POST['recipient_username']
        amount = Decimal(request.POST['amount'])
        try:
            recipient = AppUser.objects.get(username=recipient_username)
            if request.user.currency != recipient.currency:
                conversion_url = f"{settings.BASE_URL}/api/conversion/{request.user.currency}/{recipient.currency}/{amount}"
                response = requests.get(conversion_url)
                if response.status_code == 200:
                    converted_amount = Decimal(response.json()['converted_amount'])
                else:
                    messages.error(request, 'Error converting currency')
                    return redirect('request_payment')
            else:
                converted_amount = amount

            PaymentRequest.objects.create(
                requester=request.user,
                recipient=recipient,
                sentAmount=converted_amount,
                sentCurrency=recipient.currency,
                receiveAmount=amount,
                receiveCurrency=request.user.currency
            )
            return redirect('home')
        except AppUser.DoesNotExist:
            messages.error(request, 'Invalid recipient')
    return render(request, 'payapp/request_payment.html', context)

@login_required
@csrf_protect
def handle_payment_request(request, request_id):
    payment_request = get_object_or_404(PaymentRequest, id=request_id, recipient=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            with transaction.atomic():
                request.user.balance -= payment_request.sentAmount
                payment_request.requester.balance += payment_request.receiveAmount
                request.user.save()
                payment_request.requester.save()
                Transaction.objects.create(
                    sender=request.user,
                    recipient=payment_request.requester,
                    sentAmount=payment_request.sentAmount,
                    sentCurrency=payment_request.sentCurrency,
                    receiveAmount=payment_request.receiveAmount,
                    receiveCurrency=payment_request.receiveCurrency
                )
                payment_request.status = 'accepted'
                payment_request.save()
        elif action == 'reject':
            payment_request.status = 'rejected'
            payment_request.save()
    return redirect('home')
