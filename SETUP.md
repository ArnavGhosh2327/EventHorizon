# Quick Setup Guide for Event Horizon

## Prerequisites
- Python 3.12+
- pip or uv package manager
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ArnavGhosh2327/EventHorizon.git
cd EventHorizon
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your settings (optional for development)
```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
# Follow prompts to create admin user
```

### 7. Load Sample Data (Optional)
```bash
python manage.py shell < create_sample_data.py
```

This creates:
- Sample categories (Technology, Business, Arts & Culture, Sports & Fitness, Education)
- Sample tags (networking, workshop, conference, etc.)
- Sample venues (physical and virtual)
- Sample events
- A sample organizer user (username: `eventorganizer`, password: `password123`)

### 8. Run the Development Server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

## Quick Testing

### Admin Interface
Visit http://127.0.0.1:8000/admin/ and login with your superuser credentials.

### API Endpoints
- Events List: http://127.0.0.1:8000/api/events/
- Categories: http://127.0.0.1:8000/api/categories/
- Tags: http://127.0.0.1:8000/api/tags/
- Venues: http://127.0.0.1:8000/api/venues/

### Get API Token
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### Use API Token
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
  http://127.0.0.1:8000/api/events/
```

## Docker Setup (Alternative)

### Using Docker Compose
```bash
docker-compose up
```

This will:
- Start a PostgreSQL database
- Start the Django application
- Expose the app on http://localhost:8000

### Initial Setup with Docker
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Load sample data
docker-compose exec web python manage.py shell < create_sample_data.py
```

## Common Commands

### Create a new Django app
```bash
python manage.py startapp app_name
```

### Make migrations after model changes
```bash
python manage.py makemigrations
python manage.py migrate
```

### Run tests
```bash
python manage.py test
```

### Collect static files (for production)
```bash
python manage.py collectstatic
```

## Troubleshooting

### Port already in use
If port 8000 is already in use:
```bash
python manage.py runserver 8001
```

### Database issues
Delete db.sqlite3 and re-run migrations:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Import errors
Ensure virtual environment is activated and dependencies are installed:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

1. Read the [API Documentation](API.md) to understand available endpoints
2. Check [CONTRIBUTING.md](CONTRIBUTING.md) if you want to contribute
3. Explore the Django admin to manage events, categories, and users
4. Start building your frontend or use the REST API directly

## Support

For issues or questions, please open an issue on GitHub.
