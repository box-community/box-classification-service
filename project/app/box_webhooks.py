""" handle box webhooks from box exvents"""
from boxsdk import BoxAPIException
from sqlalchemy.orm import Session

from app.config import Settings
from app.box_jwt import jwt_check_client

def webhook_signature_check(
    webhook_id: str,
    body: bytes,
    header: dict,
    db: Session,
    settings: Settings,
) -> bool:
    """check the signature of the webhook request"""

    client = jwt_check_client(db, settings)
    webhook = client.webhook(webhook_id)
    
    key_a = settings.WH_KEY_A
    key_b = settings.WH_KEY_B

    return webhook.validate_message(body, header, key_a, key_b)

def classify_file(file_id: str, db: Session, settings: Settings):
    """classify a file"""

    try:
        client = jwt_check_client(db, settings)
        file = client.file(file_id)
        file_class = file.get_classification()
        if file_class is None or file_class != "Sensitive":
            print("Classifying file")
            file_class = file.set_classification("Sensitive")
        # file_class = file.set_classification("Sensitive")
        print(file_class)
    except BoxAPIException as exc:
        pass

    
