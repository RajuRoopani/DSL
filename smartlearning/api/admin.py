from django.contrib import admin
from activity.models import ActivityLog, UserStatistics


# ============ Activity & Statistics ============

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'object_type', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('user__username', 'description')
    readonly_fields = ('created_at', 'ip_address', 'user_agent')


@admin.register(UserStatistics)
class UserStatisticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_xp', 'total_skills_completed', 'rank', 'current_streak', 'percentile')
    list_filter = ('rank', 'current_streak', 'last_updated')
    search_fields = ('user__username',)
    readonly_fields = ('last_updated',)
