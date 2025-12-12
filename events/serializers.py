from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Tag, Venue, Event


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at']
        read_only_fields = ['created_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['created_at']


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = [
            'id', 'name', 'venue_type', 'address', 'city', 'state', 
            'country', 'postal_code', 'latitude', 'longitude', 
            'online_url', 'capacity', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer for event organizer info"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id', 'username', 'email']


class EventListSerializer(serializers.ModelSerializer):
    """Serializer for event list view with minimal data"""
    organizer = UserSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'short_description', 'organizer', 
            'category_name', 'tags', 'start_datetime', 'end_datetime',
            'status', 'visibility', 'cover_image', 'capacity', 
            'is_upcoming', 'is_full', 'available_spots'
        ]
        read_only_fields = ['is_upcoming', 'is_full', 'available_spots']


class EventDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed event view"""
    organizer = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    venue = VenueSerializer(read_only=True)
    
    # Add computed properties
    is_upcoming = serializers.BooleanField(read_only=True)
    is_past = serializers.BooleanField(read_only=True)
    is_ongoing = serializers.BooleanField(read_only=True)
    is_registration_open = serializers.BooleanField(read_only=True)
    available_spots = serializers.IntegerField(read_only=True)
    is_full = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'description', 'short_description',
            'organizer', 'category', 'tags', 'venue',
            'start_datetime', 'end_datetime', 'timezone',
            'capacity', 'registration_required', 
            'registration_open_datetime', 'registration_close_datetime',
            'status', 'visibility', 'cover_image',
            'created_at', 'updated_at',
            'is_upcoming', 'is_past', 'is_ongoing', 
            'is_registration_open', 'available_spots', 'is_full'
        ]
        read_only_fields = [
            'created_at', 'updated_at', 'is_upcoming', 'is_past', 
            'is_ongoing', 'is_registration_open', 'available_spots', 'is_full'
        ]


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating events"""
    
    class Meta:
        model = Event
        fields = [
            'title', 'slug', 'description', 'short_description',
            'category', 'tags', 'venue',
            'start_datetime', 'end_datetime', 'timezone',
            'capacity', 'registration_required',
            'registration_open_datetime', 'registration_close_datetime',
            'status', 'visibility', 'cover_image'
        ]

    def validate(self, data):
        """Validate event data"""
        if data.get('end_datetime') and data.get('start_datetime'):
            if data['end_datetime'] <= data['start_datetime']:
                raise serializers.ValidationError(
                    "End datetime must be after start datetime"
                )
        
        if data.get('registration_close_datetime') and data.get('start_datetime'):
            if data['registration_close_datetime'] > data['start_datetime']:
                raise serializers.ValidationError(
                    "Registration close datetime must be before event start"
                )
        
        return data
