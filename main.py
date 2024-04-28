import argparse
import sys
import os
import logging
from encryption import encrypt_message, decrypt_message
from steganography import encode, decode
from utils import setup_logging
from dotenv import load_dotenv
from typing import Optional

def main() -> None:
    setup_logging()
    load_dotenv()

    parser = argparse.ArgumentParser(description="Steganography CLI: Hide or retrieve messages in images")
    parser.add_argument('-i', '--input-image', type=str, required=True, help="Path to the input image file")
    parser.add_argument('-m', '--message', type=str, help="The message to hide, or path to a file containing the message; required for encoding")
    parser.add_argument('-o', '--output-image', type=str, help="Path to the output image file (optional for encoding)")
    parser.add_argument('-d', '--decode', action='store_true', help="Decode a message from an image (default: encode)")
    parser.add_argument('-p', '--password', type=str, help="Password to use for encryption or decryption (optional)")

    # TODO - show the help message if no arguments are provided
    # # Check if no arguments were provided
    # if len(sys.argv) == 1:
    #     parser.print_help(sys.stderr)
    #     sys.exit(1)

    args = parser.parse_args()

    # Early argument validation
    if args.decode:
        if args.message or args.output_image:
            logging.error("No message or output image should be specified when decoding.")
            raise ValueError("No message or output image should be specified when decoding.")
    else:
        if not args.message:
            logging.error("A message is required for encoding.")
            raise ValueError("A message is required for encoding.")
        if not os.path.isfile(args.input_image) or not args.input_image.endswith(('.png', '.bmp', '.tiff')):
            logging.error("Input image must be a valid PNG, BMP, or TIFF file.")
            raise ValueError("Input image must be a valid PNG, BMP, or TIFF file.")

    password: Optional[str] = args.password if args.password else os.getenv('STEG_PASS')
    
    # Proceed based on mode
    if args.decode:
        decode_message(args.input_image, password)
    else:
        encode_message(args.input_image, args.message, args.output_image, password)

def decode_message(input_image: str, password: Optional[str]) -> None:
    try:
        if password:
            logging.info("Using password for decryption")
        encrypted_message = decode(input_image)
        message = decrypt_message(encrypted_message, password) if password else encrypted_message
        logging.info("Decoded message: %s", message)
    except Exception as e:
        logging.error(f"Error decoding the message: {e}")
        raise ValueError("Failed to decode the message.")

def encode_message(input_image: str, message: str, output_image_path: Optional[str], password: Optional[str]) -> None:
    try:
        if password:
            logging.info("Using password for encryption")
        message = encrypt_message(message, password) if password else message
        output_image = output_image_path if output_image_path else input_image
        if encode(input_image, message, output_image): 
            logging.info("Message encoded successfully into %s", output_image)
    except Exception as e:
        logging.error(f"Error encoding the image: {e}")
        raise ValueError("Failed to encode the image.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)
