""" Test JWT boxsdk auth"""

from datetime import timedelta
from sqlalchemy.orm import sessionmaker
from app.box_jwt import jwt_auth, jwt_client, jwt_check_client
from db import crud
from db.crud import get_jwt

from tests.config import get_settings_override

from db.database import create_db_engine
from db import models

# create a new database engine if not exists yet
settings = get_settings_override()
engine = create_db_engine(settings)

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_jwt_auth():
    """should return a valid access token (JWTAuth object)"""
    db = SessionLocal()
    auth = jwt_auth(db, settings)

    assert auth.access_token is not None
    assert auth.access_token != ""


def test_jwt_client():
    """should return a valid client (Client object)"""
    db = SessionLocal()
    auth = jwt_auth(db, settings)

    client = jwt_client(auth)
    assert client is not None

    service_account = client.user().get()
    assert service_account is not None

    # should be able to reuse the auth token
    client = jwt_check_client(db, settings)
    assert client is not None

    service_account = client.user().get()
    assert service_account is not None


def test_jwt_client_expired():
    """should return a valid client (Client object)"""
    db = SessionLocal()
    auth = jwt_auth(db, settings)

    client = jwt_client(auth)
    assert client is not None

    service_account = client.user().get()
    assert service_account is not None

    # force the token to expire
    db_jwt = get_jwt(db, settings.JWT_PUBLIC_KEY_ID, settings.FERNET_KEY)
    db_jwt.expires_on = db_jwt.expires_on - timedelta(hours=24)
    crud.save_jwt(db, db_jwt, settings.FERNET_KEY)

    # should be able to reuse the auth token
    client = jwt_check_client(db, settings)
    assert client is not None

    service_account = client.user().get()
    assert service_account is not None
