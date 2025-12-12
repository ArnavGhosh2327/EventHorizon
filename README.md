# Event Horizon 🌌

A modern event management platform inspired by Luma, built with Django and Django REST Framework.

## Overview

Event Horizon is a comprehensive event management solution that allows users to create, discover, and manage events. Whether you're hosting a small meetup or a large conference, Event Horizon provides all the tools you need.

## Features

### Current Features
- 🔐 OAuth2 authentication (GitHub, Google)
- 🎫 Event creation and management
- 👥 User profiles and authentication
- 📝 Event registration and RSVP system
- 🔍 Event search and filtering
- 📧 Email notifications

### Planned Features
- 📅 Calendar integration (iCal export)
- 📊 Event analytics dashboard
- 🖼️ Event image uploads
- 🎟️ Ticketing system
- 💬 Event comments and discussions
- 🌐 Multi-language support

## Tech Stack

- **Backend**: Django 6.0, Django REST Framework
- **Authentication**: Django Allauth, OAuth2 Provider
- **Database**: SQLite (development), PostgreSQL (production ready)
- **API**: RESTful API with token authentication

## Prerequisites

- Python 3.12+
- pip or uv package manager

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/ArnavGhosh2327/EventHorizon.git
cd EventHorizon
```

### 2. Set up environment

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
- Set `SECRET_KEY` to a secure random string
- Set `DEBUG=True` for development
- Configure OAuth credentials if needed

### 3. Install dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the application.

## Project Structure

```
EventHorizon/
├── EventHorizon/          # Main project settings
│   ├── settings.py        # Django settings
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py           # WSGI application
├── events/               # Events app (to be created)
├── users/                # Users app (to be created)
├── registrations/        # Registration app (to be created)
├── manage.py             # Django management script
└── pyproject.toml        # Project dependencies
```

## API Endpoints

Once fully implemented, the API will include:

- `GET /api/events/` - List all events
- `POST /api/events/` - Create a new event
- `GET /api/events/{id}/` - Get event details
- `PUT /api/events/{id}/` - Update an event
- `DELETE /api/events/{id}/` - Delete an event
- `POST /api/events/{id}/register/` - Register for an event
- `GET /api/users/profile/` - Get user profile
- `GET /api/registrations/` - List user's registrations

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration
EMAIL2CONSOLE=True

# Database (optional, defaults to SQLite)
# DATABASE_URL=postgresql://user:password@localhost/eventhorizon

# OAuth (optional)
# GITHUB_CLIENT_ID=your-github-client-id
# GITHUB_CLIENT_SECRET=your-github-client-secret
# GOOGLE_CLIENT_ID=your-google-client-id
# GOOGLE_CLIENT_SECRET=your-google-client-secret

# Site Customization
DJANGO_SITE_HEADER=Event Horizon
DJANGO_SITE_TITLE=Event Horizon
DJANGO_INDEX_TITLE=Event Horizon Admin
```

## Development

### Running Tests

```bash
python manage.py test
```

### Code Style

This project follows PEP 8 style guidelines. Format your code with:

```bash
black .
flake8 .
```

### Making Migrations

After modifying models:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Roadmap

### Version 0.1 (Current)
- ✅ Basic Django setup
- ✅ OAuth authentication
- 🔄 Core models
- 🔄 REST API

### Version 0.2 (Next)
- Event CRUD operations
- User registration system
- Basic frontend

### Version 1.0 (Future)
- Full-featured event platform
- Advanced search and filtering
- Analytics dashboard
- Mobile responsive design

## Support

For support, please open an issue in the GitHub repository.

## Acknowledgments

- Inspired by [Luma](https://lu.ma/)
- Built with Django and Django REST Framework

