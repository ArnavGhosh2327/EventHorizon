from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile for additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Profile Information
    bio = models.TextField(max_length=500, blank=True)
    avatar_url = models.URLField(blank=True, help_text="URL to user's avatar image")
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    
    # Social Links
    twitter_handle = models.CharField(max_length=50, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Preferences
    receive_event_notifications = models.BooleanField(default=True)
    receive_marketing_emails = models.BooleanField(default=False)
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Profile of {self.user.username}"

    @property
    def full_name(self):
        """Get user's full name"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a profile when a new user is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Automatically save profile when user is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
