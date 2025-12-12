# Event Horizon API Documentation

## Authentication

The API supports token-based authentication. To obtain a token:

### Get Authentication Token

```http
POST /api/auth/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

Response:
```json
{
  "token": "your_auth_token_here"
}
```

Use this token in subsequent requests:
```http
Authorization: Token your_auth_token_here
```

## API Endpoints

### Events API

#### List Events
```http
GET /api/events/
```

Query Parameters:
- `category` - Filter by category slug
- `tag` - Filter by tag slug
- `time` - Filter by time (`upcoming` or `past`)
- `search` - Search in title and description
- `ordering` - Order by field (e.g., `start_datetime`, `-created_at`)

#### Get Event Details
```http
GET /api/events/{slug}/
```

#### Create Event
```http
POST /api/events/
Authorization: Token <your_token>
Content-Type: application/json

{
  "title": "Tech Conference 2025",
  "slug": "tech-conference-2025",
  "description": "A conference about the latest in tech",
  "short_description": "Latest tech trends",
  "start_datetime": "2025-06-01T09:00:00Z",
  "end_datetime": "2025-06-01T17:00:00Z",
  "status": "published",
  "visibility": "public"
}
```

#### Update Event
```http
PUT /api/events/{slug}/
PATCH /api/events/{slug}/
Authorization: Token <your_token>
```

#### Delete Event
```http
DELETE /api/events/{slug}/
Authorization: Token <your_token>
```

#### My Events (as attendee)
```http
GET /api/events/my_events/
Authorization: Token <your_token>
```

#### My Organized Events
```http
GET /api/events/my_organized_events/
Authorization: Token <your_token>
```

#### Get Event Attendees
```http
GET /api/events/{slug}/attendees/
Authorization: Token <your_token>
```
*Only accessible by event organizer*

### Categories API

#### List Categories
```http
GET /api/categories/
```

#### Get Category
```http
GET /api/categories/{slug}/
```

### Tags API

#### List Tags
```http
GET /api/tags/
```

#### Get Tag
```http
GET /api/tags/{slug}/
```

### Venues API

#### List Venues
```http
GET /api/venues/
```

#### Get Venue
```http
GET /api/venues/{id}/
```

### Registrations API

#### List My Registrations
```http
GET /api/registrations/
Authorization: Token <your_token>
```

#### Register for Event
```http
POST /api/registrations/register/
Authorization: Token <your_token>
Content-Type: application/json

{
  "event_id": 1,
  "notes": "Looking forward to it!",
  "dietary_requirements": "Vegetarian"
}
```

#### Cancel Registration
```http
POST /api/registrations/{id}/cancel/
Authorization: Token <your_token>
```

#### Confirm Registration (Organizer only)
```http
POST /api/registrations/{id}/confirm/
Authorization: Token <your_token>
```

### Tickets API

#### List Tickets
```http
GET /api/tickets/
```

Query Parameters:
- `event` - Filter by event ID

#### Get Ticket
```http
GET /api/tickets/{id}/
```

### User Profile API

#### Get My Profile
```http
GET /api/users/profiles/me/
Authorization: Token <your_token>
```

#### Update My Profile
```http
PUT /api/users/profiles/me/
PATCH /api/users/profiles/me/
Authorization: Token <your_token>
Content-Type: application/json

{
  "bio": "Tech enthusiast",
  "location": "San Francisco, CA",
  "website": "https://example.com"
}
```

### User Registration API

#### Register New User
```http
POST /api/users/register/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

## Response Format

### Success Response
```json
{
  "id": 1,
  "title": "Event Title",
  ...
}
```

### List Response
```json
{
  "count": 10,
  "next": "http://api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error Response
```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

## Event Model Fields

```json
{
  "id": 1,
  "title": "Event Title",
  "slug": "event-title",
  "description": "Full description",
  "short_description": "Brief summary",
  "organizer": {
    "id": 1,
    "username": "organizer",
    "first_name": "John",
    "last_name": "Doe"
  },
  "category": {
    "id": 1,
    "name": "Technology",
    "slug": "technology"
  },
  "tags": [...],
  "venue": {
    "id": 1,
    "name": "Conference Center",
    "venue_type": "physical"
  },
  "start_datetime": "2025-06-01T09:00:00Z",
  "end_datetime": "2025-06-01T17:00:00Z",
  "timezone": "UTC",
  "capacity": 100,
  "registration_required": true,
  "status": "published",
  "visibility": "public",
  "cover_image": "https://example.com/image.jpg",
  "is_upcoming": true,
  "is_past": false,
  "is_ongoing": false,
  "is_registration_open": true,
  "available_spots": 75,
  "is_full": false
}
```

## Rate Limiting

Currently no rate limiting is implemented. This will be added in future versions.

## Pagination

All list endpoints are paginated with 20 items per page by default.

Use `?page=2` to get the next page.

## Filtering and Search

Most list endpoints support:
- `?search=query` - Search in relevant fields
- `?ordering=field` - Order by field (prefix with `-` for descending)

## Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success with no response body
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Permission denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
