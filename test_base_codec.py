#!/usr/bin/env python3
"""
Unit tests for Base Encoder/Decoder Toolkit
"""

import unittest
from base_codec import BaseCodec, EncodingFormat


class TestBaseCodecEncoding(unittest.TestCase):
    """Test encoding functionality"""
    
    def test_encode_base16(self):
        """Test Base16 encoding"""
        result = BaseCodec.encode("Hello", EncodingFormat.BASE16)
        self.assertEqual(result, "48656C6C6F")
    
    def test_encode_base32(self):
        """Test Base32 encoding"""
        result = BaseCodec.encode("Hello", EncodingFormat.BASE32)
        self.assertEqual(result, "JBSWY3DP")
    
    def test_encode_base64(self):
        """Test Base64 encoding"""
        result = BaseCodec.encode("Hello", EncodingFormat.BASE64)
        self.assertEqual(result, "SGVsbG8=")
    
    def test_encode_bytes(self):
        """Test encoding bytes"""
        data = b"Test"
        result = BaseCodec.encode(data, EncodingFormat.BASE64)
        self.assertEqual(result, "VGVzdA==")
    
    def test_encode_empty_string(self):
        """Test encoding empty string"""
        result = BaseCodec.encode("", EncodingFormat.BASE64)
        self.assertEqual(result, "")
    
    def test_encode_unicode(self):
        """Test encoding Unicode characters"""
        result = BaseCodec.encode("Hello 🌍", EncodingFormat.BASE64)
        decoded = BaseCodec.decode(result, EncodingFormat.BASE64)
        self.assertEqual(decoded.decode('utf-8'), "Hello 🌍")
    
    def test_encode_invalid_format(self):
        """Test encoding with invalid format"""
        with self.assertRaises(ValueError):
            BaseCodec.encode("Hello", EncodingFormat.UNKNOWN)


class TestBaseCodecDecoding(unittest.TestCase):
    """Test decoding functionality"""
    
    def test_decode_base16(self):
        """Test Base16 decoding"""
        result = BaseCodec.decode("48656C6C6F", EncodingFormat.BASE16)
        self.assertEqual(result.decode('utf-8'), "Hello")
    
    def test_decode_base32(self):
        """Test Base32 decoding"""
        result = BaseCodec.decode("JBSWY3DP", EncodingFormat.BASE32)
        self.assertEqual(result.decode('utf-8'), "Hello")
    
    def test_decode_base64(self):
        """Test Base64 decoding"""
        result = BaseCodec.decode("SGVsbG8=", EncodingFormat.BASE64)
        self.assertEqual(result.decode('utf-8'), "Hello")
    
    def test_decode_with_whitespace(self):
        """Test decoding with leading/trailing whitespace"""
        result = BaseCodec.decode("  SGVsbG8=  ", EncodingFormat.BASE64)
        self.assertEqual(result.decode('utf-8'), "Hello")
    
    def test_decode_base16_case_insensitive(self):
        """Test Base16 decoding is case-insensitive"""
        result1 = BaseCodec.decode("48656c6c6f", EncodingFormat.BASE16)
        result2 = BaseCodec.decode("48656C6C6F", EncodingFormat.BASE16)
        self.assertEqual(result1, result2)
    
    def test_decode_base32_case_insensitive(self):
        """Test Base32 decoding is case-insensitive"""
        result1 = BaseCodec.decode("jbswy3dp", EncodingFormat.BASE32)
        result2 = BaseCodec.decode("JBSWY3DP", EncodingFormat.BASE32)
        self.assertEqual(result1, result2)
    
    def test_decode_invalid_base16(self):
        """Test decoding invalid Base16 data"""
        with self.assertRaises(ValueError):
            BaseCodec.decode("ZZZZZ", EncodingFormat.BASE16)
    
    def test_decode_invalid_base32(self):
        """Test decoding invalid Base32 data"""
        with self.assertRaises(ValueError):
            BaseCodec.decode("1111", EncodingFormat.BASE32)
    
    def test_decode_invalid_base64(self):
        """Test decoding invalid Base64 data"""
        with self.assertRaises(ValueError):
            BaseCodec.decode("@@@", EncodingFormat.BASE64)
    
    def test_decode_empty_string(self):
        """Test decoding empty string"""
        result = BaseCodec.decode("", EncodingFormat.BASE64)
        self.assertEqual(result, b"")


class TestBaseCodecAutoDetection(unittest.TestCase):
    """Test auto-detection functionality"""
    
    def test_detect_base16(self):
        """Test detecting Base16 format"""
        result = BaseCodec.detect_format("48656C6C6F")
        self.assertEqual(result, EncodingFormat.BASE16)
    
    def test_detect_base16_lowercase(self):
        """Test detecting Base16 format (lowercase)"""
        result = BaseCodec.detect_format("48656c6c6f")
        self.assertEqual(result, EncodingFormat.BASE16)
    
    def test_detect_base32(self):
        """Test detecting Base32 format"""
        result = BaseCodec.detect_format("JBSWY3DP")
        self.assertEqual(result, EncodingFormat.BASE32)
    
    def test_detect_base32_with_padding(self):
        """Test detecting Base32 format with padding"""
        result = BaseCodec.detect_format("JBSWY3DPEQ======")
        self.assertEqual(result, EncodingFormat.BASE32)
    
    def test_detect_base64(self):
        """Test detecting Base64 format"""
        result = BaseCodec.detect_format("SGVsbG8=")
        self.assertEqual(result, EncodingFormat.BASE64)
    
    def test_detect_base64_no_padding(self):
        """Test detecting Base64 format without padding"""
        result = BaseCodec.detect_format("SGVsbG8")
        # This could be detected as BASE16 or BASE64, but should be one of them
        self.assertIn(result, [EncodingFormat.BASE16, EncodingFormat.BASE64])
    
    def test_detect_unknown(self):
        """Test detecting unknown format"""
        result = BaseCodec.detect_format("Invalid@Data!")
        self.assertEqual(result, EncodingFormat.UNKNOWN)
    
    def test_detect_empty(self):
        """Test detecting empty string"""
        result = BaseCodec.detect_format("")
        self.assertEqual(result, EncodingFormat.UNKNOWN)
    
    def test_decode_with_auto_detection(self):
        """Test decoding with auto-detection"""
        # Base64
        result = BaseCodec.decode("SGVsbG8=")
        self.assertEqual(result.decode('utf-8'), "Hello")
        
        # Base32
        result = BaseCodec.decode("JBSWY3DP")
        self.assertEqual(result.decode('utf-8'), "Hello")
        
        # Base16
        result = BaseCodec.decode("48656C6C6F")
        self.assertEqual(result.decode('utf-8'), "Hello")
    
    def test_decode_auto_detection_failure(self):
        """Test decoding with failed auto-detection"""
        with self.assertRaises(ValueError):
            BaseCodec.decode("Invalid@Data!")


class TestBaseCodecValidation(unittest.TestCase):
    """Test validation functionality"""
    
    def test_is_valid_base16(self):
        """Test validating Base16 data"""
        self.assertTrue(BaseCodec.is_valid("48656C6C6F", EncodingFormat.BASE16))
        self.assertFalse(BaseCodec.is_valid("ZZZZZ", EncodingFormat.BASE16))
    
    def test_is_valid_base32(self):
        """Test validating Base32 data"""
        self.assertTrue(BaseCodec.is_valid("JBSWY3DP", EncodingFormat.BASE32))
        self.assertFalse(BaseCodec.is_valid("1111", EncodingFormat.BASE32))
    
    def test_is_valid_base64(self):
        """Test validating Base64 data"""
        self.assertTrue(BaseCodec.is_valid("SGVsbG8=", EncodingFormat.BASE64))
        self.assertFalse(BaseCodec.is_valid("@@@", EncodingFormat.BASE64))


class TestBaseCodecConversion(unittest.TestCase):
    """Test format conversion functionality"""
    
    def test_convert_base64_to_base16(self):
        """Test converting from Base64 to Base16"""
        result = BaseCodec.convert("SGVsbG8=", EncodingFormat.BASE64, EncodingFormat.BASE16)
        self.assertEqual(result, "48656C6C6F")
    
    def test_convert_base64_to_base32(self):
        """Test converting from Base64 to Base32"""
        result = BaseCodec.convert("SGVsbG8=", EncodingFormat.BASE64, EncodingFormat.BASE32)
        self.assertEqual(result, "JBSWY3DP")
    
    def test_convert_base16_to_base64(self):
        """Test converting from Base16 to Base64"""
        result = BaseCodec.convert("48656C6C6F", EncodingFormat.BASE16, EncodingFormat.BASE64)
        self.assertEqual(result, "SGVsbG8=")
    
    def test_convert_base32_to_base64(self):
        """Test converting from Base32 to Base64"""
        result = BaseCodec.convert("JBSWY3DP", EncodingFormat.BASE32, EncodingFormat.BASE64)
        self.assertEqual(result, "SGVsbG8=")
    
    def test_convert_with_auto_detection(self):
        """Test converting with auto-detection"""
        result = BaseCodec.convert("SGVsbG8=", None, EncodingFormat.BASE16)
        self.assertEqual(result, "48656C6C6F")
    
    def test_convert_invalid_data(self):
        """Test converting invalid data"""
        with self.assertRaises(ValueError):
            BaseCodec.convert("Invalid@@@", EncodingFormat.BASE64, EncodingFormat.BASE16)


class TestBaseCodecEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""
    
    def test_long_data(self):
        """Test encoding/decoding long data"""
        long_text = "A" * 10000
        encoded = BaseCodec.encode(long_text, EncodingFormat.BASE64)
        decoded = BaseCodec.decode(encoded, EncodingFormat.BASE64)
        self.assertEqual(decoded.decode('utf-8'), long_text)
    
    def test_binary_data(self):
        """Test encoding/decoding binary data"""
        binary_data = bytes(range(256))
        encoded = BaseCodec.encode(binary_data, EncodingFormat.BASE64)
        decoded = BaseCodec.decode(encoded, EncodingFormat.BASE64)
        self.assertEqual(decoded, binary_data)
    
    def test_special_characters(self):
        """Test encoding/decoding special characters"""
        special = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        encoded = BaseCodec.encode(special, EncodingFormat.BASE64)
        decoded = BaseCodec.decode(encoded, EncodingFormat.BASE64)
        self.assertEqual(decoded.decode('utf-8'), special)
    
    def test_multiline_text(self):
        """Test encoding/decoding multiline text"""
        multiline = "Line 1\nLine 2\nLine 3"
        encoded = BaseCodec.encode(multiline, EncodingFormat.BASE64)
        decoded = BaseCodec.decode(encoded, EncodingFormat.BASE64)
        self.assertEqual(decoded.decode('utf-8'), multiline)


if __name__ == '__main__':
    unittest.main()
