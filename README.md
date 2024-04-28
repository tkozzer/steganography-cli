# Steganography CLI

Steganography CLI is a command-line tool that enables users to hide and retrieve encrypted messages within images. This tool leverages Python's cryptography and Pillow libraries to provide robust encryption and image manipulation capabilities, respectively.

## Features

- **Encode Messages**: Hide a message inside an image with optional AES encryption using a password.
- **Decode Messages**: Retrieve hidden messages from an image, decrypting them if they were encrypted using a password.
- **Interactive Mode**: Offers an interactive CLI mode for user-friendly operation.
- **Non-Interactive Mode**: Allows batch processing through command line arguments.
- **Logging**: Includes detailed logging to help with troubleshooting and understanding the tool's operation.

## Installation

Before you can use Steganography CLI, you need to set up your environment:

### Prerequisites

- Python 3.8 or higher
- Pip for installing Python packages

### Dependencies

Install all required dependencies with pip:

```bash
pip install -r requirements.txt
```

## Environment Variables

Optionally, you can set an environment variable for the encryption password:

```bash
export STEG_PASS='your_encryption_password_here'
```

## Usage

### Running the CLI

To use the CLI, navigate to the directory containing the script and run:

```bash
python -m steganography.main
```

### Command Line Arguments

The CLI supports the following arguments:

- -i, --input-image: Path to the input image file.
- -m, --message: The message to hide inside the image.
- -o, --output-image: Path for the output image file (optional for encoding).
- -d, --decode: Decode a message from an image.
- -p, --password: Password for encrypting or decrypting the message.
- -h, --help: Display help message and exit.
- mode: Specify 'interactive' for interactive mode.

### Interactive Mode

Start interactive mode by adding 'interactive' at the end of the command:

```bash
python -m steganography.main interactive
```

Follow the prompts to encode or decode messages.

### Examples

Encoding a Message:

```bash
python -m steganography.main -i path/to/input.png -m "Your secret message" -o path/to/output.png -p YourPassword
```

Decoding a Message:

```bash
python -m steganography.main -d -i path/to/image.png -p YourPassword
```

## Development

### Testing

Run tests using pytest:

```bash
pytest
```

Ensure that you have test images and necessary configurations in place for integration tests.

## Contributing

Contributions to improve Steganography CLI are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details. The MIT License permits users to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
