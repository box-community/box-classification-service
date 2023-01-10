""" Test JWT boxsdk auth"""

from sqlalchemy.orm import sessionmaker
from app.box_jwt import jwt_auth     

from tests.config import get_settings_override

from db.database import create_db_engine
from db import crud, models, schemas

   

# create a new database engine if not exists yet
settings = get_settings_override()
engine = create_db_engine(settings)

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_jwt_auth():
    """should return a valid access token (JWTAuth object)"""
    db = SessionLocal()
    jwt = jwt_auth(db, settings)

    print(jwt.access_token)
    assert jwt.access_token is not None
    assert jwt.access_token != ""
