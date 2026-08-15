"""
 ============================================================
  MODULE/PLUGIN NAME: Config
  VERSION: 1.0.0
  MODULE CLASS: Config
  DESCRIPTION:
       Terminal configuration management for TerminalX

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
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class TerminalConfig:
    """Terminal configuration"""
    # General
    theme: str = "default"
    font_size: int = 12
    font_family: str = "Consolas"
    
    # Display
    enable_colors: bool = True
    enable_emoji: bool = True
    enable_unicode: bool = True
    line_numbers: bool = False
    
    # Behavior
    auto_save: bool = True
    auto_save_interval: int = 300
    command_history_size: int = 1000
    tab_completion: bool = True
    
    # Performance
    max_processes: int = 10
    cache_size: int = 100
    enable_hot_reload: bool = True
    
    # Security
    enable_sandbox: bool = False
    require_auth: bool = False
    log_sensitive: bool = False
    
    # GUI
    gui_enabled: bool = False
    framebuffer_width: int = 120
    framebuffer_height: int = 40
    
    # Network
    enable_network: bool = True
    proxy_enabled: bool = False
    proxy_host: str = ""
    proxy_port: int = 8080
    
    # AI
    ai_enabled: bool = True
    ai_model: str = "default"
    ai_timeout: int = 30
    
    # Modules
    auto_load_modules: bool = True
    module_paths: list = None
    
    def __post_init__(self):
        """Initialize defaults"""
        if self.module_paths is None:
            self.module_paths = []


class Config:
    """Configuration manager"""
    
    DEFAULT_PATH = Path.home() / ".terminalx" / "config.json"
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration
        
        Args:
            config_path: Path to config file
        """
        self.config_path = config_path or self.DEFAULT_PATH
        self.config = TerminalConfig()
        self._load()
        
    def _load(self) -> None:
        """Load configuration from file"""
        if not self.config_path.exists():
            self._save()
            return
            
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                
            # Update config with loaded data
            for key, value in data.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
                    
        except Exception as e:
            print(f"Error loading config: {e}")
            
    def _save(self) -> None:
        """Save configuration to file"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(asdict(self.config), f, indent=2)
                
        except Exception as e:
            print(f"Error saving config: {e}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return getattr(self.config, key, default)
        
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value
        
        Args:
            key: Configuration key
            value: New value
        """
        if hasattr(self.config, key):
            setattr(self.config, key, value)
            if self.config.auto_save:
                self._save()
                
    def reset(self) -> None:
        """Reset configuration to defaults"""
        self.config = TerminalConfig()
        self._save()
        
    def reload(self) -> None:
        """Reload configuration from file"""
        self._load()
        
    def export(self, path: Path) -> None:
        """
        Export configuration to file
        
        Args:
            path: Export path
        """
        try:
            with open(path, 'w') as f:
                json.dump(asdict(self.config), f, indent=2)
        except Exception as e:
            print(f"Error exporting config: {e}")
            
    def import_config(self, path: Path) -> None:
        """
        Import configuration from file
        
        Args:
            path: Import path
        """
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                
            for key, value in data.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
                    
            self._save()
        except Exception as e:
            print(f"Error importing config: {e}")
            
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary
        
        Returns:
            Configuration dictionary
        """
        return asdict(self.config)


# Global configuration instance
config = Config()
