from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    ProfileViewSet, BadgeViewSet, UserBadgeViewSet,
    SkillViewSet, TopicViewSet, ResourceViewSet, UserSkillProgressViewSet,
    ActivityLogViewSet, UserStatisticsViewSet,
    recommended_skills, skill_categories, leaderboard, user_dashboard_stats
)

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'badges', BadgeViewSet, basename='badge')
router.register(r'user-badges', UserBadgeViewSet, basename='user-badge')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'skill-progress', UserSkillProgressViewSet, basename='skill-progress')
router.register(r'activity', ActivityLogViewSet, basename='activity')
router.register(r'statistics', UserStatisticsViewSet, basename='statistics')

urlpatterns = [
    path('', include(router.urls)),
    path('recommended-skills/', recommended_skills, name='recommended-skills'),
    path('skill-categories/', skill_categories, name='skill-categories'),
    path('leaderboard/', leaderboard, name='api-leaderboard'),
    path('dashboard-stats/', user_dashboard_stats, name='dashboard-stats'),
]
