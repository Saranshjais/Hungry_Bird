import os

class Config:
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///hungrybird.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API Keys
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

    # Pagination / limits (future-proofing)
    ITEMS_PER_PAGE = 12

    # Deployment mode
    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = ENV == "development"
