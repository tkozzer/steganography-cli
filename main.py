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

    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Steganography CLI: Hide or retrieve messages in images",
                                     add_help=False)  # Disable automatic help to handle manually
    parser.add_argument('-i', '--input-image', type=str, required=False, help="Path to the input image file")
    parser.add_argument('-m', '--message', type=str, required=False, help="The message to hide")
    parser.add_argument('-o', '--output-image', type=str, help="Path to the output image file (optional for encoding)")
    parser.add_argument('-d', '--decode', action='store_true', help="Decode a message from an image (default: encode)")
    parser.add_argument('-p', '--password', type=str, help="Password to use for encryption or decryption (optional)")
    parser.add_argument('-h', '--help', action='store_true', help="Show this help message and exit")
    parser.add_argument('mode', nargs='?', help="Operate in 'interactive' mode")

    args = parser.parse_args()

    # Check for help or no arguments
    if args.help or not any(vars(args).values()):
        parser.print_help()
        raise SystemExit
    elif args.mode == 'interactive':
        run_interactive()
    else:
        run_non_interactive(args)

def run_interactive():
    print("Interactive Steganography CLI")
    action = input("Do you want to encode or decode a message? (encode/decode | e/d): ").strip().lower()
    input_image = input("Enter the path to the input image file: ").strip()
    password = input("Enter a password for encryption/decryption (optional, press enter to skip): ").strip() or None

    if action in ['decode', 'd']:
        decode_message(input_image, password)
    elif action in ['encode', 'e']:
        message = input("Enter the message to hide: ").strip()
        output_image = input("Enter the path to the output image file (optional, press enter to use the same as input): ").strip() or input_image
        encode_message(input_image, message, output_image, password)
    else:
        print("Invalid action. Please choose either 'encode' or 'decode'.")
        raise ValueError("Invalid action selected.")

def run_non_interactive(args):
    password: Optional[str] = args.password if args.password else os.getenv('STEG_PASS')
    if args.decode:
        decode_message(args.input_image, password)
    else:
        if not args.input_image or not args.message:
            raise ValueError("Both an input image and a message are required for encoding.")
        encode_message(args.input_image, args.message, args.output_image, password)

def decode_message(input_image: str, password: Optional[str]) -> None:
    try:
        encrypted_message = decode(input_image)
        message = decrypt_message(encrypted_message, password) if password else encrypted_message
        logging.info("Decoded message: %s", message)
    except Exception as e:
        logging.error(f"Error decoding the message: {e}")
        raise e  # Rethrow the exception to be handled in the main block

def encode_message(input_image: str, message: str, output_image_path: Optional[str], password: Optional[str]) -> None:
    try:
        message = encrypt_message(message, password) if password else message
        output_image = output_image_path if output_image_path else input_image
        if encode(input_image, message, output_image):
            logging.info("Message encoded successfully into %s", output_image)
    except Exception as e:
        logging.error(f"Error encoding the image: {e}")
        raise e  # Rethrow the exception to be handled in the main block

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)
