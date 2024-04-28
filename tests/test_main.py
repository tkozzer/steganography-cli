import pytest
import logging
from unittest.mock import patch, MagicMock
from main import main
import tempfile
import shutil
import sys

@pytest.fixture
def setup_env(monkeypatch):
    def _setup_env(password=None):
        if password is None:
            monkeypatch.delenv("STEG_PASS", raising=False)
        else:
            monkeypatch.setenv("STEG_PASS", password)
    return _setup_env

def test_encode_with_password_provided(setup_env):
    setup_env()  # Ensure no STEG_PASS environment variable is set
    with patch('main.argparse.ArgumentParser.parse_args') as mock_args, \
         patch('main.os.path.isfile', return_value=True), \
         patch('main.encode_message') as mock_encode, \
         patch('main.load_dotenv'):
        mock_args.return_value = MagicMock(input_image='path/to/image.png',
                                           message='Secret',
                                           output_image='path/to/output.png',
                                           password='mypassword',
                                           decode=False)
        main()
        mock_encode.assert_called_once_with('path/to/image.png', 'Secret', 'path/to/output.png', 'mypassword')

def test_decode_failure_no_password_no_env_var(setup_env):
    setup_env()  # Clear the environment variable explicitly
    with patch('main.argparse.ArgumentParser.parse_args') as mock_args, \
         patch('main.decode_message') as mock_decode, \
         patch('main.load_dotenv'):
        mock_args.return_value = MagicMock(input_image='path/to/image.png',
                                           message=None,
                                           output_image=None,
                                           password=None,
                                           decode=True)
        main()
        mock_decode.assert_called_once_with('path/to/image.png', None)

# Remember to use `setup_env` in tests that require specific env var settings

def test_decode_success_with_provided_password(setup_env):
    setup_env()  # Clear any environment variables
    with patch('main.argparse.ArgumentParser.parse_args') as mock_args, \
         patch('main.decode_message') as mock_decode, \
         patch('main.load_dotenv'):
        mock_args.return_value = MagicMock(input_image='path/to/image.png',
                                           message=None,
                                           output_image=None,
                                           password='mypassword',
                                           decode=True)
        main()
        mock_decode.assert_called_once_with('path/to/image.png', 'mypassword')

def test_decode_failure_with_provided_password(setup_env):
    setup_env()  # Clear any environment variables
    with patch('main.argparse.ArgumentParser.parse_args') as mock_args, \
         patch('main.decode_message') as mock_decode, \
         patch('main.load_dotenv'):
        mock_args.return_value = MagicMock(input_image='path/to/image.png',
                                           message=None,
                                           output_image=None,
                                           password='mypassword',
                                           decode=True)
        # Let's mock the decode function to raise an exception
        mock_decode.side_effect = ValueError("Failed to decode the message.")
        with pytest.raises(ValueError) as exc_info:
            main()
        assert exc_info.type == ValueError
        assert str(exc_info.value) == "Failed to decode the message."

# We'll also need tests for scenarios where decoding succeeds/fails using the environment variable password (STEG_PASS), and when no password is provided at all. 

def test_decode_success_with_env_var_password(setup_env):
    setup_env(password='env_password')  # Set environment variable
    with patch('main.argparse.ArgumentParser.parse_args') as mock_args, \
         patch('main.decode_message') as mock_decode, \
         patch('main.load_dotenv'):
        mock_args.return_value = MagicMock(input_image='path/to/image.png',
                                           message=None,
                                           output_image=None,
                                           password=None,
                                           decode=True)
        main()
        mock_decode.assert_called_once_with('path/to/image.png', 'env_password')

def test_decode_failure_with_env_var_password(setup_env):
    setup_env(password='env_password')  # Set environment variable
    with patch('main.argparse.ArgumentParser.parse_args') as mock_args, \
         patch('main.decode_message') as mock_decode, \
         patch('main.load_dotenv'):
        mock_args.return_value = MagicMock(input_image='path/to/image.png',
                                           message=None,
                                           output_image=None,
                                           password=None,
                                           decode=True)
        # Let's mock the decode function to raise an exception
        mock_decode.side_effect = ValueError("Failed to decode the message.")
        with pytest.raises(ValueError) as exc_info:
            main()
        assert exc_info.type == ValueError
        assert str(exc_info.value) == "Failed to decode the message."

def test_decode_success_with_no_password_or_env_var(setup_env):
    setup_env()  # Ensure no environment variable
    with patch('main.argparse.ArgumentParser.parse_args') as mock_args, \
         patch('main.decode_message') as mock_decode, \
         patch('main.load_dotenv'):
        mock_args.return_value = MagicMock(input_image='path/to/image.png',
                                           message=None,
                                           output_image=None,
                                           password=None,
                                           decode=True)
        main()
        mock_decode.assert_called_once_with('path/to/image.png', None)

def test_decode_failure_with_no_password_or_env_var(setup_env):
    setup_env()  # Ensure no environment variable
    with patch('main.argparse.ArgumentParser.parse_args') as mock_args, \
         patch('main.decode_message') as mock_decode, \
         patch('main.load_dotenv'):
        mock_args.return_value = MagicMock(input_image='path/to/image.png',
                                           message=None,
                                           output_image=None,
                                           password=None,
                                           decode=True)
        # Let's mock the decode function to raise an exception
        mock_decode.side_effect = ValueError("Failed to decode the message.")
        with pytest.raises(ValueError) as exc_info:
            main()
        assert exc_info.type == ValueError
        assert str(exc_info.value) == "Failed to decode the message."

def test_invalid_image_format(setup_env):
    setup_env()  # Ensure no STEG_PASS environment variable is set
    with patch('main.argparse.ArgumentParser.parse_args') as mock_args, \
         patch('main.os.path.isfile', return_value=True), \
         patch('main.encode_message') as mock_encode, \
         patch('main.load_dotenv'):
        mock_args.return_value = MagicMock(input_image='path/to/image.jpg',  # Invalid format
                                           message='Secret',
                                           output_image='path/to/output.png',
                                           password='mypassword',
                                           decode=False)
        with pytest.raises(ValueError) as exc_info:
            main()
        assert 'Input image must be a valid PNG, BMP, or TIFF file.' in str(exc_info.value)
        mock_encode.assert_not_called()
