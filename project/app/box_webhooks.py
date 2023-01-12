""" handle box webhooks from box exvents"""
from functools import lru_cache
from sqlalchemy.orm import Session

from app.config import Settings
from app.box_jwt import jwt_check_client


@lru_cache()
def webhook_check(webhook_id, client):
    """check if webhook exists for this application"""

    webhook = client.webhook(webhook_id)
    # this raises an error if the webhook does not exist
    # or is not accessible on this security context
    webhook.get()
    return webhook

def webhook_signature_check(
    webhook_id: str,
    body: bytes,
    header: dict,
    db: Session,
    settings: Settings,
) -> bool:
    """check the signature of the webhook request"""

    client = jwt_check_client(db, settings)
    webhook = webhook_check(webhook_id, client)
    key_a = settings.WH_KEY_A
    key_b = settings.WH_KEY_B

    return webhook.validate_message(body, header, key_a, key_b)
