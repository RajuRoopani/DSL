from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count, Sum
from django.contrib.auth.models import User

from users.models import Profile, Badge, UserBadge
from roadmap.models import Skill, Topic, Resource, UserSkillProgress
from activity.models import ActivityLog, UserStatistics
from api.serializers import (
    ProfileSerializer, BadgeSerializer, UserBadgeSerializer,
    SkillSerializer, SkillDetailSerializer, TopicSerializer, ResourceSerializer,
    UserSkillProgressSerializer, ActivityLogSerializer, UserStatisticsSerializer
)


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# ============ User Profile & Badges ============

class ProfileViewSet(viewsets.ModelViewSet):
    """User profile endpoints."""
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'bio', 'learning_goal']
    ordering_fields = ['total_xp', 'current_streak', 'created_at']
    ordering = ['-total_xp']
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Profile.objects.filter(public_profile=True) | Profile.objects.filter(user=self.request.user)
        return Profile.objects.filter(public_profile=True)


class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    """Available badges."""
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['badge_type', 'created_at']


class UserBadgeViewSet(viewsets.ReadOnlyModelViewSet):
    """User's earned badges."""
    serializer_class = UserBadgeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user)


# ============ Skills & Learning ============

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """Skills endpoints with search, filter, and recommendations."""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['popularity_score', 'learners_count', 'difficulty', 'created_at']
    ordering = ['-popularity_score']
    pagination_class = StandardPagination
    
    def get_serializer_class(self):
        """Use detailed serializer for detail view."""
        if self.action == 'retrieve':
            return SkillDetailSerializer
        return SkillSerializer
    
    def get_queryset(self):
        """Filter by difficulty and category if provided."""
        queryset = Skill.objects.all()
        
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    """Topics within skills."""
    queryset = Topic.objects.filter(status='published')
    serializer_class = TopicSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['order', 'created_at']
    ordering = ['order']
    
    def get_queryset(self):
        skill_id = self.request.query_params.get('skill_id')
        queryset = Topic.objects.filter(status='published')
        if skill_id:
            queryset = queryset.filter(skill_id=skill_id)
        return queryset


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """Learning resources."""
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'resource_type']
    ordering_fields = ['rating', 'duration_minutes', 'is_recommended', 'order']
    ordering = ['-is_recommended', 'order']
    
    def get_queryset(self):
        topic_id = self.request.query_params.get('topic_id')
        queryset = Resource.objects.all()
        if topic_id:
            queryset = queryset.filter(topic_id=topic_id)
        return queryset


class UserSkillProgressViewSet(viewsets.ModelViewSet):
    """User's skill progress tracking."""
    serializer_class = UserSkillProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserSkillProgress.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ============ Activity & Statistics ============

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """User activity audit trail."""
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'action']
    ordering = ['-created_at']
    pagination_class = StandardPagination
    
    def get_queryset(self):
        return ActivityLog.objects.filter(user=self.request.user)


class UserStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """User learning statistics."""
    serializer_class = UserStatisticsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return UserStatistics.objects.filter(
                Q(user=self.request.user) | Q(user__profile__public_profile=True)
            )
        return UserStatistics.objects.filter(user__profile__public_profile=True)


# ============ Recommendations & Analytics ============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommended_skills(request):
    """Get personalized skill recommendations."""
    user = request.user
    profile = user.profile
    
    # Get skills the user hasn't started
    user_skills = UserSkillProgress.objects.filter(user=user).values_list('skill_id', flat=True)
    recommended = Skill.objects.exclude(id__in=user_skills).order_by('-popularity_score')[:10]
    
    serializer = SkillSerializer(recommended, many=True)
    return Response({
        'total_xp': profile.total_xp,
        'recommended_skills': serializer.data
    })


@api_view(['GET'])
def skill_categories(request):
    """Get available skill categories."""
    categories = Skill.objects.values_list('category', flat=True).distinct().order_by('category')
    return Response({'categories': list(categories)})


@api_view(['GET'])
def leaderboard(request):
    """Global leaderboard with pagination."""
    limit = int(request.query_params.get('limit', 50))
    offset = int(request.query_params.get('offset', 0))
    
    leaderboard = Profile.objects.filter(
        public_profile=True
    ).order_by('-total_xp')[offset:offset+limit]
    
    data = [{
        'rank': idx + offset + 1,
        'username': profile.user.username,
        'total_xp': profile.total_xp,
        'current_streak': profile.current_streak,
        'badge_count': profile.user.earned_badges.count()
    } for idx, profile in enumerate(leaderboard)]
    
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard_stats(request):
    """Get comprehensive user dashboard statistics."""
    user = request.user
    profile = user.profile
    
    try:
        stats = UserStatistics.objects.get(user=user)
    except UserStatistics.DoesNotExist:
        stats = UserStatistics.objects.create(user=user)
    
    # Recent activity
    recent_activity = ActivityLog.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Current learning
    current_skills = UserSkillProgress.objects.filter(
        user=user, 
        mastery_level__lt=4
    ).order_by('-updated_at')[:5]
    
    return Response({
        'profile': ProfileSerializer(profile).data,
        'statistics': UserStatisticsSerializer(stats).data,
        'current_skills': UserSkillProgressSerializer(current_skills, many=True).data,
        'recent_activity': ActivityLogSerializer(recent_activity, many=True).data,
    })
