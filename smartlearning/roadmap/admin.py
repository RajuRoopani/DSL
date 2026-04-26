from django.contrib import admin
from .models import Skill, Topic, Resource, UserSkillProgress


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'difficulty', 'icon_emoji', 'learners_count', 'popularity_score')
	list_filter = ('difficulty', 'category', 'created_at')
	search_fields = ('name', 'description')
	filter_horizontal = ('prerequisites',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
	list_display = ('title', 'skill', 'status', 'estimated_hours', 'order')
	list_filter = ('status', 'skill', 'created_at')
	search_fields = ('title', 'description')
	ordering = ('skill', 'order')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
	list_display = ('title', 'topic', 'resource_type', 'difficulty', 'duration_minutes', 'rating', 'is_recommended')
	list_filter = ('resource_type', 'difficulty', 'is_recommended', 'created_at')
	search_fields = ('title', 'description')
	ordering = ('topic', 'order')


@admin.register(UserSkillProgress)
class UserSkillProgressAdmin(admin.ModelAdmin):
	list_display = ('user', 'skill', 'mastery_level', 'xp_earned', 'updated_at')
	list_filter = ('mastery_level', 'skill', 'updated_at')
	search_fields = ('user__username', 'skill__name')
	readonly_fields = ('started_at', 'updated_at')
