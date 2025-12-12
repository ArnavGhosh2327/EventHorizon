# User Guide - Event Horizon

## Quick Start Guide

This guide shows you how to use Event Horizon's core Luma-like functionality.

## Table of Contents
1. [For Event Organizers](#for-event-organizers)
2. [For Event Attendees](#for-event-attendees)
3. [Admin Panel Guide](#admin-panel-guide)

---

## For Event Organizers

### Step 1: Create an Account

**Via API:**
```bash
POST /api/users/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123"
}
```

**Via Admin Panel:**
Go to http://localhost:8000/admin/ and create a user account.

### Step 2: Get Your Authentication Token

```bash
POST /api/auth/token/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepass123"
}

# Response:
{
  "token": "abc123xyz789..."
}
```

Save this token - you'll use it in all future requests.

### Step 3: Create Your First Event

```bash
POST /api/events/
Authorization: Token abc123xyz789...
Content-Type: application/json

{
  "title": "Community Coding Workshop",
  "slug": "community-coding-workshop",
  "description": "A beginner-friendly workshop on web development. Bring your laptop!",
  "short_description": "Learn web development basics",
  "start_datetime": "2025-06-20T14:00:00Z",
  "end_datetime": "2025-06-20T17:00:00Z",
  "capacity": 30,
  "registration_required": true,
  "status": "published",
  "visibility": "public"
}
```

**What this does:**
- Creates a public event that anyone can find
- Sets capacity to 30 people
- Makes it discoverable in event listings
- Opens registration automatically

### Step 4: View Who's Registered

```bash
GET /api/events/community-coding-workshop/attendees/
Authorization: Token abc123xyz789...
```

**Response:**
```json
[
  {
    "username": "alice",
    "checked_in": false,
    "registration_date": "2025-06-01T10:30:00Z"
  },
  {
    "username": "bob",
    "checked_in": false,
    "registration_date": "2025-06-01T11:15:00Z"
  }
]
```

### Step 5: Manage Registrations

**Via Admin Panel** (recommended):
1. Go to http://localhost:8000/admin/
2. Click "Registrations"
3. Select registrations you want to manage
4. Use bulk actions:
   - "Confirm selected registrations"
   - "Check in selected attendees"
   - "Cancel selected registrations"

**Via API:**
```bash
# Confirm a registration
POST /api/registrations/{registration_id}/confirm/
Authorization: Token abc123xyz789...
```

### Step 6: Track Your Events

```bash
# See all events you've created
GET /api/events/my_organized_events/
Authorization: Token abc123xyz789...
```

---

## For Event Attendees

### Step 1: Browse Events

**No login required!**

```bash
# See all upcoming events
GET /api/events/?time=upcoming

# Search for tech events
GET /api/events/?search=tech

# Filter by category
GET /api/events/?category=technology
```

**Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "title": "Community Coding Workshop",
      "short_description": "Learn web development basics",
      "start_datetime": "2025-06-20T14:00:00Z",
      "capacity": 30,
      "available_spots": 15,
      "is_full": false,
      "organizer": {
        "username": "johndoe",
        "first_name": "John",
        "last_name": "Doe"
      }
    }
  ]
}
```

### Step 2: Register for an Event

**First, create an account and get your token** (see organizer steps 1-2)

Then register:

```bash
POST /api/registrations/register/
Authorization: Token YOUR_TOKEN
Content-Type: application/json

{
  "event_id": 1,
  "dietary_requirements": "Vegetarian",
  "notes": "Excited to attend!"
}
```

**Response:**
```json
{
  "id": 123,
  "status": "confirmed",
  "registration_datetime": "2025-06-01T12:00:00Z",
  "event_details": {
    "title": "Community Coding Workshop",
    "start_datetime": "2025-06-20T14:00:00Z"
  }
}
```

### Step 3: View Your Events

```bash
# See all events you're registered for
GET /api/events/my_events/
Authorization: Token YOUR_TOKEN
```

### Step 4: Cancel a Registration

```bash
POST /api/registrations/{registration_id}/cancel/
Authorization: Token YOUR_TOKEN
```

---

## Admin Panel Guide

The admin panel at http://localhost:8000/admin/ provides a user-friendly interface for managing everything.

### For Organizers

**Managing Your Events:**
1. Log in to admin panel
2. Click "Events" to see all your events
3. Click on an event to:
   - Edit details
   - Change status (draft/published/cancelled)
   - Set capacity limits
   - Add venue information

**Managing Registrations:**
1. Click "Registrations"
2. Filter by your event
3. See attendee details:
   - Name and email
   - Registration status
   - Dietary requirements
   - Check-in status
4. Use bulk actions:
   - Confirm pending registrations
   - Check-in attendees at the door
   - Send to waitlist if event is full

**Checking In Attendees:**
1. On event day, open admin panel on a tablet/laptop
2. Go to Registrations
3. Filter by your event and "confirmed" status
4. Select attendees as they arrive
5. Click "Check in selected attendees"
6. Attendees are marked as "attended"

### For Attendees

**Update Your Profile:**
1. Log in to admin panel
2. Click on your username (top right)
3. Edit your profile:
   - Add bio and avatar
   - Set location and timezone
   - Add social media links
   - Configure email preferences

**View Your Registrations:**
1. Click "Registrations"
2. Filter by your username
3. See all events you're registered for

---

## Common Scenarios

### Scenario 1: Organizing a Free Community Meetup

```bash
# 1. Create the event
POST /api/events/
{
  "title": "Monthly Python Meetup",
  "slug": "monthly-python-meetup-june",
  "description": "Join us for networking, lightning talks, and pizza!",
  "start_datetime": "2025-06-25T18:00:00Z",
  "end_datetime": "2025-06-25T21:00:00Z",
  "capacity": 50,
  "status": "published"
}

# 2. Share the event URL with your community
# People can register at: /api/events/monthly-python-meetup-june/

# 3. On event day, check people in via admin panel
```

### Scenario 2: Finding and Attending a Workshop

```bash
# 1. Browse upcoming tech workshops
GET /api/events/?category=technology&search=workshop&time=upcoming

# 2. Pick one and register
POST /api/registrations/register/
{
  "event_id": 5,
  "notes": "Bringing my own laptop"
}

# 3. Get confirmation
# You'll see "confirmed" status in response

# 4. Check your events anytime
GET /api/events/my_events/
```

### Scenario 3: Managing a Sold-Out Event

When your event reaches capacity:

1. New registrations automatically go to "waitlist" status
2. If someone cancels, you can manually promote waitlist attendees
3. Via admin:
   - Go to Registrations
   - Filter by waitlist status
   - Select person to promote
   - Change status to "confirmed"

---

## Tips & Best Practices

### For Organizers

✅ **Set realistic capacity** - Consider venue size and resources
✅ **Publish early** - Give people time to register
✅ **Use categories and tags** - Help people discover your event
✅ **Add venue details** - Include address or online meeting link
✅ **Check in attendees** - Track who actually showed up
✅ **Review dietary requirements** - Plan food accordingly

### For Attendees

✅ **Register early** - Popular events fill up fast
✅ **Cancel if you can't make it** - Help others on the waitlist
✅ **Add notes** - Let organizers know special requirements
✅ **Keep your profile updated** - Organizers can see your info

---

## Need Help?

- **API Issues**: Check API.md for detailed endpoint documentation
- **Setup Issues**: See SETUP.md for installation help
- **Feature Requests**: Open an issue on GitHub

## What's Next?

Currently, Event Horizon provides the core Luma functionality via API and admin panel. 

**Coming Soon:**
- Web UI for browsing and registering for events
- Email notifications for confirmations and reminders
- Calendar integration (iCal downloads)
- Event analytics for organizers
