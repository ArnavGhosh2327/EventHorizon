from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator


class Category(models.Model):
    """Event categories (e.g., Tech, Business, Arts, Sports)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tags for events (e.g., networking, workshop, conference)"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Venue(models.Model):
    """Physical or virtual venue for events"""
    VENUE_TYPE_CHOICES = [
        ('physical', 'Physical Location'),
        ('virtual', 'Virtual/Online'),
        ('hybrid', 'Hybrid'),
    ]

    name = models.CharField(max_length=200)
    venue_type = models.CharField(max_length=20, choices=VENUE_TYPE_CHOICES, default='physical')
    address = models.TextField(blank=True, help_text="Full address for physical venues")
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    online_url = models.URLField(blank=True, help_text="URL for virtual events")
    capacity = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_venue_type_display()})"


class Event(models.Model):
    """Main event model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('unlisted', 'Unlisted'),
    ]

    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    # Organizer
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    
    # Categorization
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    tags = models.ManyToManyField(Tag, blank=True, related_name='events')
    
    # Venue
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    
    # Timing
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Capacity and Registration
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Leave blank for unlimited")
    registration_required = models.BooleanField(default=True)
    registration_open_datetime = models.DateTimeField(null=True, blank=True)
    registration_close_datetime = models.DateTimeField(null=True, blank=True)
    
    # Status and Visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    
    # Media
    cover_image = models.URLField(blank=True, help_text="URL to event cover image")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_datetime']
        indexes = [
            models.Index(fields=['-start_datetime']),
            models.Index(fields=['status', 'visibility']),
        ]

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        """Check if event is in the future"""
        return self.start_datetime > timezone.now()

    @property
    def is_past(self):
        """Check if event has ended"""
        return self.end_datetime < timezone.now()

    @property
    def is_ongoing(self):
        """Check if event is currently happening"""
        now = timezone.now()
        return self.start_datetime <= now <= self.end_datetime

    @property
    def is_registration_open(self):
        """Check if registration is currently open"""
        if not self.registration_required:
            return False
        
        now = timezone.now()
        
        if self.registration_open_datetime and now < self.registration_open_datetime:
            return False
        
        if self.registration_close_datetime and now > self.registration_close_datetime:
            return False
        
        return True

    @property
    def available_spots(self):
        """Calculate remaining spots"""
        if not self.capacity:
            return None
        
        confirmed_count = self.registrations.filter(status='confirmed').count()
        return max(0, self.capacity - confirmed_count)

    @property
    def is_full(self):
        """Check if event is at capacity"""
        if not self.capacity:
            return False
        return self.available_spots == 0
