# Base Encoder/Decoder Toolkit

A comprehensive encoding toolkit that supports multiple base formats (Base16, Base32, Base64), auto-detects input encoding, and handles invalid data gracefully.

## Features

- **Multiple Format Support**: Encode and decode Base16 (hex), Base32, and Base64
- **Auto-Detection**: Automatically detect the encoding format of input data
- **Error Handling**: Graceful handling of invalid data with clear error messages
- **Format Conversion**: Convert between different base encoding formats
- **Validation**: Check if data is valid for a specific encoding format
- **CLI Tool**: Command-line interface for easy encoding/decoding operations
- **Python API**: Clean and well-documented Python API for programmatic use

## Installation

Clone the repository:

```bash
git clone https://github.com/BaseMax/base-encoder-decoder.git
cd base-encoder-decoder
```

No additional dependencies required - uses only Python standard library.

## Usage

### Command-Line Interface (CLI)

#### Encode Data

```bash
# Encode to Base64 (default)
python3 base_cli.py encode "Hello, World!"

# Encode to Base16 (hexadecimal)
python3 base_cli.py encode -f base16 "Hello, World!"

# Encode to Base32
python3 base_cli.py encode -f base32 "Hello, World!"

# Encode from stdin
echo "Hello, World!" | python3 base_cli.py encode -f base64
```

#### Decode Data

```bash
# Auto-detect format and decode
python3 base_cli.py decode "SGVsbG8sIFdvcmxkIQ=="

# Decode with specific format
python3 base_cli.py decode -f base32 "JBSWY3DPEBLW64TMMQ======"

# Decode from stdin
echo "48656C6C6F" | python3 base_cli.py decode -f base16
```

#### Auto-Detect Format

```bash
# Detect the encoding format
python3 base_cli.py detect "SGVsbG8sIFdvcmxkIQ=="
python3 base_cli.py detect "48656C6C6F"
python3 base_cli.py detect "JBSWY3DP"
```

#### Convert Between Formats

```bash
# Convert Base64 to Base16
python3 base_cli.py convert -f base64 -t base16 "SGVsbG8="

# Convert Base16 to Base32 (auto-detect source)
python3 base_cli.py convert -t base32 "48656C6C6F"
```

#### Validate Data

```bash
# Check if data is valid Base64
python3 base_cli.py validate -f base64 "SGVsbG8="

# Check if data is valid Base16
python3 base_cli.py validate -f base16 "48656C6C6F"
```

### Python API

```python
from base_codec import BaseCodec, EncodingFormat

# Encoding
text = "Hello, World!"
base64_encoded = BaseCodec.encode(text, EncodingFormat.BASE64)
base32_encoded = BaseCodec.encode(text, EncodingFormat.BASE32)
base16_encoded = BaseCodec.encode(text, EncodingFormat.BASE16)

# Decoding with specific format
decoded = BaseCodec.decode("SGVsbG8sIFdvcmxkIQ==", EncodingFormat.BASE64)
print(decoded.decode('utf-8'))  # "Hello, World!"

# Auto-detection and decoding
decoded = BaseCodec.decode("SGVsbG8sIFdvcmxkIQ==")  # Auto-detects Base64
print(decoded.decode('utf-8'))  # "Hello, World!"

# Format detection
format = BaseCodec.detect_format("48656C6C6F")
print(format)  # EncodingFormat.BASE16

# Format conversion
base16_data = BaseCodec.convert("SGVsbG8=", EncodingFormat.BASE64, EncodingFormat.BASE16)
print(base16_data)  # "48656C6C6F"

# Validation
is_valid = BaseCodec.is_valid("SGVsbG8=", EncodingFormat.BASE64)
print(is_valid)  # True
```

## Running Tests

Run the comprehensive test suite:

```bash
python3 test_base_codec.py
```

Run with verbose output:

```bash
python3 test_base_codec.py -v
```

## Examples

See the examples in action:

```bash
# Run the example demonstrations
python3 base_codec.py
```

This will show:
- Encoding examples for all formats
- Auto-detection examples
- Error handling demonstrations
- Format conversion examples

## Architecture

The toolkit consists of three main components:

1. **base_codec.py**: Core encoding/decoding functionality
   - `BaseCodec` class with static methods for all operations
   - `EncodingFormat` enum for format specification
   - Auto-detection algorithm
   - Error handling and validation

2. **base_cli.py**: Command-line interface
   - Argument parsing and command routing
   - Support for stdin/stdout pipelines
   - User-friendly error messages

3. **test_base_codec.py**: Comprehensive test suite
   - Unit tests for all functionality
   - Edge case testing
   - Error handling verification

## Supported Formats

### Base16 (Hexadecimal)
- Characters: 0-9, A-F (case-insensitive)
- Most compact representation
- Example: `48656C6C6F` → "Hello"

### Base32
- Characters: A-Z, 2-7, with padding (=)
- Case-insensitive
- Good for human-readable codes
- Example: `JBSWY3DP` → "Hello"

### Base64
- Characters: A-Z, a-z, 0-9, +, /, with padding (=)
- Most common encoding for data transfer
- Example: `SGVsbG8=` → "Hello"

## Auto-Detection Algorithm

The toolkit uses a sophisticated algorithm to detect encoding formats:

1. **Base16 Detection**: Checks for hexadecimal characters only (0-9, A-F) with even length
2. **Base32 Detection**: Checks for Base32 alphabet (A-Z, 2-7) with valid padding
3. **Base64 Detection**: Checks for Base64 alphabet with valid padding and length
4. **Validation**: Attempts to decode to verify the format

## Error Handling

The toolkit provides graceful error handling:

- Invalid characters for the specified format
- Incorrect padding
- Malformed input data
- Unsupported formats
- Auto-detection failures

All errors include descriptive messages to help identify the issue.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Author

Maintained by BaseMax
