from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.utils import timezone
from .models import Category, Tag, Venue, Event
from .serializers import (
    CategorySerializer, TagSerializer, VenueSerializer,
    EventListSerializer, EventDetailSerializer, EventCreateUpdateSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for event categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for event tags"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class VenueViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for venues"""
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'country']
    ordering_fields = ['name', 'city', 'created_at']


class EventViewSet(viewsets.ModelViewSet):
    """API endpoint for events"""
    queryset = Event.objects.filter(status='published', visibility='public')
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['start_datetime', 'created_at', 'title']
    ordering = ['start_datetime']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'list':
            return EventListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EventCreateUpdateSerializer
        return EventDetailSerializer
    
    def get_queryset(self):
        """Filter queryset based on user and query parameters"""
        queryset = super().get_queryset()
        
        # Show all events for authenticated users viewing their own events
        if self.request.user.is_authenticated:
            if self.action in ['my_events', 'my_organized_events']:
                return Event.objects.filter(organizer=self.request.user)
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Filter by tag
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        # Filter by upcoming/past
        time_filter = self.request.query_params.get('time', None)
        if time_filter == 'upcoming':
            queryset = queryset.filter(start_datetime__gte=timezone.now())
        elif time_filter == 'past':
            queryset = queryset.filter(end_datetime__lt=timezone.now())
        
        return queryset.distinct()
    
    def perform_create(self, serializer):
        """Set the organizer to the current user"""
        serializer.save(organizer=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_events(self, request):
        """Get events the user is registered for"""
        registrations = request.user.registrations.filter(
            status__in=['confirmed', 'pending']
        ).select_related('event')
        events = [reg.event for reg in registrations]
        serializer = EventListSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_organized_events(self, request):
        """Get events organized by the user"""
        queryset = Event.objects.filter(organizer=request.user)
        serializer = EventListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def attendees(self, request, slug=None):
        """Get list of attendees for an event"""
        event = self.get_object()
        
        # Only allow organizer to see attendee list
        if event.organizer != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You don't have permission to view attendees."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        registrations = event.registrations.filter(status='confirmed')
        attendees = [
            {
                'username': reg.user.username,
                'checked_in': reg.checked_in,
                'registration_date': reg.registration_datetime
            }
            for reg in registrations
        ]
        return Response(attendees)

