from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render

from payapp.models import Transaction
# Create your views here.


def convert_currency(request, currency1, currency2, amount):
    rates = {
        'GBP': {'USD': 1.25, 'EUR': 1.17},
        'USD': {'GBP': 0.8, 'EUR': 0.94},
        'EUR': {'GBP': 0.85, 'USD': 1.07}
    }
    try:
        amount = float(amount)
        rate = rates[currency1][currency2]
        converted_amount = round(amount * rate, 2)
        return JsonResponse({'converted_amount': converted_amount})
    except KeyError:
        return JsonResponse({'error': 'Error converting currency'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'Invalid amount'}, status=400)
