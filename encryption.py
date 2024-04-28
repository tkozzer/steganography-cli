from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

def generate_key(password: str, salt: bytes) -> bytes:
    """Generate a key from the given password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # Length of the key for AES256
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    # Directly return the Fernet key
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_message(message: str, password: str) -> str:
    """Encrypt the message using the given password."""
    try:
        salt = os.urandom(16)  # Generate a random salt
        key = generate_key(password, salt)
        fernet = Fernet(key)
        encrypted_message = fernet.encrypt(message.encode())
        return base64.urlsafe_b64encode(salt + encrypted_message).decode('ascii')
    except Exception as e:
        raise ValueError("Error encrypting the message") from e

def decrypt_message(encrypted_message: str, password: str) -> str:
    """Decrypt the message using the given password."""
    try:
        data = base64.urlsafe_b64decode(encrypted_message.encode('ascii'))
        salt = data[:16]
        key = generate_key(password, salt)
        fernet = Fernet(key)
        decrypted_message = fernet.decrypt(data[16:])
        return decrypted_message.decode()
    except Exception as e:
        raise ValueError("Error decrypting the message") from e
