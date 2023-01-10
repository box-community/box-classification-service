from datetime import datetime, timedelta
from boxsdk import Client, JWTAuth
from sqlalchemy.orm import Session

from app.cypto import decrypt_token, encrypt_token
from app.config import Settings
from db import models, crud, schemas

def jwt_access_token_get(db:Session, settings:Settings) -> str:
    """
    Get the access token for the JWT assertion
    """
    # check if we have a valid access token
    # jwt_rec = Jwt.query.filter_by(box_app_id=Config.JWT_PUBLIC_KEY_ID).first()
    jwt_rec = crud.get_jwt(db,"nztcgflw", settings)
        
    if jwt_rec_is_valid(jwt_rec):
        return decrypt_token(jwt_rec.access_token, settings)

    # get a new access token
    auth = JWTAuth.from_settings_file(settings.jwt_path, store_tokens=jwt_store_token)
    return auth.authenticate_instance()


def jwt_rec_is_valid(jwt_rec: models.Jwt) -> bool:
    """
    Check if the JWT record is valid
    """
    if jwt_rec is None:
        return False

    if jwt_rec.expires_on < datetime.now():
        return False

    return True

def jwt_store_token(access_token: str, refresh_token: str = None) -> bool:
    return True

# def jwt_store_token(access_token: str, refresh_token: str = None) -> bool:
#     """
#     Store the access tokens for the jwt app user
#     """
#     print(f"Storing access token: {access_token}")
#     jwt_rec = Jwt.query.filter_by(box_app_id=Config.JWT_PUBLIC_KEY_ID).first()
#     seconds = int(Config.JWT_EXPIRATION_SECONDS)

#     if jwt_rec == None:

#         jwt_new = Jwt(
#             box_app_id=Config.JWT_PUBLIC_KEY_ID,
#             access_token=encrypt_token(access_token),
#             expires_on=datetime.now() + timedelta(seconds=seconds),
#             app_user_id=0,
#             box_demo_folder_id=0,
#         )
#         db.session.add(jwt_new)
#         db.session.commit()
#     else:
#         jwt_rec.box_app_id = Config.JWT_PUBLIC_KEY_ID
#         jwt_rec.access_token = encrypt_token(access_token)
#         jwt_rec.expires_on = datetime.now() + timedelta(seconds=seconds)
#         db.session.commit()


# @fl_cache.cached(key_prefix="jwt_downscoped_access_token_get")
# def jwt_downscoped_access_token_get() -> str:
#     """
#     Get the downscoped access token for the jwt app user
#     """

#     scope = [
#         "base_explorer",
#         "item_preview",  #'item_download', 'item_rename', 'item_share', 'item_delete',
#         "base_picker",  #'item_upload', # , 'item_share'
#         #'base_preview', 'annotation_edit', 'annotation_view_all', 'annotation_view_self', #, 'item_download'
#         #'base_sidebar', 'item_comment', #'item_task', # , 'item_rename', 'item_upload'
#         "base_upload",
#     ]
#     client = jwt_check_client()
#     downscoped_token = client.downscope_token(scopes=scope)
#     return downscoped_token.access_token


def jwt_auth(db:Session, settings: Settings) -> JWTAuth:
    """
    Get the auth for the JWT app user
    """
    access_token = jwt_access_token_get(db, settings)

    auth = JWTAuth.from_settings_file(
        settings.jwt_path, store_tokens = jwt_store_token,
        access_token=access_token
    )

    return auth


def jwt_client(auth: JWTAuth) -> Client:
    """
    Get the client for the JWT app user
    """
    client = Client(auth)

    return client


def jwt_check_client(settings: Settings) -> Client:

    auth = jwt_auth(settings)
    client = jwt_client(auth)
    return client
