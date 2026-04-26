from django.shortcuts import render


def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')


def leaderboard_view(request):
    return render(request, 'dashboard/leaderboard.html')
