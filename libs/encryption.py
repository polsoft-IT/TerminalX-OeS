"""
 ============================================================
  MODULE/PLUGIN NAME: Encryption
  VERSION: 1.0.0
  MODULE CLASS: Encryption
  DESCRIPTION:
       Data encryption utilities for TerminalX security

  AUTHOR:  Sebastian Januchowski
  COMPANY: polsoft.ITS™ Dev
  EMAIL:   polsoft.its@mail.com
  GITHUB:  polsoft-IT
  STATUS:  stable

 ============================================================
  COMPATIBILITY
 ============================================================
  PYTHON: 3.10+
  OS: Windows / Linux / macOS / Android (TerminalOS Runtime)
  ARCH: x86_64 / ARM64
  TERMINALOS KERNEL: v1.0+
"""

import hashlib
import base64
import os
from typing import Optional, Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from libs.clean_logger import CleanLogger, LogLevel


class Encryption:
    """Data encryption utilities"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize encryption utilities
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("Encryption", LogLevel.INFO)
        self._fernet: Optional[Fernet] = None
        
    def generate_key(self, password: Optional[str] = None, salt: Optional[bytes] = None) -> bytes:
        """
        Generate encryption key
        
        Args:
            password: Optional password for key derivation
            salt: Optional salt for key derivation
            
        Returns:
            Encryption key
        """
        if password:
            salt = salt or os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            return key
        else:
            return Fernet.generate_key()
            
    def set_key(self, key: bytes) -> None:
        """
        Set encryption key
        
        Args:
            key: Encryption key
        """
        self._fernet = Fernet(key)
        self.logger.info("Encryption key set")
        
    def encrypt(self, data: Union[str, bytes]) -> Optional[bytes]:
        """
        Encrypt data
        
        Args:
            data: Data to encrypt
            
        Returns:
            Encrypted data or None if error
        """
        if not self._fernet:
            self.logger.error("No encryption key set")
            return None
            
        try:
            if isinstance(data, str):
                data = data.encode()
            encrypted = self._fernet.encrypt(data)
            return encrypted
        except Exception as e:
            self.logger.error(f"Encryption failed: {e}")
            return None
            
    def decrypt(self, encrypted_data: bytes) -> Optional[str]:
        """
        Decrypt data
        
        Args:
            encrypted_data: Encrypted data
            
        Returns:
            Decrypted string or None if error
        """
        if not self._fernet:
            self.logger.error("No encryption key set")
            return None
            
        try:
            decrypted = self._fernet.decrypt(encrypted_data)
            return decrypted.decode()
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            return None
            
    def encrypt_file(self, file_path: str, output_path: Optional[str] = None) -> bool:
        """
        Encrypt file
        
        Args:
            file_path: Input file path
            output_path: Output file path (default: input + .enc)
            
        Returns:
            True if encrypted successfully
        """
        if not self._fernet:
            self.logger.error("No encryption key set")
            return False
            
        output_path = output_path or file_path + '.enc'
        
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                
            encrypted = self.encrypt(data)
            if encrypted:
                with open(output_path, 'wb') as f:
                    f.write(encrypted)
                self.logger.info(f"File encrypted: {output_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"File encryption failed: {e}")
            return False
            
    def decrypt_file(self, file_path: str, output_path: Optional[str] = None) -> bool:
        """
        Decrypt file
        
        Args:
            file_path: Input file path
            output_path: Output file path (default: input without .enc)
            
        Returns:
            True if decrypted successfully
        """
        if not self._fernet:
            self.logger.error("No encryption key set")
            return False
            
        output_path = output_path or file_path.replace('.enc', '')
        
        try:
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
                
            decrypted = self.decrypt(encrypted_data)
            if decrypted:
                with open(output_path, 'w') as f:
                    f.write(decrypted)
                self.logger.info(f"File decrypted: {output_path}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"File decryption failed: {e}")
            return False
            
    def hash_data(self, data: Union[str, bytes], algorithm: str = 'sha256') -> str:
        """
        Hash data
        
        Args:
            data: Data to hash
            algorithm: Hash algorithm (md5, sha1, sha256, sha512)
            
        Returns:
            Hash string
        """
        try:
            if isinstance(data, str):
                data = data.encode()
                
            if algorithm == 'md5':
                hash_obj = hashlib.md5()
            elif algorithm == 'sha1':
                hash_obj = hashlib.sha1()
            elif algorithm == 'sha512':
                hash_obj = hashlib.sha512()
            else:
                hash_obj = hashlib.sha256()
                
            hash_obj.update(data)
            return hash_obj.hexdigest()
        except Exception as e:
            self.logger.error(f"Hashing failed: {e}")
            return ""
            
    def hash_file(self, file_path: str, algorithm: str = 'sha256') -> str:
        """
        Hash file
        
        Args:
            file_path: File path
            algorithm: Hash algorithm
            
        Returns:
            Hash string
        """
        try:
            hash_obj = hashlib.sha256() if algorithm == 'sha256' else hashlib.md5()
            
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_obj.update(chunk)
                    
            return hash_obj.hexdigest()
        except Exception as e:
            self.logger.error(f"File hashing failed: {e}")
            return ""
            
    def verify_hash(self, data: Union[str, bytes], expected_hash: str, algorithm: str = 'sha256') -> bool:
        """
        Verify data hash
        
        Args:
            data: Data to verify
            expected_hash: Expected hash
            algorithm: Hash algorithm
            
        Returns:
            True if hash matches
        """
        actual_hash = self.hash_data(data, algorithm)
        return actual_hash == expected_hash.lower()
        
    def verify_file_hash(self, file_path: str, expected_hash: str, algorithm: str = 'sha256') -> bool:
        """
        Verify file hash
        
        Args:
            file_path: File path
            expected_hash: Expected hash
            algorithm: Hash algorithm
            
        Returns:
            True if hash matches
        """
        actual_hash = self.hash_file(file_path, algorithm)
        return actual_hash == expected_hash.lower()
        
    def generate_random_bytes(self, length: int = 32) -> bytes:
        """
        Generate random bytes
        
        Args:
            length: Number of bytes
            
        Returns:
            Random bytes
        """
        return os.urandom(length)
        
    def encode_base64(self, data: Union[str, bytes]) -> str:
        """
        Encode data to base64
        
        Args:
            data: Data to encode
            
        Returns:
            Base64 encoded string
        """
        if isinstance(data, str):
            data = data.encode()
        return base64.b64encode(data).decode()
        
    def decode_base64(self, encoded: str) -> Optional[str]:
        """
        Decode base64 data
        
        Args:
            encoded: Base64 encoded string
            
        Returns:
            Decoded string or None if error
        """
        try:
            decoded = base64.b64decode(encoded)
            return decoded.decode()
        except Exception as e:
            self.logger.error(f"Base64 decode failed: {e}")
            return None


# Global encryption instance
encryption = Encryption()
