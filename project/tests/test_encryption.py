"""Test encryption module."""

from tests.config import get_settings_override
from app.cypto import encrypt_token, decrypt_token


def test_encrypt_decrypt():
    """Test encrypt and decrypt."""
    settings = get_settings_override()
    encrypted_token = encrypt_token("hello", settings.FERNET_KEY)
    decrypted_token = decrypt_token(encrypted_token, settings.FERNET_KEY)

    assert decrypted_token == "hello"
    assert encrypted_token != "hello"
    assert encrypted_token != decrypted_token
