import pytest
from unittest.mock import patch
from encryption import generate_key, encrypt_message, decrypt_message

@pytest.fixture
def password():
    return "strongpassword"

@pytest.fixture
def salt():
    return b"1234567890123456"  # fixed salt for testing

@pytest.fixture
def key(password, salt):
    return generate_key(password, salt)

def test_generate_key(password, salt):
    # Test that the key is generated correctly and consistently
    key = generate_key(password, salt)
    assert isinstance(key, bytes)
    assert len(key) == 44  # Check if key length is as expected from urlsafe_b64encode

def test_encrypt_message(password, salt, key):
    message = "secret message"
    with patch('os.urandom', return_value=salt):
        encrypted_message = encrypt_message(message, password)
    assert isinstance(encrypted_message, str)
    assert encrypted_message != message  # ensure message is encrypted

def test_decrypt_message(password, salt, key):
    message = "secret message"
    with patch('os.urandom', return_value=salt):
        encrypted_message = encrypt_message(message, password)
    decrypted_message = decrypt_message(encrypted_message, password)
    assert decrypted_message == message  # ensure message is correctly decrypted

# Optionally, add tests for failure cases
def test_decrypt_message_with_wrong_password(password, salt, key):
    wrong_password = "weakpassword"
    message = "secret message"
    with patch('os.urandom', return_value=salt):
        encrypted_message = encrypt_message(message, password)
    with pytest.raises(Exception):
        decrypt_message(encrypted_message, wrong_password)

# Test with different passwords and messages
@pytest.mark.parametrize("message, password", [
    ("hello", "pass123"),
    ("bye", "strongpass"),
    ("12345", "weakpass")
])
def test_message_encryption_decryption(message, password):
    encrypted_message = encrypt_message(message, password)
    decrypted_message = decrypt_message(encrypted_message, password)
    assert decrypted_message == message
