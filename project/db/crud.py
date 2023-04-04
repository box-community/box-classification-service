"""CRUD operations for the database"""
from sqlalchemy.orm import Session
from cryptography.fernet import InvalidToken

from app.cypto import encrypt_token, decrypt_token
from . import models, schemas


def get_jwt(db: Session, box_app_id: str, fernet_key: str) -> schemas.Jwt:
    """Get a JWT from the database using the unique app id"""

    db_jwt = db.query(models.Jwt).filter(models.Jwt.box_app_id == box_app_id).first()
    if db_jwt is None:
        return None

    jwt = jwt_db_to_jwt(db_jwt, fernet_key, False, False)

    return jwt


def save_jwt(db: Session, jwt: schemas.JwtCreate, fernet_key: str) -> schemas.Jwt:
    """Save a JWT to the database (create or update)"""
    db_jwt = get_jwt(db, jwt.box_app_id, fernet_key)

    if db_jwt is None:
        return create_jwt(db, jwt, fernet_key)

    return update_jwt(db, jwt, fernet_key)


def create_jwt(db: Session, jwt: schemas.JwtCreate, fernet_key: str) -> schemas.Jwt:
    """Create a JWT in the database"""

    db_jwt = models.Jwt()

    db_jwt.box_app_id = jwt.box_app_id
    db_jwt.access_token_encrypted = encrypt_token(jwt.access_token_clear, fernet_key)
    db_jwt.expires_on = jwt.expires_on
    db_jwt.app_user_id = jwt.app_user_id

    db.add(db_jwt)
    db.commit()
    db.refresh(db_jwt)
    return jwt_db_to_jwt(db_jwt, fernet_key, False, False)


def update_jwt(db: Session, jwt: schemas.JwtCreate, fernet_key: str):
    """Update a JWT in the database"""
    db_jwt = (
        db.query(models.Jwt).filter(models.Jwt.box_app_id == jwt.box_app_id).first()
    )

    if db_jwt is None:
        raise ValueError("JWT not found")

    # update the record
    db_jwt.access_token_encrypted = encrypt_token(jwt.access_token_clear, fernet_key)
    db_jwt.expires_on = jwt.expires_on

    # update the record on the database
    db.commit()
    db.refresh(db_jwt)

    return jwt_db_to_jwt(db_jwt, fernet_key, False, False)


def list_jwts(
    db: Session, fernet_key: str, skip: int = 0, limit: int = 100
) -> list[schemas.Jwt]:
    """List all the JWTs in the database"""
    jwts_model = db.query(models.Jwt).offset(skip).limit(limit).all()
    jwts_resutl = []
    for jwt_model in jwts_model:
        jwts_resutl.append(jwt_db_to_jwt(jwt_model, fernet_key))

    return jwts_resutl


def jwt_db_to_jwt(
    jwt_db: models.Jwt,
    fernet_key: str,
    hide_encrypted: bool = True,
    hide_clear: bool = True,
) -> schemas.Jwt:
    """Convert a JWT database record to a JWT"""
    jwt = schemas.Jwt(
        box_app_id=jwt_db.box_app_id,
        expires_on=jwt_db.expires_on,
        app_user_id=jwt_db.app_user_id,
        access_token_clear=decrypt_token(jwt_db.access_token_encrypted, fernet_key),
    )
    if hide_clear:
        jwt.access_token_clear = "********"
    if hide_encrypted:
        jwt.access_token_encrypted = "********"

    return jwt
