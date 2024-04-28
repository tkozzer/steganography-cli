import argparse
import sys
import logging
from steganography import encode, decode
from utils import setup_logging

def main():
    # Set up logging
    setup_logging()

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Steganography CLI: Hide or retrieve messages in images")
    parser.add_argument('-i', '--input-image', type=str, required=True, help="Path to the input image file")
    parser.add_argument('-m', '--message', type=str, help="The message to hide, or path to a file containing the message; required for encoding")
    parser.add_argument('-o', '--output-image', type=str, help="Path to the output image file (optional for encoding)")
    parser.add_argument('-d', '--decode', action='store_true', help="Decode a message from an image (default: encode)")

    args = parser.parse_args()

    # Process the provided arguments
    if args.decode:
        if args.message or args.output_image:
            logging.error("No message or output image should be specified when decoding.")
            sys.exit(1)
        try:
            message = decode(args.input_image)
            logging.info("Decoded message: %s", message)
        except Exception as e:
            logging.error(f"Error decoding the message: {e}")
            sys.exit(1)
        message = decode(args.input_image)
    else:
        if not args.message:
            logging.error("A message is required for encoding.")
            sys.exit(1)
        try:
            output_image_path = args.output_image if args.output_image else args.input_image
            if encode(args.input_image, args.message, output_image_path):
                logging.info("Message encoded successfully into %s", output_image_path)
        except Exception as e:
            logging.error(f"Error encoding the image: {e}")
            sys.exit(1)
        output_image_path = args.output_image if args.output_image else args.input_image

if __name__ == "__main__":
    main()