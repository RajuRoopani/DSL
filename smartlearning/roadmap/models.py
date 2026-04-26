from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    """Learning skill with metadata and recommendations."""
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    icon_emoji = models.CharField(max_length=10, blank=True)
    
    # Prerequisites and relations
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependent_skills')
    
    # Engagement metrics
    learners_count = models.IntegerField(default=0)
    popularity_score = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-popularity_score', 'name']
    
    def __str__(self):
        return f"{self.icon_emoji} {self.name}" if self.icon_emoji else self.name
    
    def get_recommended_next_skills(self):
        """Return skills that depend on this one (recommended to learn next)."""
        return self.dependent_skills.all()[:5]


class Topic(models.Model):
    """Topic within a skill with structured content."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    skill = models.ForeignKey(Skill, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    learning_objectives = models.TextField(blank=True, help_text="Comma-separated learning goals")

    order = models.IntegerField(default=0, help_text="Display order within skill")
    estimated_hours = models.FloatField(default=1.0)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['skill', 'order']

    def __str__(self):
        return f"{self.title} ({self.skill.name})"


class Resource(models.Model):
    """Learning resource with type and quality rating."""
    RESOURCE_TYPES = [
        ('video', 'Video'),
        ('article', 'Article'),
        ('tutorial', 'Tutorial'),
        ('documentation', 'Documentation'),
        ('book', 'Book'),
        ('course', 'Online Course'),
        ('interactive', 'Interactive'),
        ('exercise', 'Exercise/Project'),
    ]
    
    topic = models.ForeignKey(Topic, related_name='resources', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES, default='article')
    
    # Quality metrics
    difficulty = models.CharField(max_length=20, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium')
    duration_minutes = models.IntegerField(null=True, blank=True)
    rating = models.FloatField(default=0.0, help_text="Average rating 0-5")
    
    order = models.IntegerField(default=0)
    is_recommended = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['topic', 'order', 'is_recommended']
    
    def __str__(self):
        return f"{self.title} - {self.topic.title}"


class UserSkillProgress(models.Model):
    """Track user's progress on individual skills."""
    MASTERY_LEVELS = [
        (0, 'Not Started'),
        (1, 'Learning'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Expert'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skill_progress')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    
    mastery_level = models.IntegerField(choices=MASTERY_LEVELS, default=0)
    xp_earned = models.IntegerField(default=0)
    topics_completed = models.IntegerField(default=0)
    resources_completed = models.IntegerField(default=0)
    
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('user', 'skill')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.skill.name} (Level {self.mastery_level})"


class Roadmap(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    GOAL_CHOICES = [
        ('interview_prep', 'Interview Prep'),
        ('portfolio', 'Portfolio Project'),
        ('general', 'General Learning'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roadmaps')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    hours_per_week = models.IntegerField()
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user.username} — {self.skill.name} ({self.level})"


class RoadmapTopicProgress(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='topic_progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('roadmap', 'topic')

    def __str__(self):
        return f"{self.roadmap} — {self.topic.title} ({'done' if self.completed else 'pending'})"
