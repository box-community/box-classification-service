"""test databse models and cruds"""

from datetime import datetime, timedelta
import random
import string
from sqlalchemy.orm import sessionmaker

from tests.config import get_settings_override

from app.cypto import decrypt_token

from db.database import create_db_engine
from db import crud, models, schemas


# create a new database engine if not exists yet
settings = get_settings_override()
engine = create_db_engine(settings)

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_create_jwt():
    """should create a new jwt in the database"""

    db = SessionLocal()

    box_app_id = "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(20)
    )
    app_user_id = "USER_ID:" + box_app_id

    expires_on = datetime.now() + timedelta(hours=1)

    jwt = schemas.JwtCreate(
        box_app_id=box_app_id,
        access_token_clear="FAKE_ACCESS_TOKEN",
        expires_on=expires_on,
        app_user_id=app_user_id,
    )

    db_jwt = crud.save_jwt(db, jwt, settings.FERNET_KEY)

    assert db_jwt.box_app_id == jwt.box_app_id
    assert db_jwt.expires_on == jwt.expires_on
    assert db_jwt.app_user_id == jwt.app_user_id

    assert db_jwt.access_token_encrypted is not None
    assert db_jwt.access_token_encrypted != jwt.access_token_clear
    # assert db_jwt.access_token == encrypt_token(jwt.access_token_clear, settings)
    assert decrypt_token(db_jwt.access_token_encrypted, settings.FERNET_KEY) == jwt.access_token_clear
