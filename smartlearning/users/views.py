from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from rest_framework.authtoken.models import Token
from progress.models import Progress

REACT_ORIGIN = 'http://localhost:5173'


def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return redirect(f'{REACT_ORIGIN}/?token={token.key}')
        error = 'Invalid username or password.'
    return render(request, 'users/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def profile(request):
    progress = Progress.objects.filter(user=request.user).aggregate(total=Sum('xp'))
    total_xp = progress.get('total') or 0
    return render(request, 'users/profile.html', {'total_xp': total_xp})
