from django.db import models
from django.utils import timezone


class Profile(models.Model):
    """Enhanced user profile with rich metadata and learning stats."""
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True, help_text="Profile picture URL")
    learning_goal = models.CharField(max_length=255, blank=True, null=True)
    
    # Social links
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    
    # Learning stats
    total_xp = models.IntegerField(default=0, help_text="Total experience points earned")
    current_streak = models.IntegerField(default=0, help_text="Days learning consecutively")
    longest_streak = models.IntegerField(default=0, help_text="Longest learning streak")
    last_activity_date = models.DateField(null=True, blank=True)
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    public_profile = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-total_xp', '-created_at']
    
    def __str__(self):
        return f"Profile({self.user.username})"
    
    def update_streak(self):
        """Update learning streak based on last_activity_date."""
        if self.last_activity_date is None:
            self.current_streak = 1
            self.last_activity_date = timezone.now().date()
        else:
            today = timezone.now().date()
            yesterday = today - timezone.timedelta(days=1)
            
            if self.last_activity_date == today:
                # Already updated today
                pass
            elif self.last_activity_date == yesterday:
                # Continuing streak
                self.current_streak += 1
                if self.current_streak > self.longest_streak:
                    self.longest_streak = self.current_streak
            else:
                # Streak broken
                self.current_streak = 1
            
            self.last_activity_date = today
        
        self.save(update_fields=['current_streak', 'longest_streak', 'last_activity_date'])
    
    def add_xp(self, amount):
        """Add XP to user and update streak."""
        self.total_xp += amount
        self.update_streak()
        self.save(update_fields=['total_xp'])


class Badge(models.Model):
    """Achievement badges users can earn."""
    BADGE_TYPES = [
        ('xp', 'Experience Milestone'),
        ('streak', 'Learning Streak'),
        ('skill', 'Skill Expert'),
        ('social', 'Community Champion'),
        ('achievement', 'Special Achievement'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon_emoji = models.CharField(max_length=10)
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    
    # Unlock criteria
    xp_threshold = models.IntegerField(null=True, blank=True, help_text="Unlock at this XP level")
    streak_threshold = models.IntegerField(null=True, blank=True, help_text="Unlock at this streak length")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['badge_type', 'name']
    
    def __str__(self):
        return f"{self.icon_emoji} {self.name}"


class UserBadge(models.Model):
    """Track badges earned by users."""
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'badge')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
