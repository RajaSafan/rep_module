
    
import hashlib
import secrets

from cryptography.fernet import Fernet

from backend.core.config import settings


fernet = Fernet(
    settings.token_encryption_key.encode()
)


def create_invitation_token() -> tuple[str, str]:
    raw_token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()

    return raw_token, token_hash


def hash_invitation_token(raw_token: str) -> str:
    return hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()


def encrypt_token(token: str) -> str:
    return fernet.encrypt(
        token.encode("utf-8")
    ).decode("utf-8")


def decrypt_token(encrypted_token: str) -> str:
    return fernet.decrypt(
        encrypted_token.encode("utf-8")
    ).decode("utf-8")    