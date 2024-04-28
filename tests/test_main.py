import pytest
import os
from unittest import mock
from main import main

def test_missing_input_image():
    test_args = ['main.py']
    with pytest.raises(SystemExit) as e:
        with mock.patch('sys.argv', test_args):
            main()
    assert e.type == SystemExit
    assert e.value.code == 2  # argparse exits with code 2 on error

def test_decode_with_extra_args():
    test_args = ['main.py', '-i', 'image.png', '-m', 'message', '-d']
    with mock.patch('sys.argv', test_args):
        with mock.patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_once_with(1)

@mock.patch('main.decode', return_value="hidden message")
def test_decode_success(mock_decode):
    test_args = ['main.py', '-i', 'image.png', '-d']
    with mock.patch('sys.argv', test_args):
        with mock.patch('logging.info') as mock_log_info:
            main()
            mock_log_info.assert_called_with("Decoded message: %s", "hidden message")

def test_encode_missing_message():
    test_args = ['main.py', '-i', 'image.png']
    with mock.patch('sys.argv', test_args):
        with mock.patch('sys.exit') as mock_exit:
            main()
            mock_exit.assert_called_once_with(1)

@mock.patch('main.encode', return_value=True)
def test_encode_success(mock_encode):
    test_args = ['main.py', '-i', 'image.png', '-m', 'secret', '-o', 'output.png']
    with mock.patch('sys.argv', test_args):
        with mock.patch('logging.info') as mock_log_info:
            main()
            mock_log_info.assert_called_with("Message encoded successfully into %s", 'output.png')

@mock.patch('main.encode', side_effect=PermissionError("Permission denied"))
def test_encode_permission_error(mock_encode):
    test_args = ['main.py', '-i', 'image.png', '-m', 'secret', '-o', 'output.png']
    with mock.patch('sys.argv', test_args), \
         mock.patch('sys.exit') as mock_exit, \
         mock.patch('logging.error') as mock_log_error:
        main()
        mock_exit.assert_called_once_with(1)
        mock_log_error.assert_called_with("Error encoding the image: Permission denied")

@mock.patch('main.encrypt_message', return_value="encrypted message")
@mock.patch('main.encode', return_value=True)
def test_encode_with_encryption_success(mock_encode, mock_encrypt_message):
    test_args = ['main.py', '-i', 'image.png', '-m', 'secret', '-o', 'output.png', '-p', 'password']
    with mock.patch('sys.argv', test_args):
        with mock.patch('logging.info') as mock_log_info:
            main()
            mock_encrypt_message.assert_called_once_with('secret', 'password')
            mock_log_info.assert_called_with("Message encoded successfully into %s", 'output.png')

#### Test Decryption During Decoding:
@mock.patch('main.decrypt_message', return_value="decrypted message")
@mock.patch('main.decode', return_value="encrypted message")
def test_decode_with_decryption_success(mock_decode, mock_decrypt_message):
    test_args = ['main.py', '-i', 'image.png', '-d', '-p', 'password']
    with mock.patch('sys.argv', test_args):
        with mock.patch('logging.info') as mock_log_info:
            main()
            mock_decrypt_message.assert_called_once_with('encrypted message', 'password')
            mock_log_info.assert_called_with("Decoded message: %s", "decrypted message")

#### Test Failed Decryption:
@mock.patch('main.decrypt_message', side_effect=Exception("Decryption failed"))
@mock.patch('main.decode', return_value="encrypted message")
def test_decode_with_decryption_failure(mock_decode, mock_decrypt_message):
    test_args = ['main.py', '-i', 'image.png', '-d', '-p', 'wrongpassword']
    with mock.patch('sys.argv', test_args), \
         mock.patch('sys.exit') as mock_exit, \
         mock.patch('logging.error') as mock_log_error:
        main()
        mock_exit.assert_called_once_with(1)
        mock_log_error.assert_called_with("Error decoding the message: Decryption failed")

@mock.patch.dict(os.environ, {"STEG_PASS": "envpassword"}, clear=True)
@mock.patch('main.encrypt_message', return_value="encrypted message")
@mock.patch('main.encode', return_value=True)
def test_encode_with_env_var_password(mock_encode, mock_encrypt_message):
    test_args = ['main.py', '-i', 'image.png', '-m', 'secret', '-o', 'output.png']
    with mock.patch('sys.argv', test_args):
        with mock.patch('logging.info') as mock_log_info:
            main()
            mock_encode.assert_called_once_with('image.png', "encrypted message", 'output.png')

@mock.patch.dict(os.environ, {"STEG_PASS": "envpassword"}, clear=True)
@mock.patch('main.decode', return_value="encrypted message")
@mock.patch('main.decrypt_message', return_value="decrypted message")
def test_decode_with_env_var_password(mock_decrypt_message, mock_decode):
    test_args = ['main.py', '-i', 'image.png', '-d']
    with mock.patch('sys.argv', test_args):
        with mock.patch('logging.info') as mock_log_info:
            main()
            mock_decrypt_message.assert_called_once_with('encrypted message', 'envpassword')
            mock_log_info.assert_called_with("Decoded message: %s", "decrypted message")

@mock.patch.dict(os.environ, {}, clear=True)
@mock.patch('main.encode', return_value=True)
def test_encode_without_password(mock_encode):
    test_args = ['main.py', '-i', 'image.png', '-m', 'secret', '-o', 'output.png']
    with mock.patch('sys.argv', test_args):
        with mock.patch('logging.info') as mock_log_info:
            main()
            mock_encode.assert_called_once_with('image.png', 'secret', 'output.png')

@mock.patch.dict(os.environ, {}, clear=True)
@mock.patch('main.decode', return_value="plain message")
def test_decode_without_password(mock_decode):
    test_args = ['main.py', '-i', 'image.png', '-d']
    with mock.patch('sys.argv', test_args):
        with mock.patch('logging.info') as mock_log_info:
            main()
            mock_log_info.assert_called_with("Decoded message: %s", "plain message")
