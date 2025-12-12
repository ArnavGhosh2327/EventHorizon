from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Registration, Ticket
from .serializers import (
    RegistrationSerializer, RegistrationCreateSerializer, TicketSerializer
)
from events.models import Event


class RegistrationViewSet(viewsets.ModelViewSet):
    """API endpoint for event registrations"""
    queryset = Registration.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.action == 'create':
            return RegistrationCreateSerializer
        return RegistrationSerializer
    
    def get_queryset(self):
        """Users can only see their own registrations"""
        return Registration.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Create registration for the current user"""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register for an event"""
        event_id = request.data.get('event_id')
        if not event_id:
            return Response(
                {"error": "event_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        event = get_object_or_404(Event, id=event_id)
        
        # Check if already registered
        existing = Registration.objects.filter(
            user=request.user, 
            event=event
        ).first()
        
        if existing:
            return Response(
                {"error": "You are already registered for this event"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create registration
        serializer = RegistrationCreateSerializer(data={'event': event.id, **request.data})
        serializer.is_valid(raise_exception=True)
        registration = serializer.save(user=request.user)
        
        return Response(
            RegistrationSerializer(registration).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a registration"""
        registration = self.get_object()
        
        if registration.status == 'cancelled':
            return Response(
                {"error": "Registration is already cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        registration.cancel()
        return Response(RegistrationSerializer(registration).data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a registration (for organizers)"""
        registration = self.get_object()
        
        # Only event organizer can confirm
        if registration.event.organizer != request.user and not request.user.is_staff:
            return Response(
                {"error": "Only the event organizer can confirm registrations"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        registration.confirm()
        return Response(RegistrationSerializer(registration).data)


class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for event tickets"""
    queryset = Ticket.objects.filter(is_active=True)
    serializer_class = TicketSerializer
    
    def get_queryset(self):
        """Filter tickets by event if specified"""
        queryset = super().get_queryset()
        event_id = self.request.query_params.get('event', None)
        if event_id:
            queryset = queryset.filter(event_id=event_id)
        return queryset

