"""
 ============================================================
  MODULE/PLUGIN NAME: MetadataModule
  VERSION: 1.0.0
  MODULE CLASS: MetadataModule
  DESCRIPTION:
       Advanced metadata scanner, editor, creator and remover. Supports all known metadata types: file, media, EXIF, ID3, PDF, DOCX, ZIP, TAR, custom tags, extended attrs, JSON sidecars, YAML sidecars, binary headers, magic blocks

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

import os
import json
import yaml
import time
import traceback
from typing import Any, Dict, List, Optional, Union

# ============================================================
#  RETRY POLICY (PLUGIN COMPATIBLE)
# ============================================================

def retry(operation, retries=3, delay=0.2):
    for attempt in range(1, retries + 1):
        try:
            return operation()
        except Exception:
            if attempt == retries:
                raise
            time.sleep(delay)

# ============================================================
#  METADATA SCANNERS — ALL TYPES
# ============================================================

class MetadataScanner:
    """Universal metadata scanner for all supported formats."""

    def scan(self, path: str) -> Dict[str, Any]:
        """Auto-detect metadata type and scan."""
        if not os.path.exists(path):
            return {"error": "File not found"}

        ext = os.path.splitext(path)[1].lower()

        # Universal metadata container
        meta = {
            "file": self.scan_file(path),
            "extended": self.scan_extended_attrs(path),
            "magic": self.scan_magic_header(path),
        }

        # Format-specific
        if ext in [".jpg", ".jpeg", ".png", ".webp"]:
            meta["exif"] = self.scan_exif(path)
        if ext in [".mp3", ".wav", ".flac"]:
            meta["id3"] = self.scan_id3(path)
        if ext == ".pdf":
            meta["pdf"] = self.scan_pdf(path)
        if ext in [".docx"]:
            meta["docx"] = self.scan_docx(path)
        if ext in [".zip", ".tar", ".gz", ".7z"]:
            meta["archive"] = self.scan_archive(path)

        # Sidecars
        meta["sidecar"] = self.scan_sidecars(path)

        return meta

    # ------------------------------------------------------------
    # BASIC FILE METADATA
    # ------------------------------------------------------------

    def scan_file(self, path: str):
        stat = os.stat(path)
        return {
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "mode": stat.st_mode,
        }

    # ------------------------------------------------------------
    # EXTENDED ATTRIBUTES (Linux, macOS, NTFS ADS)
    # ------------------------------------------------------------

    def scan_extended_attrs(self, path: str):
        try:
            if hasattr(os, "listxattr"):
                attrs = os.listxattr(path)
                return {a: os.getxattr(path, a).decode("utf-8", "ignore") for a in attrs}
        except Exception:
            return {}
        return {}

    # ------------------------------------------------------------
    # MAGIC HEADER (first 32 bytes)
    # ------------------------------------------------------------

    def scan_magic_header(self, path: str):
        try:
            with open(path, "rb") as f:
                return f.read(32).hex()
        except Exception:
            return None

    # ------------------------------------------------------------
    # EXIF
    # ------------------------------------------------------------

    def scan_exif(self, path: str):
        try:
            from PIL import Image
            img = Image.open(path)
            exif = img.getexif()
            return {str(k): str(v) for k, v in exif.items()}
        except Exception:
            return {}

    # ------------------------------------------------------------
    # ID3
    # ------------------------------------------------------------

    def scan_id3(self, path: str):
        try:
            from mutagen import File
            audio = File(path)
            return dict(audio.tags)
        except Exception:
            return {}

    # ------------------------------------------------------------
    # PDF
    # ------------------------------------------------------------

    def scan_pdf(self, path: str):
        try:
            from PyPDF2 import PdfReader
            pdf = PdfReader(path)
            return pdf.metadata
        except Exception:
            return {}

    # ------------------------------------------------------------
    # DOCX
    # ------------------------------------------------------------

    def scan_docx(self, path: str):
        try:
            import docx
            doc = docx.Document(path)
            core = doc.core_properties
            return {
                "author": core.author,
                "title": core.title,
                "subject": core.subject,
                "created": core.created,
                "modified": core.modified,
            }
        except Exception:
            return {}

    # ------------------------------------------------------------
    # ARCHIVES
    # ------------------------------------------------------------

    def scan_archive(self, path: str):
        try:
            import zipfile
            if zipfile.is_zipfile(path):
                with zipfile.ZipFile(path) as z:
                    return {"files": z.namelist()}
        except Exception:
            return {}
        return {}

    # ------------------------------------------------------------
    # SIDECARS (.json, .yaml)
    # ------------------------------------------------------------

    def scan_sidecars(self, path: str):
        base = os.path.splitext(path)[0]
        out = {}

        json_path = base + ".json"
        yaml_path = base + ".yaml"

        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    out["json"] = json.load(f)
            except Exception:
                pass

        if os.path.exists(yaml_path):
            try:
                with open(yaml_path, "r", encoding="utf-8") as f:
                    out["yaml"] = yaml.safe_load(f)
            except Exception:
                pass

        return out

# ============================================================
#  METADATA EDITOR
# ============================================================

class MetadataEditor:
    """Mass editor for all metadata types."""

    def set_sidecar(self, path: str, data: Dict[str, Any]):
        base = os.path.splitext(path)[0]
        json_path = base + ".json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def remove_sidecar(self, path: str):
        base = os.path.splitext(path)[0]
        for ext in [".json", ".yaml"]:
            p = base + ext
            if os.path.exists(p):
                os.remove(p)

    def mass_update(self, files: List[str], key: str, value: Any):
        """Mass update JSON sidecar metadata."""
        for f in files:
            base = os.path.splitext(f)[0]
            json_path = base + ".json"
            data = {}
            if os.path.exists(json_path):
                try:
                    with open(json_path, "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                except Exception:
                    data = {}
            data[key] = value
            with open(json_path, "w", encoding="utf-8") as fp:
                json.dump(data, fp, indent=4)

# ============================================================
#  PLUGIN SYSTEM
# ============================================================

class MetadataPlugin:
    """Base class for metadata plugins."""

    def apply(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        return metadata


class MetadataPluginManager:
    def __init__(self):
        self.plugins: List[MetadataPlugin] = []

    def register(self, plugin: MetadataPlugin):
        self.plugins.append(plugin)

    def apply_all(self, metadata: Dict[str, Any]):
        for p in self.plugins:
            try:
                metadata = retry(lambda: p.apply(metadata))
            except Exception:
                traceback.print_exc()
        return metadata

# ============================================================
#  MAIN MODULE CLASS
# ============================================================

class MetadataModule:
    def __init__(self):
        self.scanner = MetadataScanner()
        self.editor = MetadataEditor()
        self.plugins = MetadataPluginManager()
        self.notification_callback = None
        self.stats = {
            'files_scanned': 0,
            'files_updated': 0,
            'sidecars_created': 0,
            'sidecars_removed': 0,
            'errors': 0,
        }
        
    def set_notification_callback(self, callback):
        """Set callback for metadata notifications"""
        self.notification_callback = callback
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize metadata module"""
        self.config = config or {}
        
    def scan(self, path: str):
        try:
            meta = retry(lambda: self.scanner.scan(path))
            self.stats['files_scanned'] += 1
            return self.plugins.apply_all(meta)
        except Exception as e:
            self.stats['errors'] += 1
            return {"error": str(e)}

    def update(self, files: List[str], key: str, value: Any):
        try:
            result = retry(lambda: self.editor.mass_update(files, key, value))
            self.stats['files_updated'] += len(files)
            return result
        except Exception as e:
            self.stats['errors'] += 1
            return {"error": str(e)}

    def sidecar(self, path: str, data: Dict[str, Any]):
        try:
            result = retry(lambda: self.editor.set_sidecar(path, data))
            self.stats['sidecars_created'] += 1
            return result
        except Exception as e:
            self.stats['errors'] += 1
            return {"error": str(e)}

    def remove_sidecar(self, path: str):
        try:
            result = retry(lambda: self.editor.remove_sidecar(path))
            self.stats['sidecars_removed'] += 1
            return result
        except Exception as e:
            self.stats['errors'] += 1
            return {"error": str(e)}

    def register_plugin(self, plugin: MetadataPlugin):
        self.plugins.register(plugin)
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get metadata statistics"""
        return self.stats.copy()
        
    async def clear_stats(self):
        """Clear statistics"""
        self.stats = {
            'files_scanned': 0,
            'files_updated': 0,
            'sidecars_created': 0,
            'sidecars_removed': 0,
            'errors': 0,
        }
