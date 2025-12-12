from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'timezone', 'receive_event_notifications', 'created_at']
    list_filter = ['receive_event_notifications', 'receive_marketing_emails', 'timezone']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'location']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Profile Information', {
            'fields': ('bio', 'avatar_url', 'location', 'website')
        }),
        ('Social Links', {
            'fields': ('twitter_handle', 'linkedin_url', 'github_url'),
            'classes': ('collapse',)
        }),
        ('Preferences', {
            'fields': ('receive_event_notifications', 'receive_marketing_emails', 'timezone')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
