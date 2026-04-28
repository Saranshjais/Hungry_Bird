# Technology Stack

> Auto-generated on 2026-04-28

## Runtime

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11.9 | Core runtime |

## Dependencies

### Production
| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.1.1 | Web framework |
| SQLAlchemy | 2.0.41 | SQL Toolkit and ORM |
| Flask-SQLAlchemy | 3.1.1 | Flask integration for SQLAlchemy |
| Flask-Migrate | 4.1.0 | Database migrations using Alembic |
| pandas | 2.1.4 | Data manipulation and analysis |
| scikit-learn | 1.5.1 | Machine learning library |
| python-dotenv | 1.2.1 | Environment variable management |
| psycopg2-binary | 2.9.10 | PostgreSQL database adapter |
| gunicorn | 23.0.0 | WSGI HTTP Server for production |

### Development
| Package | Version | Purpose |
|---------|---------|---------|
| Werkzeug | 3.1.3 | WSGI web application library |
| Flask-Login | 0.6.3 | User session management (prepared for auth) |

## Infrastructure

| Service | Provider | Purpose |
|---------|----------|---------|
| Database | SQLite / PostgreSQL | Data storage |
| Maps | Google Maps Platform | Geospatial visualization |

## Configuration

| Variable | Purpose | Location |
|----------|---------|----------|
| `SECRET_KEY` | Flask session encryption | `.env` |
| `DATABASE_URL` | Database connection string | `.env` |
| `GOOGLE_MAPS_API_KEY` | Maps API authentication | `.env` |
