"""Main module of the application."""

from functools import lru_cache

from fastapi import Depends, FastAPI, Request, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from boxsdk import BoxAPIException

from app import config
from app import box_jwt
from app import box_webhooks

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


@app.get("/box/info")
async def info(request: Request):
    """
    Get the info for the app.
    Returns the settings for the app.
    (remember not to expose secrets like the FERNET_KEY)
    """
    configurations = config.Settings().dict()
    configurations["FERNET_KEY"] = "****"
    configurations["root_path"] = request.scope.get("root_path")
    return configurations


@app.get("/box/info/jwt", response_model=list[schemas.Jwt])
def info_jwt(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """list all jwt accounts in current database"""
    jwts = crud.list_jwts(db, skip=skip, limit=limit)
    for jwt in jwts:
        jwt.access_token = "****"
    return jwts


@app.get("/box/info/me")
async def info_me(
    settings: config.Settings = Depends(get_settings), db: Session = Depends(get_db)
):
    """
    Returns current user info
    """
    client = box_jwt.jwt_check_client(db, settings)
    me = client.user()
    me = me.get()
    # print(me.name)
    return {"name": me.name, "email": me.login, "id": me.id}


@app.post("/box/classify")
async def classify(
    request: Request,
    settings: config.Settings = Depends(get_settings),
    db: Session = Depends(get_db),
):
    """
    Classify endpoint
    """
    body_json = await request.json()

    # check if the webhook id is the expected one
    # created on the console
    webhook_id = body_json["webhook"]["id"]

    if webhook_id != settings.WH_ID:
        raise HTTPException(status_code=404, detail="Unexpected webhook id")

    # should also check for replay attacks
    # TBD

    body = await request.body()

    # check for valid signatures
    try:
        is_valid = box_webhooks.webhook_signature_check(
            webhook_id, body, request.headers, db, settings
        )
    except BoxAPIException as exc:
        raise HTTPException(status_code=404, detail="Webhook not found") from exc

    if not is_valid:
        raise HTTPException(status_code=404, detail="Invalid signature")

    return {"ok": True}
