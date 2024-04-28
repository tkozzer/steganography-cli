import pytest
from PIL import Image
import os
from steganography import encode, decode

def create_test_image():
    """Helper function to create a test image."""
    img = Image.new('RGB', (100, 100), color = 'white')
    img_path = 'test_image.png'
    img.save(img_path)
    return img_path

@pytest.fixture(params=[(100, 100), (200, 200), (300, 300)])
def setup_image(request):
    """Pytest fixture to set up and tear down a test image of different sizes."""
    size = request.param
    img = Image.new('RGB', size, color='white')
    img_path = f'test_image_{size[0]}x{size[1]}.png'
    img.save(img_path)
    yield img_path
    os.remove(img_path)

def test_encode_decode(setup_image):
    """Test that encoding and then decoding retrieves the original message."""
    input_image_path = setup_image
    output_image_path = 'output_test_image.png'
    message = "Hello, World!"
    
    # Encode the message
    assert encode(input_image_path, message, output_image_path) == True, "Encoding failed"
    
    # Decode the message
    decoded_message = decode(output_image_path)
    assert decoded_message == message, "Decoded message does not match the original"
    
    # Cleanup
    if os.path.exists(output_image_path):
        os.remove(output_image_path)

def test_invalid_image_path():
    """Test encoding with an invalid image path."""
    with pytest.raises(ValueError):
        encode('invalid_image_path.png', "Test Message", 'output_test_image.png')

def test_message_integrity(setup_image):
    input_image_path = setup_image
    output_image_path = 'output_test_image.png'
    original_message = "Test message for integrity check.1234567890!@"

    result = encode(input_image_path, original_message, output_image_path)
    assert result, "Encoding failed due to insufficient capacity or other issues."

    decoded_message = decode(output_image_path)
    assert decoded_message == original_message, f"Message integrity compromised. Decoded: {decoded_message}"
    
    # Cleanup
    if os.path.exists(output_image_path):
        os.remove(output_image_path)

def test_encoding_capacity(setup_image):
    """Test that encoding fails gracefully when the image is too small for the message."""
    input_image_path = setup_image
    output_image_path = 'output_test_image_too_small.png'

    # Get the dimensions from the image filename
    dimensions = setup_image.replace('test_image_', '').replace('.png', '').split('x')
    width, height = map(int, dimensions)
    total_capacity = width * height
    
    # Create a message longer than the total capacity
    original_message = "A" * (total_capacity // 8 + 100)  # Ensuring the message is definitely too long

    result = encode(input_image_path, original_message, output_image_path)
    assert not result, "Encoding should fail when the image is too small for the message"
    
    # Cleanup
    if os.path.exists(output_image_path):
        os.remove(output_image_path)

def test_unicode_message_integrity(setup_image):
    """Test encoding and decoding with Unicode characters."""
    input_image_path = setup_image
    output_image_path = 'output_test_image_unicode.png'
    original_message = "测试中文字符和🙂"  # Chinese characters and an emoji

    result = encode(input_image_path, original_message, output_image_path)
    assert result, "Encoding failed for Unicode message."

    decoded_message = decode(output_image_path)
    assert decoded_message == original_message, "Unicode message integrity compromised."

    # Cleanup
    if os.path.exists(output_image_path):
        os.remove(output_image_path)



# Additional tests for file input, corrupted data handling, etc., can be added here.
