from django.urls import path
from . import views

urlpatterns =[
    path('make_payment/', views.make_payment, name='make_payment'),
    path('request_payment/', views.request_payment, name='request_payment'),
    path('handle_payment_request/<int:request_id>/', views.handle_payment_request, name='handle_payment_request')
]
