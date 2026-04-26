from django.shortcuts import render
from roadmap.models import Skill, Topic, UserSkillProgress, Roadmap, RoadmapTopicProgress


def dashboard_view(request):
    skills = Skill.objects.order_by('-popularity_score', 'name')

    roadmaps_by_skill = {}
    if request.user.is_authenticated:
        for roadmap in Roadmap.objects.filter(user=request.user).select_related('skill'):
            total = Topic.objects.filter(skill=roadmap.skill, status='published').count()
            done = RoadmapTopicProgress.objects.filter(roadmap=roadmap, completed=True).count()
            percent = round(done / total * 100) if total > 0 else 0
            roadmaps_by_skill[roadmap.skill_id] = {
                'roadmap': roadmap,
                'percent_complete': percent,
                'topics_completed': done,
            }

    skill_cards = []
    for skill in skills:
        info = roadmaps_by_skill.get(skill.id, {})
        skill_cards.append({
            'skill': skill,
            'roadmap': info.get('roadmap'),
            'percent_complete': info.get('percent_complete', 0),
            'topics_completed': info.get('topics_completed', 0),
        })

    return render(request, 'dashboard/dashboard.html', {'skill_cards': skill_cards})


def leaderboard_view(request):
    return render(request, 'dashboard/leaderboard.html')
