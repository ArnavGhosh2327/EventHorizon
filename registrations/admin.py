from django.contrib import admin
from .models import Registration, Ticket


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'checked_in', 'registration_datetime']
    list_filter = ['status', 'checked_in', 'registration_datetime']
    search_fields = ['user__username', 'user__email', 'event__title']
    readonly_fields = ['registration_datetime', 'confirmation_datetime', 'cancellation_datetime', 'check_in_datetime', 'updated_at']
    
    fieldsets = (
        ('Registration Information', {
            'fields': ('event', 'user', 'status')
        }),
        ('Additional Details', {
            'fields': ('notes', 'dietary_requirements', 'special_requests'),
            'classes': ('collapse',)
        }),
        ('Attendance', {
            'fields': ('checked_in', 'check_in_datetime')
        }),
        ('Timestamps', {
            'fields': ('registration_datetime', 'confirmation_datetime', 'cancellation_datetime', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['confirm_registrations', 'cancel_registrations', 'check_in_attendees']
    
    def confirm_registrations(self, request, queryset):
        for registration in queryset:
            registration.confirm()
        self.message_user(request, f"{queryset.count()} registrations confirmed.")
    confirm_registrations.short_description = "Confirm selected registrations"
    
    def cancel_registrations(self, request, queryset):
        for registration in queryset:
            registration.cancel()
        self.message_user(request, f"{queryset.count()} registrations cancelled.")
    cancel_registrations.short_description = "Cancel selected registrations"
    
    def check_in_attendees(self, request, queryset):
        for registration in queryset:
            registration.check_in()
        self.message_user(request, f"{queryset.count()} attendees checked in.")
    check_in_attendees.short_description = "Check in selected attendees"


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'ticket_type', 'price', 'quantity_sold', 'is_active']
    list_filter = ['ticket_type', 'is_active', 'created_at']
    search_fields = ['name', 'event__title']
    readonly_fields = ['created_at', 'updated_at', 'quantity_sold']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('event', 'name', 'description', 'ticket_type')
        }),
        ('Pricing', {
            'fields': ('price', 'currency')
        }),
        ('Availability', {
            'fields': ('quantity_available', 'quantity_sold', 'is_active')
        }),
        ('Sale Period', {
            'fields': ('sale_start_datetime', 'sale_end_datetime'),
            'classes': ('collapse',)
        }),
        ('Order Limits', {
            'fields': ('min_per_order', 'max_per_order'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
