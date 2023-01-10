"""Crypto functions."""
from cryptography.fernet import Fernet
from app.config import Settings

def encrypt_token(token:str, settings:Settings) -> str:
    """Encrypt token."""
    key = settings.FERNET_KEY
    encoded_token = token.encode()
    f = Fernet(key)
    encrypted = f.encrypt(encoded_token)
    return encrypted.decode()

def decrypt_token(token:str, settings:Settings) -> str:
    """Decrypt token."""
    key = settings.FERNET_KEY
    encoded_token = token.encode()
    f = Fernet(key)
    dencrypted = f.decrypt(encoded_token)
    return dencrypted.decode()