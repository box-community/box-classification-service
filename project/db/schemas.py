"""Schemas for the database models."""

from datetime import datetime
from pydantic import BaseModel

class JwtBase(BaseModel):
    """Base class for the JWT model"""
    box_app_id: str
    access_token: str | None
    expires_on: datetime
    app_user_id: str

class JwtCreate(JwtBase):
    """Create class for the JWT model"""
    access_token_clear: str

class Jwt(JwtBase):
    """JWT model"""
    class Config:
        """Pydantic config"""
        orm_mode = True
