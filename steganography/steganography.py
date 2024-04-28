import logging
from PIL import Image

def encode(input_image_path: str, message: str, output_image_path: str) -> bool:
    try:
        img = Image.open(input_image_path)
        encoded_img = img.copy()
        encoded_pixels = list(encoded_img.getdata())

        # Use bytes for the message and append a null byte sequence to indicate the end
        byte_message = message.encode('utf-8') + b'\x00\x00\x00\x00'
        binary_message = ''.join(format(byte, '08b') for byte in byte_message)
        
        if len(binary_message) > len(encoded_pixels):
            logging.error("Image does not have enough capacity to hold the message.")
            return False

        for i, bit in enumerate(binary_message):
            pixel = list(encoded_pixels[i])
            pixel[0] = (pixel[0] & ~1) | int(bit)
            encoded_pixels[i] = tuple(pixel)

        encoded_img.putdata(encoded_pixels)
        encoded_img.save(output_image_path)
        return True
    except Exception as e:
        logging.error(f"Error encoding the image: {e}")
        raise ValueError(f"Failed to encode the image. {e}")

def decode(image_path: str) -> str:
    try:
        img = Image.open(image_path)
        pixels = list(img.getdata())

        binary_message = ''
        for pixel in pixels:
            binary_message += str(pixel[0] & 1)

        byte_list = []
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if byte == '00000000':
                break
            byte_list.append(int(byte, 2))

        return bytes(byte_list).decode('utf-8')
    except Exception as e:
        logging.error(f"Error decoding the message: {e}")
        return ""

