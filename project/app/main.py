"""Main module of the application."""

from functools import lru_cache

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session,sessionmaker

from app import config

from db.database import create_db_engine
from db import models, schemas, crud

@lru_cache()
def get_settings():
    """Get the settings for the app."""
    return config.Settings()

engine = create_db_engine(get_settings())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    """Get the database session for the request as a dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/info")
async def info(settings: config.Settings = Depends(get_settings)):
    """Get the info for the app."""
    return {
        "app_name": settings.app_name,
        "SQLALCHEMY_DATABASE_URL": settings.SQLALCHEMY_DATABASE_URL,
    }

@app.get("/jwts/", response_model=list[schemas.Jwt])
def list_jwts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """list all jwts in current database"""
    jwts = crud.list_jwts(db, skip=skip, limit=limit)
    return jwts
