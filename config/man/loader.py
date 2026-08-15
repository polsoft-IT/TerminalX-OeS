"""
 ============================================================
  MODULE/PLUGIN NAME: ManConfigLoader
  VERSION: 1.0.0
  MODULE CLASS: ManConfigLoader
  DESCRIPTION:
       Configuration loader for man module settings and parameters

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

import json
import os
from typing import Dict, Any, Optional


class ManConfigLoader:
    """Loader for man configuration"""

    def __init__(self, config_dir: str):
        self.config_dir = config_dir

    def load(self, filename: str = "man.json") -> Dict[str, Any]:
        """Load man configuration"""
        config_path = os.path.join(self.config_dir, filename)
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading man config: {e}")
                return {}
        
        # Default configuration
        return {
            "enabled": True,
            "cache": {
                "enabled": True,
                "max_memory_size": 100,
                "max_disk_size": 1000,
                "ttl": 3600,
                "policy": "lru"
            },
            "parser": {
                "default_format": "md"
            },
            "viewer": {
                "default_format": "ansi",
                "terminal_width": 80,
                "terminal_height": 24,
                "colors_enabled": True
            },
            "load_external": False,
            "man_path": "/usr/share/man"
        }

    def save(self, config: Dict[str, Any], filename: str = "man.json") -> bool:
        """Save man configuration"""
        config_path = os.path.join(self.config_dir, filename)
        
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving man config: {e}")
            return False
