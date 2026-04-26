from rest_framework import serializers
from users.models import Profile, Badge, UserBadge
from roadmap.models import Skill, Topic, Resource, UserSkillProgress
from activity.models import ActivityLog, UserStatistics
from django.contrib.auth.models import User


# ============ User & Profile ============

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'bio', 'avatar_url', 'learning_goal',
            'github_url', 'linkedin_url', 'portfolio_url',
            'total_xp', 'current_streak', 'longest_streak',
            'email_notifications', 'public_profile', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_xp', 'current_streak', 'longest_streak', 'created_at', 'updated_at']


# ============ Badges & Achievements ============

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'name', 'description', 'icon_emoji', 'badge_type', 'xp_threshold', 'streak_threshold']


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    
    class Meta:
        model = UserBadge
        fields = ['id', 'badge', 'earned_at']
        read_only_fields = ['id', 'earned_at']


# ============ Skills & Learning ============

class SkillBasicSerializer(serializers.ModelSerializer):
    """Lightweight skill serializer."""
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'difficulty', 'icon_emoji', 'learners_count', 'popularity_score']


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = [
            'id', 'topic', 'title', 'description', 'url', 'resource_type',
            'difficulty', 'duration_minutes', 'rating', 'is_recommended', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class TopicSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Topic
        fields = [
            'id', 'skill', 'title', 'description', 'learning_objectives',
            'order', 'estimated_hours', 'status', 'resources', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class SkillDetailSerializer(serializers.ModelSerializer):
    """Full skill serializer with topics and relations."""
    topics = TopicSerializer(many=True, read_only=True)
    prerequisites = SkillBasicSerializer(many=True, read_only=True)
    dependent_skills = SkillBasicSerializer(many=True, read_only=True)
    
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'description', 'category', 'difficulty', 'icon_emoji',
            'prerequisites', 'dependent_skills', 'learners_count', 'popularity_score',
            'topics', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'learners_count', 'popularity_score', 'created_at', 'updated_at']


class SkillSerializer(serializers.ModelSerializer):
    """Standard skill serializer."""
    class Meta:
        model = Skill
        fields = [
            'id', 'name', 'description', 'category', 'difficulty', 'icon_emoji',
            'learners_count', 'popularity_score', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'learners_count', 'created_at', 'updated_at']


class UserSkillProgressSerializer(serializers.ModelSerializer):
    skill = SkillBasicSerializer(read_only=True)
    mastery_level_display = serializers.CharField(source='get_mastery_level_display', read_only=True)
    
    class Meta:
        model = UserSkillProgress
        fields = [
            'id', 'skill', 'mastery_level', 'mastery_level_display',
            'xp_earned', 'topics_completed', 'resources_completed',
            'started_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'started_at', 'updated_at', 'completed_at']


# ============ Activity & Statistics ============

class ActivityLogSerializer(serializers.ModelSerializer):
    user_display = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = ActivityLog
        fields = [
            'id', 'user', 'user_display', 'action', 'action_display',
            'object_type', 'object_id', 'description', 'ip_address', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class UserStatisticsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserStatistics
        fields = [
            'id', 'user', 'total_skills_started', 'total_skills_completed',
            'total_topics_completed', 'total_resources_viewed', 'total_xp',
            'total_badges_earned', 'total_learning_minutes', 'average_session_minutes',
            'days_active', 'current_streak', 'longest_streak', 'rank', 'percentile',
            'last_updated'
        ]
        read_only_fields = ['id', 'user', 'last_updated']
