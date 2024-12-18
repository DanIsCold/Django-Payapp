from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.AdminLoginView.as_view(), name='AdminLoginView'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register/', views.register_admin, name='register_admin')
]