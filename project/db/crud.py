"""CRUD operations for the database"""
from sqlalchemy.orm import Session

from app.cypto import encrypt_token, decrypt_token
from . import models,schemas

def get_jwt(db: Session, box_app_id: str, fernet_key: str):
    """Get a JWT from the database using the unique app id"""

    db_jwt = db.query(models.Jwt).filter(models.Jwt.box_app_id == box_app_id).first()
    if db_jwt is not None:
        if db_jwt.access_token is not None:
            db_jwt.access_token = decrypt_token(db_jwt.access_token, fernet_key)
    return db_jwt

def save_jwt(db: Session, jwt: schemas.JwtCreate, fernet_key: str):
    """Save a JWT to the database (create or update)"""
    db_jwt = get_jwt(db, jwt.box_app_id, fernet_key)

    if db_jwt is None:
        return create_jwt(db, jwt, fernet_key)

    return update_jwt(db, jwt, fernet_key)

def create_jwt(db: Session, jwt: schemas.JwtCreate, fernet_key: str):
    """Create a JWT in the database"""

    db_jwt = models.Jwt()

    db_jwt.box_app_id = jwt.box_app_id
    db_jwt.access_token = encrypt_token(jwt.access_token_clear, fernet_key)
    db_jwt.expires_on = jwt.expires_on
    db_jwt.app_user_id = jwt.app_user_id

    db.add(db_jwt)
    db.commit()
    db.refresh(db_jwt)
    return db_jwt

def update_jwt(db: Session, jwt: schemas.JwtCreate, fernet_key: str):
    """Update a JWT in the database"""
    db_jwt = get_jwt(db, jwt.box_app_id, fernet_key)

    if db_jwt is None:
        raise ValueError("JWT not found")

    db_jwt.box_app_id = jwt.box_app_id
    db_jwt.access_token = encrypt_token(jwt.access_token,fernet_key)
    db_jwt.expires_on = jwt.expires_on
    db_jwt.app_user_id = jwt.app_user_id

    db.commit()
    db.refresh(db_jwt)
    return db_jwt

def list_jwts(db: Session, skip: int = 0, limit: int = 100):
    """List all the JWTs in the database"""
    return db.query(models.Jwt).offset(skip).limit(limit).all()
