""" Tests for configuration settings of application and test cases"""
from tests.config import get_settings_override
from app.main import get_settings


def test_config_read():
    """should return NON overridden settings"""
    settings = get_settings()

    assert settings.app_name == "Awesome API"
    assert settings.SQLALCHEMY_DATABASE_URL == "sqlite:///./db.sqlite3"
    assert settings.FERNET_KEY is not None
    assert settings.jwt_path == "./.jwt.config.json"

def test_config_override():
    """should return overridden settings"""
    settings = get_settings_override()

    assert settings.app_name == "Testing API"
    assert settings.SQLALCHEMY_DATABASE_URL == "sqlite:///./test.db.sqlite3"
    assert settings.FERNET_KEY is not None
    assert settings.jwt_path == "./.jwt.config.json"
