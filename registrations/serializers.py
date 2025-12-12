from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Registration, Ticket
from events.serializers import EventListSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for event registrations"""
    event_details = EventListSerializer(source='event', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Registration
        fields = [
            'id', 'event', 'event_details', 'user', 'user_username', 'status',
            'registration_datetime', 'confirmation_datetime', 'cancellation_datetime',
            'notes', 'dietary_requirements', 'special_requests',
            'checked_in', 'check_in_datetime', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'registration_datetime', 'confirmation_datetime',
            'cancellation_datetime', 'check_in_datetime', 'updated_at'
        ]
    
    def validate_event(self, value):
        """Validate event registration"""
        if not value.is_registration_open:
            raise serializers.ValidationError("Registration is not open for this event")
        
        if value.is_full:
            raise serializers.ValidationError("This event is full")
        
        return value


class RegistrationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating registrations"""
    
    class Meta:
        model = Registration
        fields = ['event', 'notes', 'dietary_requirements', 'special_requests']
    
    def validate_event(self, value):
        """Validate event registration"""
        if not value.is_registration_open:
            raise serializers.ValidationError("Registration is not open for this event")
        
        if value.is_full:
            raise serializers.ValidationError("This event is full")
        
        return value
    
    def create(self, validated_data):
        """Create registration with auto-confirmation for free events"""
        registration = Registration.objects.create(**validated_data)
        # Auto-confirm for events without tickets
        if not registration.event.tickets.exists():
            registration.confirm()
        return registration


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for event tickets"""
    is_available = serializers.BooleanField(read_only=True)
    remaining_quantity = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'event', 'name', 'description', 'ticket_type',
            'price', 'currency', 'quantity_available', 'quantity_sold',
            'sale_start_datetime', 'sale_end_datetime',
            'min_per_order', 'max_per_order', 'is_active',
            'is_available', 'remaining_quantity',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'quantity_sold', 'is_available', 'remaining_quantity',
            'created_at', 'updated_at'
        ]
