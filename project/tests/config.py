""" configuration."""

from cryptography.fernet import Fernet
from app.config import Settings


def get_settings_override():
    """Override static settings for testing."""
    fernet_key = Fernet.generate_key()
    return Settings(
        app_name = "Testing API",
        SQLALCHEMY_DATABASE_URL="sqlite:///./test.db.sqlite3",
        FERNET_KEY = fernet_key,
        jwt_path = "./.jwt.config.json",
        JWT_PUBLIC_KEY_ID = 'nztcgflw',
        JWT_EXPIRATION_SECONDS = 3300,
    )
