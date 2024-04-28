import pytest
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

