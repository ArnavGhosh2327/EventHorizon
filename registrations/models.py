from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from events.models import Event


class Registration(models.Model):
    """Event registration/RSVP model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('waitlist', 'Waitlist'),
        ('attended', 'Attended'),
    ]

    # Core fields
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Registration details
    registration_datetime = models.DateTimeField(auto_now_add=True)
    confirmation_datetime = models.DateTimeField(null=True, blank=True)
    cancellation_datetime = models.DateTimeField(null=True, blank=True)
    
    # Additional information
    notes = models.TextField(blank=True, help_text="Notes from attendee")
    dietary_requirements = models.CharField(max_length=200, blank=True)
    special_requests = models.TextField(blank=True)
    
    # Attendance tracking
    checked_in = models.BooleanField(default=False)
    check_in_datetime = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['event', 'user']
        ordering = ['-registration_datetime']
        indexes = [
            models.Index(fields=['event', 'status']),
            models.Index(fields=['user', 'status']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.get_status_display()})"

    def confirm(self):
        """Confirm the registration"""
        self.status = 'confirmed'
        self.confirmation_datetime = timezone.now()
        self.save()

    def cancel(self):
        """Cancel the registration"""
        self.status = 'cancelled'
        self.cancellation_datetime = timezone.now()
        self.save()

    def check_in(self):
        """Check in the attendee"""
        self.checked_in = True
        self.check_in_datetime = timezone.now()
        if self.status == 'confirmed':
            self.status = 'attended'
        self.save()


class Ticket(models.Model):
    """Ticket types for events (free or paid)"""
    TICKET_TYPE_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
        ('donation', 'Donation'),
    ]

    # Core fields
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='tickets')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPE_CHOICES, default='free')
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    
    # Availability
    quantity_available = models.PositiveIntegerField(null=True, blank=True, help_text="Leave blank for unlimited")
    quantity_sold = models.PositiveIntegerField(default=0)
    
    # Sale period
    sale_start_datetime = models.DateTimeField(null=True, blank=True)
    sale_end_datetime = models.DateTimeField(null=True, blank=True)
    
    # Settings
    min_per_order = models.PositiveIntegerField(default=1)
    max_per_order = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['price', 'name']

    def __str__(self):
        return f"{self.name} - {self.event.title}"

    @property
    def is_available(self):
        """Check if tickets are available for purchase"""
        if not self.is_active:
            return False
        
        now = timezone.now()
        
        if self.sale_start_datetime and now < self.sale_start_datetime:
            return False
        
        if self.sale_end_datetime and now > self.sale_end_datetime:
            return False
        
        if self.quantity_available and self.quantity_sold >= self.quantity_available:
            return False
        
        return True

    @property
    def remaining_quantity(self):
        """Get remaining ticket quantity"""
        if not self.quantity_available:
            return None
        return max(0, self.quantity_available - self.quantity_sold)
