"""Configuration settings for the app."""

from pydantic import BaseSettings

class Settings(BaseSettings):
    """Configuration settings class for the app."""
    app_name: str = "Awesome API"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./db.sqlite3"
    FERNET_KEY: str
    jwt_path: str = "./.jwt.config.json"

    class Config:
        """ environment variables to read from """
        env_file = ".env"

        