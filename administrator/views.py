from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_protect
from register.models import AppUser
from payapp.models import Transaction
from .forms import AdminRegistrationForm


class AdminLoginView(LoginView):
    template_name = 'administrator/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return '/webapps2024/administrator/dashboard/'


@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    users = AppUser.objects.all()
    transactions_sent = None
    transactions_received = None

    username = request.GET.get('username', None)
    if username:
        transactions_sent = Transaction.objects.filter(sender__username=username)
        transactions_received = Transaction.objects.filter(recipient__username=username)

    return render(request, 'administrator/dashboard.html', {
        'users': users,
        'transactions_sent': transactions_sent,
        'transactions_received': transactions_received
    })


@user_passes_test(lambda u: u.is_staff)
@csrf_protect
def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            return redirect('admin_dashboard')
    else:
        form = AdminRegistrationForm()
    return render(request, 'administrator/register.html', {'form': form})
