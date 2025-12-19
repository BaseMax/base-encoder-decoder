#!/usr/bin/env python3
"""
Command-line interface for Base Encoder/Decoder Toolkit
"""

import argparse
import sys
from base_codec import BaseCodec, EncodingFormat


def get_encoding_format(format_str: str) -> EncodingFormat:
    """Convert format string to EncodingFormat enum"""
    format_map = {
        'base16': EncodingFormat.BASE16,
        'base32': EncodingFormat.BASE32,
        'base64': EncodingFormat.BASE64,
        'auto': None,
    }
    return format_map.get(format_str.lower())


def encode_command(args):
    """Handle encode command"""
    try:
        # Read input
        if args.input:
            data = args.input
        else:
            data = sys.stdin.read().rstrip('\n')
        
        # Get format
        format = get_encoding_format(args.format)
        if format is None:
            raise ValueError(f"Invalid encoding format: {args.format}")
        
        # Encode
        result = BaseCodec.encode(data, format)
        
        # Output
        print(result)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def decode_command(args):
    """Handle decode command"""
    try:
        # Read input
        if args.input:
            data = args.input
        else:
            data = sys.stdin.read().rstrip('\n')
        
        # Get format (None for auto-detection)
        format = get_encoding_format(args.format) if args.format != 'auto' else None
        
        # Decode
        result = BaseCodec.decode(data, format)
        
        # Output
        if args.binary:
            sys.stdout.buffer.write(result)
        else:
            try:
                print(result.decode('utf-8'))
            except UnicodeDecodeError:
                print("Warning: Binary data detected, use --binary flag to output raw bytes", file=sys.stderr)
                # Output hex representation instead
                print(result.hex())
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def detect_command(args):
    """Handle detect command"""
    try:
        # Read input
        if args.input:
            data = args.input
        else:
            data = sys.stdin.read().rstrip('\n')
        
        # Detect format
        format = BaseCodec.detect_format(data)
        
        # Output
        print(f"Detected format: {format.value}")
        
        # Try to decode if format is known
        if format != EncodingFormat.UNKNOWN:
            try:
                decoded = BaseCodec.decode(data, format)
                print(f"Decoded value: {decoded.decode('utf-8')}")
            except:
                print("(Unable to decode as UTF-8 text)")
        
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def convert_command(args):
    """Handle convert command"""
    try:
        # Read input
        if args.input:
            data = args.input
        else:
            data = sys.stdin.read().rstrip('\n')
        
        # Get formats
        from_format = get_encoding_format(args.from_format) if args.from_format != 'auto' else None
        to_format = get_encoding_format(args.to_format)
        
        if to_format is None:
            raise ValueError(f"Invalid target encoding format: {args.to_format}")
        
        # Convert
        result = BaseCodec.convert(data, from_format, to_format)
        
        # Output
        print(result)
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def validate_command(args):
    """Handle validate command"""
    try:
        # Read input
        if args.input:
            data = args.input
        else:
            data = sys.stdin.read().rstrip('\n')
        
        # Get format
        format = get_encoding_format(args.format)
        if format is None:
            raise ValueError(f"Invalid encoding format: {args.format}")
        
        # Validate
        is_valid = BaseCodec.is_valid(data, format)
        
        # Output
        if is_valid:
            print(f"Valid {format.value}")
            return 0
        else:
            print(f"Invalid {format.value}")
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Base Encoder/Decoder Toolkit - Encode, decode, and convert between Base16, Base32, and Base64 formats',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Encode text to Base64
  %(prog)s encode -f base64 "Hello, World!"
  echo "Hello, World!" | %(prog)s encode -f base64
  
  # Decode Base64 (auto-detect)
  %(prog)s decode "SGVsbG8sIFdvcmxkIQ=="
  
  # Decode with specific format
  %(prog)s decode -f base32 "JBSWY3DPEBLW64TMMQ======"
  
  # Detect encoding format
  %(prog)s detect "48656C6C6F"
  
  # Convert between formats
  %(prog)s convert -f base64 -t base16 "SGVsbG8="
  
  # Validate encoded data
  %(prog)s validate -f base64 "SGVsbG8="
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    subparsers.required = True
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode data to base format')
    encode_parser.add_argument('-f', '--format', 
                              choices=['base16', 'base32', 'base64'],
                              default='base64',
                              help='Encoding format (default: base64)')
    encode_parser.add_argument('input', nargs='?', help='Input data (or use stdin)')
    encode_parser.set_defaults(func=encode_command)
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode base-encoded data')
    decode_parser.add_argument('-f', '--format',
                              choices=['base16', 'base32', 'base64', 'auto'],
                              default='auto',
                              help='Encoding format (default: auto-detect)')
    decode_parser.add_argument('-b', '--binary', action='store_true',
                              help='Output raw binary data')
    decode_parser.add_argument('input', nargs='?', help='Encoded data (or use stdin)')
    decode_parser.set_defaults(func=decode_command)
    
    # Detect command
    detect_parser = subparsers.add_parser('detect', help='Auto-detect encoding format')
    detect_parser.add_argument('input', nargs='?', help='Encoded data (or use stdin)')
    detect_parser.set_defaults(func=detect_command)
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert between base formats')
    convert_parser.add_argument('-f', '--from-format',
                               choices=['base16', 'base32', 'base64', 'auto'],
                               default='auto',
                               help='Source format (default: auto-detect)')
    convert_parser.add_argument('-t', '--to-format',
                               choices=['base16', 'base32', 'base64'],
                               required=True,
                               help='Target format')
    convert_parser.add_argument('input', nargs='?', help='Encoded data (or use stdin)')
    convert_parser.set_defaults(func=convert_command)
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate encoded data')
    validate_parser.add_argument('-f', '--format',
                                choices=['base16', 'base32', 'base64'],
                                required=True,
                                help='Expected format')
    validate_parser.add_argument('input', nargs='?', help='Encoded data (or use stdin)')
    validate_parser.set_defaults(func=validate_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
