"""Crypto functions."""
from cryptography.fernet import Fernet, InvalidToken

def encrypt_token(token:str, fernet_key: str) -> str:
    """Encrypt token."""
    key = fernet_key
    encoded_token = token.encode()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(encoded_token)
    return encrypted.decode()

def decrypt_token(token:str, fernet_key: str) -> str:
    """Decrypt token."""
    key = fernet_key
    encoded_token = token.encode()
    fernet = Fernet(key)
    dencrypted = fernet.decrypt(encoded_token)
    return dencrypted.decode()
    