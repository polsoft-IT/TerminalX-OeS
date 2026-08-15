"""
 ============================================================
  MODULE/PLUGIN NAME: KernelConfigLoader
  VERSION: 1.0.0
  MODULE CLASS: KernelConfigLoader
  DESCRIPTION:
       Configuration loader for kernel module settings and parameters

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


class KernelConfigLoader:
    """Loader for kernel configuration"""

    def __init__(self, config_dir: str):
        self.config_dir = config_dir

    def load(self, filename: str = "events.json") -> Dict[str, Any]:
        """Load kernel configuration"""
        config_path = os.path.join(self.config_dir, filename)
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading kernel config: {e}")
                return {}
        return {}

    def save(self, config: Dict[str, Any], filename: str = "events.json") -> bool:
        """Save kernel configuration"""
        config_path = os.path.join(self.config_dir, filename)
        
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving kernel config: {e}")
            return False
