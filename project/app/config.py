"""Configuration settings for the app."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Configuration settings class for the app."""

    app_name: str = "Box Classification Service"
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./db.sqlite3"
    FERNET_KEY: str
    jwt_path: str = "./.jwt.config.json"
    JWT_PUBLIC_KEY_ID: str
    JWT_EXPIRATION_SECONDS: int = 3300
    WH_KEY_A: str
    WH_KEY_B: str
    WH_ID: str

    class Config:
        """environment variables to read from"""

        env_file = ".env"
