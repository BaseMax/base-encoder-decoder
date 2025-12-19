#!/usr/bin/env python3
"""
Example demonstrations of the Base Encoder/Decoder Toolkit
"""

from base_codec import BaseCodec, EncodingFormat


def demo_basic_encoding():
    """Demonstrate basic encoding operations"""
    print("=" * 60)
    print("BASIC ENCODING DEMONSTRATION")
    print("=" * 60)
    
    text = "Hello, World!"
    print(f"\nOriginal text: {text}")
    print()
    
    # Encode to different formats
    base16 = BaseCodec.encode(text, EncodingFormat.BASE16)
    base32 = BaseCodec.encode(text, EncodingFormat.BASE32)
    base64 = BaseCodec.encode(text, EncodingFormat.BASE64)
    
    print(f"Base16 (Hexadecimal): {base16}")
    print(f"Base32:               {base32}")
    print(f"Base64:               {base64}")


def demo_auto_detection():
    """Demonstrate auto-detection feature"""
    print("\n" + "=" * 60)
    print("AUTO-DETECTION DEMONSTRATION")
    print("=" * 60)
    
    samples = [
        ("48656C6C6F", "Base16 example"),
        ("JBSWY3DP", "Base32 example"),
        ("SGVsbG8=", "Base64 example"),
        ("MFRGG===", "Another Base32 example"),
        ("VGVzdA==", "Another Base64 example"),
    ]
    
    for encoded, description in samples:
        detected = BaseCodec.detect_format(encoded)
        print(f"\n{description}")
        print(f"  Input:    {encoded}")
        print(f"  Detected: {detected.value}")
        
        if detected != EncodingFormat.UNKNOWN:
            try:
                decoded = BaseCodec.decode(encoded, detected)
                print(f"  Decoded:  {decoded.decode('utf-8')}")
            except:
                print(f"  Decoded:  (binary data)")


def demo_format_conversion():
    """Demonstrate format conversion"""
    print("\n" + "=" * 60)
    print("FORMAT CONVERSION DEMONSTRATION")
    print("=" * 60)
    
    original_text = "Convert me!"
    print(f"\nOriginal text: {original_text}")
    
    # Start with Base64
    base64_data = BaseCodec.encode(original_text, EncodingFormat.BASE64)
    print(f"\nBase64: {base64_data}")
    
    # Convert to Base16
    base16_data = BaseCodec.convert(base64_data, EncodingFormat.BASE64, EncodingFormat.BASE16)
    print(f"Converted to Base16: {base16_data}")
    
    # Convert to Base32
    base32_data = BaseCodec.convert(base16_data, EncodingFormat.BASE16, EncodingFormat.BASE32)
    print(f"Converted to Base32: {base32_data}")
    
    # Convert back to Base64
    back_to_base64 = BaseCodec.convert(base32_data, EncodingFormat.BASE32, EncodingFormat.BASE64)
    print(f"Back to Base64: {back_to_base64}")
    
    # Verify it's the same
    print(f"\nVerification: {back_to_base64 == base64_data}")


def demo_error_handling():
    """Demonstrate graceful error handling"""
    print("\n" + "=" * 60)
    print("ERROR HANDLING DEMONSTRATION")
    print("=" * 60)
    
    invalid_samples = [
        ("ZZZZZ", EncodingFormat.BASE16, "Invalid hex characters"),
        ("12345", EncodingFormat.BASE32, "Invalid Base32 characters"),
        ("!!!@@@", EncodingFormat.BASE64, "Invalid Base64 characters"),
        ("ABC", EncodingFormat.BASE16, "Odd length for Base16"),
    ]
    
    for sample, format, description in invalid_samples:
        print(f"\n{description}")
        print(f"  Input:  {sample}")
        print(f"  Format: {format.value}")
        
        is_valid = BaseCodec.is_valid(sample, format)
        print(f"  Valid:  {is_valid}")
        
        if not is_valid:
            try:
                BaseCodec.decode(sample, format)
            except ValueError as e:
                print(f"  Error:  {e}")


def demo_unicode_and_binary():
    """Demonstrate Unicode and binary data handling"""
    print("\n" + "=" * 60)
    print("UNICODE AND BINARY DATA DEMONSTRATION")
    print("=" * 60)
    
    # Unicode text
    unicode_text = "Hello 🌍 World! 你好 مرحبا"
    print(f"\nUnicode text: {unicode_text}")
    
    encoded = BaseCodec.encode(unicode_text, EncodingFormat.BASE64)
    print(f"Encoded: {encoded}")
    
    decoded = BaseCodec.decode(encoded, EncodingFormat.BASE64)
    print(f"Decoded: {decoded.decode('utf-8')}")
    
    # Binary data
    print("\n\nBinary data (bytes 0-15):")
    binary_data = bytes(range(16))
    print(f"Original: {binary_data.hex()}")
    
    encoded = BaseCodec.encode(binary_data, EncodingFormat.BASE64)
    print(f"Encoded:  {encoded}")
    
    decoded = BaseCodec.decode(encoded, EncodingFormat.BASE64)
    print(f"Decoded:  {decoded.hex()}")
    print(f"Match:    {decoded == binary_data}")


def demo_validation():
    """Demonstrate validation features"""
    print("\n" + "=" * 60)
    print("VALIDATION DEMONSTRATION")
    print("=" * 60)
    
    test_cases = [
        ("48656C6C6F", EncodingFormat.BASE16, True),
        ("GGGGGG", EncodingFormat.BASE16, False),
        ("JBSWY3DP", EncodingFormat.BASE32, True),
        ("12345", EncodingFormat.BASE32, False),
        ("SGVsbG8=", EncodingFormat.BASE64, True),
        ("@@@", EncodingFormat.BASE64, False),
    ]
    
    for data, format, expected in test_cases:
        is_valid = BaseCodec.is_valid(data, format)
        status = "✓" if is_valid == expected else "✗"
        print(f"{status} {data:20} as {format.value:8} -> {is_valid}")


def demo_pipeline_usage():
    """Demonstrate pipeline/chaining operations"""
    print("\n" + "=" * 60)
    print("PIPELINE USAGE DEMONSTRATION")
    print("=" * 60)
    
    print("\nExample: Secret message encoding pipeline")
    
    # Original message
    secret = "Secret Message"
    print(f"1. Original:     {secret}")
    
    # Encode to Base64
    step1 = BaseCodec.encode(secret, EncodingFormat.BASE64)
    print(f"2. Base64:       {step1}")
    
    # Convert to Base16
    step2 = BaseCodec.convert(step1, EncodingFormat.BASE64, EncodingFormat.BASE16)
    print(f"3. To Base16:    {step2}")
    
    # Convert to Base32
    step3 = BaseCodec.convert(step2, EncodingFormat.BASE16, EncodingFormat.BASE32)
    print(f"4. To Base32:    {step3}")
    
    # Decode back
    print("\nDecoding back:")
    back1 = BaseCodec.convert(step3, EncodingFormat.BASE32, EncodingFormat.BASE16)
    print(f"5. To Base16:    {back1}")
    
    back2 = BaseCodec.convert(back1, EncodingFormat.BASE16, EncodingFormat.BASE64)
    print(f"6. To Base64:    {back2}")
    
    back3 = BaseCodec.decode(back2, EncodingFormat.BASE64)
    print(f"7. Final:        {back3.decode('utf-8')}")
    
    print(f"\nMessage intact:  {back3.decode('utf-8') == secret}")


def main():
    """Run all demonstrations"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 8 + "Base Encoder/Decoder Toolkit Examples" + " " * 13 + "║")
    print("╚" + "=" * 58 + "╝")
    
    demo_basic_encoding()
    demo_auto_detection()
    demo_format_conversion()
    demo_error_handling()
    demo_unicode_and_binary()
    demo_validation()
    demo_pipeline_usage()
    
    print("\n" + "=" * 60)
    print("All demonstrations completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
