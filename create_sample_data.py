"""
Sample data creation script for EventHorizon

Run with: python manage.py shell < create_sample_data.py
"""

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from events.models import Category, Tag, Venue, Event
from registrations.models import Registration, Ticket

# Create categories
print("Creating categories...")
categories = [
    {'name': 'Technology', 'slug': 'technology', 'description': 'Tech events, conferences, and meetups'},
    {'name': 'Business', 'slug': 'business', 'description': 'Business networking and professional events'},
    {'name': 'Arts & Culture', 'slug': 'arts-culture', 'description': 'Art exhibitions, cultural events, and performances'},
    {'name': 'Sports & Fitness', 'slug': 'sports-fitness', 'description': 'Sports events and fitness activities'},
    {'name': 'Education', 'slug': 'education', 'description': 'Educational workshops and seminars'},
]

for cat_data in categories:
    Category.objects.get_or_create(**cat_data)

# Create tags
print("Creating tags...")
tags_list = [
    'networking', 'workshop', 'conference', 'meetup', 'webinar',
    'hackathon', 'panel-discussion', 'training', 'social', 'charity'
]

for tag_name in tags_list:
    Tag.objects.get_or_create(name=tag_name, slug=tag_name)

# Create sample user (organizer)
print("Creating sample user...")
user, created = User.objects.get_or_create(
    username='eventorganizer',
    defaults={
        'email': 'organizer@example.com',
        'first_name': 'Event',
        'last_name': 'Organizer'
    }
)
if created:
    user.set_password('password123')
    user.save()
    print(f"Created user: {user.username} (password: password123)")

# Create venues
print("Creating venues...")
venues = [
    {
        'name': 'Tech Hub Convention Center',
        'venue_type': 'physical',
        'address': '123 Tech Street',
        'city': 'San Francisco',
        'state': 'CA',
        'country': 'USA',
        'postal_code': '94102',
        'capacity': 500
    },
    {
        'name': 'Virtual Conference Platform',
        'venue_type': 'virtual',
        'online_url': 'https://meet.example.com/conference',
        'capacity': 1000
    },
    {
        'name': 'Downtown Meeting Space',
        'venue_type': 'physical',
        'address': '456 Main Ave',
        'city': 'New York',
        'state': 'NY',
        'country': 'USA',
        'postal_code': '10001',
        'capacity': 100
    }
]

for venue_data in venues:
    Venue.objects.get_or_create(name=venue_data['name'], defaults=venue_data)

# Create sample events
print("Creating sample events...")
tech_category = Category.objects.get(slug='technology')
business_category = Category.objects.get(slug='business')
tech_hub = Venue.objects.get(name='Tech Hub Convention Center')
virtual_venue = Venue.objects.get(name='Virtual Conference Platform')

now = timezone.now()

events_data = [
    {
        'title': 'AI & Machine Learning Conference 2025',
        'slug': 'ai-ml-conference-2025',
        'description': 'Join us for a comprehensive conference on the latest developments in AI and Machine Learning. Learn from industry experts and network with peers.',
        'short_description': 'Latest developments in AI and ML',
        'organizer': user,
        'category': tech_category,
        'venue': tech_hub,
        'start_datetime': now + timedelta(days=30),
        'end_datetime': now + timedelta(days=30, hours=8),
        'capacity': 200,
        'status': 'published',
        'visibility': 'public',
    },
    {
        'title': 'Startup Networking Meetup',
        'slug': 'startup-networking-meetup',
        'description': 'Connect with fellow entrepreneurs, investors, and startup enthusiasts. Share ideas and build your network.',
        'short_description': 'Network with startup community',
        'organizer': user,
        'category': business_category,
        'venue': Venue.objects.get(name='Downtown Meeting Space'),
        'start_datetime': now + timedelta(days=15),
        'end_datetime': now + timedelta(days=15, hours=3),
        'capacity': 50,
        'status': 'published',
        'visibility': 'public',
    },
    {
        'title': 'Web Development Workshop - React & Next.js',
        'slug': 'web-dev-workshop-react',
        'description': 'Hands-on workshop covering modern web development with React and Next.js. Bring your laptop!',
        'short_description': 'Learn React and Next.js',
        'organizer': user,
        'category': tech_category,
        'venue': virtual_venue,
        'start_datetime': now + timedelta(days=7),
        'end_datetime': now + timedelta(days=7, hours=4),
        'capacity': 100,
        'status': 'published',
        'visibility': 'public',
    }
]

for event_data in events_data:
    event, created = Event.objects.get_or_create(
        slug=event_data['slug'],
        defaults=event_data
    )
    if created:
        # Add tags
        if 'conference' in event.slug:
            event.tags.add(Tag.objects.get(slug='conference'))
        if 'workshop' in event.slug:
            event.tags.add(Tag.objects.get(slug='workshop'))
        if 'meetup' in event.slug:
            event.tags.add(Tag.objects.get(slug='meetup'))
        
        event.tags.add(Tag.objects.get(slug='networking'))
        
        # Create free tickets for events
        Ticket.objects.create(
            event=event,
            name='General Admission',
            description='Standard entry ticket',
            ticket_type='free',
            price=0,
            quantity_available=event.capacity,
        )

print("\nSample data created successfully!")
print("\nYou can now:")
print("1. Login to admin with username: eventorganizer, password: password123")
print("2. View events at /api/events/")
print("3. Create a superuser with: python manage.py createsuperuser")
