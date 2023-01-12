"""Models for the database."""
from sqlalchemy import Column, DateTime, String
from db.database import Base

class Jwt(Base):
    """JWT model. Caches the jwt tokens on the database"""
    __tablename__ = 'jwt'

    box_app_id = Column(String(128), primary_key=True)
    access_token_encrypted = Column(String(2048), nullable=False)
    expires_on = Column(DateTime, nullable=False)
    app_user_id = Column(String(64),unique=True)
