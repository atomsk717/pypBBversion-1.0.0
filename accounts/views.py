from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.views.decorators.http import require_POST


def register(request):
    if request.user.is_authenticated:
        return redirect('forum:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optional: log the user in immediately after registration
            # login(request, user)
            return redirect('accounts:login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('forum:home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('forum:home')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})




@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('forum:home')