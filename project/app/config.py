"""Configuration settings for the app."""

from pydantic import BaseSettings, BaseModel


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
    CLASSIFICATION: str

    class Config:
        """environment variables to read from"""

        env_file = ".env"


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "Classification Service"
    # LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_FORMAT: str = "%(levelprefix)s Classification Service -> %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }
