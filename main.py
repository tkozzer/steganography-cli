import argparse
import sys
import os
import logging
from encryption import encrypt_message, decrypt_message
from steganography import encode, decode
from utils import setup_logging
from dotenv import load_dotenv

def main():
    setup_logging()
    load_dotenv()

    parser = argparse.ArgumentParser(description="Steganography CLI: Hide or retrieve messages in images")
    parser.add_argument('-i', '--input-image', type=str, required=True, help="Path to the input image file")
    parser.add_argument('-m', '--message', type=str, help="The message to hide, or path to a file containing the message; required for encoding")
    parser.add_argument('-o', '--output-image', type=str, help="Path to the output image file (optional for encoding)")
    parser.add_argument('-d', '--decode', action='store_true', help="Decode a message from an image (default: encode)")
    parser.add_argument('-p', '--password', type=str, help="Password to use for encryption or decryption (optional)")

    args = parser.parse_args()

    # Check for password either via command-line or environment variable
    password = args.password if args.password else os.getenv('STEG_PASS')
    
    if args.decode:
        decode_message(args, password)
    else:
        encode_message(args, password)

def decode_message(args, password):
    if args.message or args.output_image:
        logging.error("No message or output image should be specified when decoding.")
        sys.exit(1)
    try:
        if password:
            logging.info("Using password for decryption")
        encrypted_message = decode(args.input_image)
        message = decrypt_message(encrypted_message, password) if password else encrypted_message
        logging.info("Decoded message: %s", message)
    except Exception as e:
        logging.error(f"Error decoding the message: {e}")
        sys.exit(1)

def encode_message(args, password):
    if not args.message:
        logging.error("A message is required for encoding.")
        sys.exit(1)
    try:
        if password:
            logging.info("Using password for encryption")
        message = encrypt_message(args.message, password) if password else args.message
        output_image_path = args.output_image if args.output_image else args.input_image
        if encode(args.input_image, message, output_image_path):
            logging.info("Message encoded successfully into %s", output_image_path)
    except Exception as e:
        logging.error(f"Error encoding the image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
