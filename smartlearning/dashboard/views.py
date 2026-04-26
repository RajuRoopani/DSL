from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from roadmap.models import Skill, Topic
from users.models import Profile


@login_required
def dashboard_view(request):
    """Dashboard showing user's learning progress and skills."""
    skills = Skill.objects.order_by('-popularity_score', 'name')[:10]
    
    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = request.user.profile
        except:
            user_profile = None
    
    skill_cards = []
    for skill in skills:
        topics = Topic.objects.filter(skill=skill, status='published').count()
        skill_cards.append({
            'skill': skill,
            'topics_count': topics,
        })

    return render(request, 'dashboard/dashboard.html', {
        'skill_cards': skill_cards,
        'user_profile': user_profile,
    })


def leaderboard_view(request):
    return render(request, 'dashboard/leaderboard.html')
