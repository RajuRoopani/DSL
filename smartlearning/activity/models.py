from django.db import models
from django.contrib.auth.models import User


class ActivityLog(models.Model):
    """Audit trail for user activities."""
    ACTION_TYPES = [
        ('signup', 'User Signup'),
        ('login', 'User Login'),
        ('add_xp', 'Added Experience Points'),
        ('skill_started', 'Skill Started'),
        ('topic_completed', 'Topic Completed'),
        ('resource_viewed', 'Resource Viewed'),
        ('badge_earned', 'Badge Earned'),
        ('profile_updated', 'Profile Updated'),
        ('roadmap_generated', 'Roadmap Generated'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs', null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_TYPES)
    
    # Contextual info
    object_type = models.CharField(max_length=100, blank=True)
    object_id = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.get_action_display()}"


class UserStatistics(models.Model):
    """Aggregated user learning statistics."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='statistics')
    
    # Stats
    total_skills_started = models.IntegerField(default=0)
    total_skills_completed = models.IntegerField(default=0)
    total_topics_completed = models.IntegerField(default=0)
    total_resources_viewed = models.IntegerField(default=0)
    total_xp = models.IntegerField(default=0)
    total_badges_earned = models.IntegerField(default=0)
    
    # Time tracking
    total_learning_minutes = models.IntegerField(default=0)
    average_session_minutes = models.FloatField(default=0.0)
    
    # Engagement
    days_active = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    
    # Rankings
    rank = models.IntegerField(default=0)
    percentile = models.FloatField(default=0.0, help_text="0-100 percentile of users")
    
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} Statistics"
