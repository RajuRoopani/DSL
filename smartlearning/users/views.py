from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from progress.models import Progress


def dummy_view(request):
    return HttpResponse('users placeholder')


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
    progress = Progress.objects.filter(user=request.user).aggregate(total=models.Sum('xp'))
    total_xp = progress.get('total') or 0
    return render(request, 'users/profile.html', {'total_xp': total_xp})
