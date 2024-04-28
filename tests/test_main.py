import pytest
from unittest.mock import patch, MagicMock
from main import decode_message, encode_message, main, run_interactive, run_non_interactive

def test_main_help(capsys):
    test_args = ['program', '-h']
    with patch('sys.argv', test_args):
        with pytest.raises(SystemExit):
            main()
        captured = capsys.readouterr()
        assert 'Steganography CLI' in captured.out

def test_main_no_args(capsys):
    test_args = ['program']
    with patch('sys.argv', test_args):
        with pytest.raises(SystemExit):
            main()
        captured = capsys.readouterr()
        assert 'usage:' in captured.out  # Expect the help message usage to be part of the output

def test_main_interactive_mode():
    test_args = ['program', 'interactive']
    with patch('sys.argv', test_args), patch('main.run_interactive') as mock_interactive:
        main()
        mock_interactive.assert_called_once()

def test_run_interactive_encode(mocker):
    mocker.patch('builtins.input', side_effect=['encode', 'input.png', '', 'Secret message', 'output.png'])
    with patch('main.encode_message') as mock_encode:
        run_interactive()
        mock_encode.assert_called_once_with('input.png', 'Secret message', 'output.png', None)

def test_run_interactive_invalid_action(mocker):
    mocker.patch('builtins.input', side_effect=['unknown action', 'input.png', '', 'output.png'])
    with pytest.raises(ValueError) as excinfo:
        run_interactive()
    assert "Invalid action selected." in str(excinfo.value)

def test_main_non_interactive_mode():
    test_args = ['program', '-i', 'input.png', '-m', 'Hello', '-o', 'output.png']
    with patch('sys.argv', test_args), patch('main.run_non_interactive') as mock_non_interactive:
        main()
        mock_non_interactive.assert_called_once()


def test_run_non_interactive_encode():
    args = MagicMock(input_image='input.png', message='Hello', output_image='output.png', decode=False, password=None)
    with patch('main.encode_message') as mock_encode, patch('os.getenv', return_value=None):
        run_non_interactive(args)
        mock_encode.assert_called_once_with('input.png', 'Hello', 'output.png', None)

# Similar tests can be added for decoding scenarios.

def test_encode_message_success(mocker):
    mocker.patch('main.encrypt_message', return_value='Encrypted')
    mocker.patch('main.encode', return_value=True)
    encode_message('input.png', 'Secret', 'output.png', 'password')

def test_decode_message_failure(mocker, caplog):
    mocker.patch('main.decode', side_effect=Exception('Failed'))
    with pytest.raises(Exception):
        decode_message('input.png', 'password')
    assert 'Error decoding the message' in caplog.text

# Additional tests should handle different branches and exceptions.

def test_encode_message_no_password(mocker):
    mocker.patch('main.encrypt_message', side_effect=lambda x, y: x)  # No encryption applied
    mocker.patch('main.encode', return_value=True)
    with patch('logging.info') as mock_log_info:
        encode_message('input.png', 'Test Message', 'output.png', None)
        mock_log_info.assert_called_with("Message encoded successfully into %s", 'output.png')

# def test_main_missing_arguments(mocker):
#     test_args = ['program', '-i', 'input.png']  # Missing message argument for encoding
#     mocker.patch('sys.argv', test_args)
#     with patch('sys.exit') as mock_exit:
#         with pytest.raises(ValueError):  # Assuming your program raises ValueError for missing args
#             main()
#         mock_exit.assert_called_once_with(1)  # Assuming the program exits with status 1 on error
