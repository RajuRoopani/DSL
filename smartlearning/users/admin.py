from django.contrib import admin
from .models import Profile, Badge, UserBadge


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'total_xp', 'current_streak', 'public_profile', 'created_at')
	search_fields = ('user__username', 'bio')
	list_filter = ('public_profile', 'email_notifications', 'created_at')
	ordering = ('-total_xp',)


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
	list_display = ('name', 'icon_emoji', 'badge_type', 'xp_threshold')
	list_filter = ('badge_type',)
	search_fields = ('name', 'description')


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
	list_display = ('user', 'badge', 'earned_at')
	list_filter = ('badge__badge_type', 'earned_at')
	search_fields = ('user__username', 'badge__name')
	readonly_fields = ('earned_at',)
