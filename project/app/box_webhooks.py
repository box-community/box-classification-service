""" handle box webhooks from box exvents"""
from functools import lru_cache
from sqlalchemy.orm import Session
from boxsdk import BoxAPIException

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


# def webhook_process_request(request_data: dict):
#     """
#     Process a webhook event request
#     """
#     webhook_id = request_data["webhook"]["id"]
#     webhook_trigger = request_data["trigger"]
#     webhook_source = request_data["source"]

#     if webhook_trigger == "FILE.PREVIEWED":

#         file_id = webhook_source["id"]

#     if webhook_trigger == "TASK_ASSIGNMENT.UPDATED":
#         webhook_process_task(webhook_source)

#     if (
#         webhook_trigger == "SIGN_REQUEST.COMPLETED"
#         or webhook_trigger == "SIGN_REQUEST.DECLINED"
#         or webhook_trigger == "SIGN_REQUEST.EXPIRED"
#     ):
#         webhook_process_sign(webhook_trigger, webhook_source)


# def webhook_process_task(webhook_source: dict):
#     """
#     Process a webhook task request
#     """
#     task_id = webhook_source["id"]
#     resolution_state = webhook_source["resolution_state"]
#     file_id = webhook_source["item"]["id"]

#     booking_divers_cert = Booking_Diver.query.filter_by(
#         certification_file_id=file_id
#     ).first()

#     if booking_divers_cert is not None:
#         booking_divers_cert.certification_status = resolution_state

#     booking_divers_ins = Booking_Diver.query.filter_by(
#         insurance_file_id=file_id
#     ).first()

#     if booking_divers_ins is not None:
#         booking_divers_ins.insurance_status = resolution_state

#     booking_divers_waiver = Booking_Diver.query.filter_by(
#         waiver_file_id=file_id
#     ).first()

#     if booking_divers_waiver is not None:
#         booking_divers_waiver.waiver_status = resolution_state

#     db.session.commit()


# def webhook_process_sign(webhook_trigger:str, webhook_source: dict):
#     file_id = webhook_source["id"]

#     booking_divers_waiver = Booking_Diver.query.filter_by(
#         waiver_file_id=file_id
#     ).first()

#     resolution_state = webhook_trigger.split('.')[1]

#     if booking_divers_waiver is not None:
#         booking_divers_waiver.waiver_status = resolution_state

#     db.session.commit()
