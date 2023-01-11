"""handle the JWT tokens for Box API"""
from datetime import datetime, timedelta
from boxsdk import Client, JWTAuth
from sqlalchemy.orm import Session

from app.config import Settings
from db import models, crud, schemas


def jwt_access_token_get(db: Session, settings: Settings) -> str:
    """
    Get the access token for the JWT assertion
    """
    # check if we have a valid access token
    jwt_rec = crud.get_jwt(db, settings.JWT_PUBLIC_KEY_ID, settings.FERNET_KEY)

    if jwt_rec_is_valid(jwt_rec):
        return jwt_rec.access_token

    # get a new access token
    auth = JWTAuth.from_settings_file(settings.jwt_path)
    auth_token = auth.authenticate_instance()
    jwt_store_token(db, settings, auth_token, None)

    return auth_token


def jwt_rec_is_valid(jwt_rec: models.Jwt) -> bool:
    """
    Check if the JWT record is valid
    """
    if jwt_rec is None:
        return False

    if jwt_rec.expires_on < datetime.now():
        return False

    return True


def jwt_store_token(
    db: Session, settings: Settings, access_token: str, refresh_token: str = None
) -> bool:
    """
    Store the access tokens for the jwt app user
    """
    seconds = int(settings.JWT_EXPIRATION_SECONDS)

    jwt_rec = schemas.JwtCreate(
        box_app_id=settings.JWT_PUBLIC_KEY_ID,
        access_token_clear=access_token,
        expires_on=datetime.now() + timedelta(seconds=seconds),
        app_user_id=0,
    )

    crud.save_jwt(db, jwt_rec, settings.FERNET_KEY)


def jwt_auth(db: Session, settings: Settings) -> JWTAuth:
    """
    Get the auth for the JWT app user
    """
    access_token = jwt_access_token_get(db, settings)

    auth = JWTAuth.from_settings_file(
        settings.jwt_path, store_tokens=jwt_store_token, access_token=access_token
    )

    return auth


def jwt_client(auth: JWTAuth) -> Client:
    """
    Get the client for the JWT app user
    """
    client = Client(auth)

    return client


def jwt_check_client(db: Session, settings: Settings) -> Client:
    """ Get a Client object for the JWT app user"""
    auth = jwt_auth(db, settings)
    client = jwt_client(auth)
    return client
