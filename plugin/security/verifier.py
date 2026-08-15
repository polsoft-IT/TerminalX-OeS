# ============================================================
#  PLUGIN VERIFIER — SIGNATURE VERIFICATION
#  Suf Terminal Hybrid Architecture (GODMODE / ULTRA / PRO)
#  AUTHOR: Sebastian Januchowski
#  COMPANY: polsoft.ITS™ Dev
# ============================================================

import os
import hashlib
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class VerificationResult:
    """Verification result"""
    valid: bool
    signature: str
    checksum: str
    errors: List[str]


class PluginVerifier:
    """
    PLUGIN SIGNATURE VERIFICATION:
    - Verify plugin signatures
    - Calculate checksums
    - Validate plugin integrity
    - Check for tampering
    """

    def __init__(self, logger: Optional[CleanLogger] = None):
        self.logger = logger or CleanLogger("PluginVerifier", LogLevel.INFO)
        self.signatures_file = "plugin/manifest/signatures.json"
        self.signatures: Dict[str, Dict[str, str]] = {}

    # ============================================================
    # SIGNATURE MANAGEMENT
    # ============================================================
    def load_signatures(self) -> bool:
        """Load signatures from file"""
        try:
            if not os.path.exists(self.signatures_file):
                self.logger.info(f"Signatures file not found: {self.signatures_file}")
                return True

            with open(self.signatures_file, "r") as f:
                self.signatures = json.load(f)

            self.logger.info(f"Signatures loaded: {len(self.signatures)} entries")
            return True

        except Exception as e:
            self.logger.error(f"Error loading signatures: {e}")
            return False

    def save_signatures(self) -> bool:
        """Save signatures to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.signatures_file), exist_ok=True)

            with open(self.signatures_file, "w") as f:
                json.dump(self.signatures, f, indent=4)

            self.logger.info(f"Signatures saved: {len(self.signatures)} entries")
            return True

        except Exception as e:
            self.logger.error(f"Error saving signatures: {e}")
            return False

    def add_signature(self, plugin_name: str, signature: str, checksum: str) -> bool:
        """Add signature for plugin"""
        self.signatures[plugin_name] = {
            "signature": signature,
            "checksum": checksum
        }
        self.logger.info(f"Signature added for: {plugin_name}")
        return True

    def remove_signature(self, plugin_name: str) -> bool:
        """Remove signature for plugin"""
        if plugin_name in self.signatures:
            del self.signatures[plugin_name]
            self.logger.info(f"Signature removed for: {plugin_name}")
            return True
        return False

    # ============================================================
    # CHECKSUM CALCULATION
    # ============================================================
    def calculate_checksum(self, plugin_path: str) -> Optional[str]:
        """Calculate checksum for plugin directory"""
        try:
            if not os.path.exists(plugin_path):
                self.logger.error(f"Plugin path not found: {plugin_path}")
                return None

            # Calculate SHA256 checksum of all files
            sha256_hash = hashlib.sha256()
            
            for root, dirs, files in os.walk(plugin_path):
                for file in sorted(files):
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        for chunk in iter(lambda: f.read(4096), b""):
                            sha256_hash.update(chunk)

            checksum = sha256_hash.hexdigest()
            self.logger.info(f"Checksum calculated for {plugin_path}: {checksum}")
            return checksum

        except Exception as e:
            self.logger.error(f"Error calculating checksum: {e}")
            return None

    def calculate_file_checksum(self, file_path: str) -> Optional[str]:
        """Calculate checksum for single file"""
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"File not found: {file_path}")
                return None

            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(chunk)

            checksum = sha256_hash.hexdigest()
            return checksum

        except Exception as e:
            self.logger.error(f"Error calculating file checksum: {e}")
            return None

    # ============================================================
    # VERIFICATION
    # ============================================================
    def verify(self, plugin_name: str, plugin_path: str) -> VerificationResult:
        """Verify plugin signature and checksum"""
        errors = []
        
        # Calculate current checksum
        current_checksum = self.calculate_checksum(plugin_path)
        if not current_checksum:
            errors.append("Failed to calculate checksum")
            return VerificationResult(False, "", "", errors)

        # Check if signature exists
        if plugin_name not in self.signatures:
            errors.append(f"No signature found for plugin: {plugin_name}")
            return VerificationResult(False, "", current_checksum, errors)

        stored_signature = self.signatures[plugin_name].get("signature", "")
        stored_checksum = self.signatures[plugin_name].get("checksum", "")

        # Verify checksum
        if current_checksum != stored_checksum:
            errors.append(f"Checksum mismatch: expected {stored_checksum}, got {current_checksum}")

        # Verify signature (simplified - in real implementation would use crypto)
        # For now, we just check if signature exists
        if not stored_signature:
            errors.append("No signature stored")

        valid = len(errors) == 0
        result = VerificationResult(valid, stored_signature, current_checksum, errors)
        
        if valid:
            self.logger.info(f"Plugin verified: {plugin_name}")
        else:
            self.logger.error(f"Plugin verification failed: {plugin_name} - {errors}")

        return result

    def verify_all(self, plugin_dir: str) -> Dict[str, VerificationResult]:
        """Verify all plugins in directory"""
        results = {}
        
        if not os.path.exists(plugin_dir):
            self.logger.error(f"Plugin directory not found: {plugin_dir}")
            return results

        for plugin_name in os.listdir(plugin_dir):
            plugin_path = os.path.join(plugin_dir, plugin_name)
            if os.path.isdir(plugin_path):
                results[plugin_name] = self.verify(plugin_name, plugin_path)

        return results

    # ============================================================
    # SIGNATURE GENERATION
    # ============================================================
    def generate_signature(self, plugin_path: str) -> Optional[str]:
        """Generate signature for plugin (simplified)"""
        # In real implementation, this would use cryptographic signing
        checksum = self.calculate_checksum(plugin_path)
        if not checksum:
            return None
        
        # Simplified signature (just hash of checksum)
        signature = hashlib.sha256(checksum.encode()).hexdigest()
        return signature

    def sign_plugin(self, plugin_name: str, plugin_path: str) -> bool:
        """Sign plugin"""
        checksum = self.calculate_checksum(plugin_path)
        if not checksum:
            return False

        signature = self.generate_signature(plugin_path)
        if not signature:
            return False

        self.add_signature(plugin_name, signature, checksum)
        self.save_signatures()
        
        self.logger.info(f"Plugin signed: {plugin_name}")
        return True

    # ============================================================
    # INTEGRITY CHECK
    # ============================================================
    def check_integrity(self, plugin_path: str) -> bool:
        """Check plugin file integrity"""
        try:
            # Check if all files are readable
            for root, dirs, files in os.walk(plugin_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "rb") as f:
                            f.read(1)
                    except Exception as e:
                        self.logger.error(f"File integrity check failed: {file_path} - {e}")
                        return False

            self.logger.info(f"Integrity check passed: {plugin_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error checking integrity: {e}")
            return False
