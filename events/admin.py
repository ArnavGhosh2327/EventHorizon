from django.contrib import admin
from .models import Category, Tag, Venue, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue_type', 'city', 'country', 'capacity']
    list_filter = ['venue_type', 'country']
    search_fields = ['name', 'city', 'address']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'venue_type', 'capacity')
        }),
        ('Physical Location', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code', 'latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Virtual Information', {
            'fields': ('online_url',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'start_datetime', 'status', 'visibility', 'capacity']
    list_filter = ['status', 'visibility', 'category', 'start_datetime']
    search_fields = ['title', 'description', 'organizer__username']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'start_datetime'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description', 'organizer')
        }),
        ('Categorization', {
            'fields': ('category', 'tags')
        }),
        ('Venue', {
            'fields': ('venue',)
        }),
        ('Timing', {
            'fields': ('start_datetime', 'end_datetime', 'timezone')
        }),
        ('Registration', {
            'fields': ('capacity', 'registration_required', 'registration_open_datetime', 'registration_close_datetime')
        }),
        ('Status & Visibility', {
            'fields': ('status', 'visibility')
        }),
        ('Media', {
            'fields': ('cover_image',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
