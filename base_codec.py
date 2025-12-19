#!/usr/bin/env python3
"""
Base Encoder/Decoder Toolkit

Supports encoding and decoding of Base16, Base32, and Base64 formats.
Features auto-detection of input encoding and graceful error handling.
"""

import base64
import re
from typing import Optional, Tuple, Union
from enum import Enum


class EncodingFormat(Enum):
    """Supported encoding formats"""
    BASE16 = "base16"
    BASE32 = "base32"
    BASE64 = "base64"
    UNKNOWN = "unknown"


class BaseCodec:
    """
    Main class for encoding and decoding base formats.
    
    Supports Base16, Base32, and Base64 with auto-detection and error handling.
    """
    
    @staticmethod
    def encode(data: Union[str, bytes], format: EncodingFormat) -> str:
        """
        Encode data to the specified base format.
        
        Args:
            data: String or bytes to encode
            format: Target encoding format (BASE16, BASE32, or BASE64)
            
        Returns:
            Encoded string
            
        Raises:
            ValueError: If format is invalid or data cannot be encoded
        """
        try:
            # Convert string to bytes if necessary
            if isinstance(data, str):
                data_bytes = data.encode('utf-8')
            else:
                data_bytes = data
            
            if format == EncodingFormat.BASE16:
                return base64.b16encode(data_bytes).decode('ascii')
            elif format == EncodingFormat.BASE32:
                return base64.b32encode(data_bytes).decode('ascii')
            elif format == EncodingFormat.BASE64:
                return base64.b64encode(data_bytes).decode('ascii')
            else:
                raise ValueError(f"Unsupported encoding format: {format}")
        except Exception as e:
            raise ValueError(f"Encoding failed: {str(e)}")
    
    @staticmethod
    def decode(encoded_data: str, format: Optional[EncodingFormat] = None) -> bytes:
        """
        Decode base-encoded data.
        
        Args:
            encoded_data: Encoded string to decode
            format: Expected encoding format (if None, auto-detect)
            
        Returns:
            Decoded bytes
            
        Raises:
            ValueError: If data is invalid or cannot be decoded
        """
        # Auto-detect format if not provided
        if format is None:
            format = BaseCodec.detect_format(encoded_data)
            if format == EncodingFormat.UNKNOWN:
                raise ValueError("Unable to auto-detect encoding format")
        
        # Remove whitespace
        encoded_data = encoded_data.strip()
        
        try:
            if format == EncodingFormat.BASE16:
                return base64.b16decode(encoded_data, casefold=True)
            elif format == EncodingFormat.BASE32:
                return base64.b32decode(encoded_data, casefold=True)
            elif format == EncodingFormat.BASE64:
                return base64.b64decode(encoded_data, validate=True)
            else:
                raise ValueError(f"Unsupported encoding format: {format}")
        except Exception as e:
            raise ValueError(f"Decoding failed: {str(e)}")
    
    @staticmethod
    def detect_format(encoded_data: str) -> EncodingFormat:
        """
        Auto-detect the encoding format of the input data.
        
        Args:
            encoded_data: Encoded string to analyze
            
        Returns:
            Detected EncodingFormat
        """
        if not encoded_data or not encoded_data.strip():
            return EncodingFormat.UNKNOWN
        
        encoded_data = encoded_data.strip()
        
        # Base16 detection: only hexadecimal characters (0-9, A-F, case-insensitive)
        if re.fullmatch(r'[0-9A-Fa-f]+', encoded_data):
            # Additional check: Base16 should have even length
            if len(encoded_data) % 2 == 0:
                return EncodingFormat.BASE16
        
        # Base32 detection: only A-Z and 2-7, with optional padding (=)
        if re.fullmatch(r'[A-Z2-7]+=*', encoded_data, re.IGNORECASE):
            # Base32 padding should be valid (0-6 padding chars)
            padding = encoded_data.count('=')
            if padding <= 6:
                # Try to decode to verify
                try:
                    base64.b32decode(encoded_data, casefold=True)
                    return EncodingFormat.BASE32
                except:
                    pass
        
        # Base64 detection: A-Z, a-z, 0-9, +, /, with optional padding (=)
        if re.fullmatch(r'[A-Za-z0-9+/]+=*', encoded_data):
            # Base64 padding should be valid (0-2 padding chars)
            padding = encoded_data.count('=')
            if padding <= 2:
                # Check if length is valid for Base64 (multiple of 4, or needs padding)
                length_with_padding = len(encoded_data)
                if length_with_padding % 4 == 0:
                    # Try to decode to verify
                    try:
                        base64.b64decode(encoded_data, validate=True)
                        return EncodingFormat.BASE64
                    except:
                        pass
                elif padding == 0:
                    # Could be Base64 without padding or Base16, need to check
                    # Prefer Base16 if it's all hex (checked earlier)
                    # Only consider Base64 if it has non-hex characters
                    if not re.fullmatch(r'[0-9A-Fa-f]+', encoded_data):
                        return EncodingFormat.BASE64
        
        return EncodingFormat.UNKNOWN
    
    @staticmethod
    def convert(encoded_data: str, from_format: Optional[EncodingFormat], 
                to_format: EncodingFormat) -> str:
        """
        Convert from one base format to another.
        
        Args:
            encoded_data: Encoded string to convert
            from_format: Source encoding format (if None, auto-detect)
            to_format: Target encoding format
            
        Returns:
            Re-encoded string in the target format
            
        Raises:
            ValueError: If conversion fails
        """
        try:
            # Decode from source format
            decoded = BaseCodec.decode(encoded_data, from_format)
            # Encode to target format
            return BaseCodec.encode(decoded, to_format)
        except Exception as e:
            raise ValueError(f"Conversion failed: {str(e)}")
    
    @staticmethod
    def is_valid(encoded_data: str, format: EncodingFormat) -> bool:
        """
        Check if the encoded data is valid for the specified format.
        
        Args:
            encoded_data: Encoded string to validate
            format: Expected encoding format
            
        Returns:
            True if valid, False otherwise
        """
        try:
            BaseCodec.decode(encoded_data, format)
            return True
        except:
            return False


def main():
    """Example usage of the BaseCodec class"""
    
    # Example 1: Encoding
    print("=== Encoding Examples ===")
    text = "Hello, World!"
    print(f"Original: {text}")
    
    base16 = BaseCodec.encode(text, EncodingFormat.BASE16)
    print(f"Base16: {base16}")
    
    base32 = BaseCodec.encode(text, EncodingFormat.BASE32)
    print(f"Base32: {base32}")
    
    base64_encoded = BaseCodec.encode(text, EncodingFormat.BASE64)
    print(f"Base64: {base64_encoded}")
    
    # Example 2: Auto-detection and decoding
    print("\n=== Auto-detection Examples ===")
    
    samples = [
        base16,
        base32,
        base64_encoded
    ]
    
    for sample in samples:
        detected = BaseCodec.detect_format(sample)
        print(f"\nEncoded: {sample}")
        print(f"Detected format: {detected.value}")
        
        if detected != EncodingFormat.UNKNOWN:
            decoded = BaseCodec.decode(sample)
            print(f"Decoded: {decoded.decode('utf-8')}")
    
    # Example 3: Error handling
    print("\n=== Error Handling Examples ===")
    
    invalid_samples = [
        ("Invalid Base64!", EncodingFormat.BASE64),
        ("ZZZZZ", EncodingFormat.BASE32),
        ("XYZ", EncodingFormat.BASE16),
    ]
    
    for sample, format in invalid_samples:
        print(f"\nTesting: {sample} as {format.value}")
        is_valid = BaseCodec.is_valid(sample, format)
        print(f"Valid: {is_valid}")
    
    # Example 4: Format conversion
    print("\n=== Format Conversion Examples ===")
    base64_data = BaseCodec.encode("Test", EncodingFormat.BASE64)
    print(f"Base64: {base64_data}")
    
    converted_to_base16 = BaseCodec.convert(base64_data, EncodingFormat.BASE64, EncodingFormat.BASE16)
    print(f"Converted to Base16: {converted_to_base16}")
    
    converted_to_base32 = BaseCodec.convert(base64_data, EncodingFormat.BASE64, EncodingFormat.BASE32)
    print(f"Converted to Base32: {converted_to_base32}")


if __name__ == "__main__":
    main()
