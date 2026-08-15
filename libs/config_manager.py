"""
 ============================================================
  MODULE/PLUGIN NAME: ConfigManager
  VERSION: 1.0.0
  MODULE CLASS: ConfigManager
  DESCRIPTION:
       Configuration management for TerminalX

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
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ConfigSnapshot:
    """Configuration snapshot"""
    name: str
    timestamp: str
    config: Dict[str, Any]
    description: str = ""


class ConfigManager:
    """Advanced configuration manager"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize config manager
        
        Args:
            config_dir: Configuration directory
        """
        self.config_dir = config_dir or Path.home() / ".terminalx"
        self.config_file = self.config_dir / "config.json"
        self.snapshots_dir = self.config_dir / "snapshots"
        self.current_config: Dict[str, Any] = {}
        self.snapshots: List[ConfigSnapshot] = []
        
        self._init_directories()
        self._load_config()
        
    def _init_directories(self) -> None:
        """Initialize configuration directories"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)
        
    def _load_config(self) -> None:
        """Load current configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.current_config = json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                self.current_config = {}
                
    def _save_config(self) -> None:
        """Save current configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.current_config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.current_config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
        
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value
        
        Args:
            key: Configuration key (supports dot notation)
            value: New value
        """
        keys = key.split('.')
        config = self.current_config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
        self._save_config()
        
    def delete(self, key: str) -> bool:
        """
        Delete configuration value
        
        Args:
            key: Configuration key
            
        Returns:
            True if deleted
        """
        keys = key.split('.')
        config = self.current_config
        
        for k in keys[:-1]:
            if isinstance(config, dict) and k in config:
                config = config[k]
            else:
                return False
                
        if keys[-1] in config:
            del config[keys[-1]]
            self._save_config()
            return True
            
        return False
        
    def create_snapshot(self, name: str, description: str = "") -> ConfigSnapshot:
        """
        Create configuration snapshot
        
        Args:
            name: Snapshot name
            description: Snapshot description
            
        Returns:
            Created snapshot
        """
        snapshot = ConfigSnapshot(
            name=name,
            timestamp=datetime.now().isoformat(),
            config=self.current_config.copy(),
            description=description
        )
        
        self.snapshots.append(snapshot)
        self._save_snapshot(snapshot)
        
        return snapshot
        
    def _save_snapshot(self, snapshot: ConfigSnapshot) -> None:
        """Save snapshot to file"""
        snapshot_file = self.snapshots_dir / f"{snapshot.name}.json"
        try:
            with open(snapshot_file, 'w') as f:
                json.dump({
                    'name': snapshot.name,
                    'timestamp': snapshot.timestamp,
                    'config': snapshot.config,
                    'description': snapshot.description
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving snapshot: {e}")
            
    def load_snapshot(self, name: str) -> bool:
        """
        Load configuration from snapshot
        
        Args:
            name: Snapshot name
            
        Returns:
            True if loaded successfully
        """
        snapshot_file = self.snapshots_dir / f"{name}.json"
        
        if not snapshot_file.exists():
            return False
            
        try:
            with open(snapshot_file, 'r') as f:
                data = json.load(f)
                
            self.current_config = data['config']
            self._save_config()
            
            return True
        except Exception as e:
            print(f"Error loading snapshot: {e}")
            return False
            
    def delete_snapshot(self, name: str) -> bool:
        """
        Delete snapshot
        
        Args:
            name: Snapshot name
            
        Returns:
            True if deleted
        """
        snapshot_file = self.snapshots_dir / f"{name}.json"
        
        if snapshot_file.exists():
            snapshot_file.unlink()
            self.snapshots = [s for s in self.snapshots if s.name != name]
            return True
            
        return False
        
    def list_snapshots(self) -> List[ConfigSnapshot]:
        """
        List all snapshots
        
        Returns:
            List of snapshots
        """
        # Reload from disk
        self.snapshots = []
        
        for snapshot_file in self.snapshots_dir.glob("*.json"):
            try:
                with open(snapshot_file, 'r') as f:
                    data = json.load(f)
                    
                snapshot = ConfigSnapshot(
                    name=data['name'],
                    timestamp=data['timestamp'],
                    config=data['config'],
                    description=data.get('description', '')
                )
                self.snapshots.append(snapshot)
            except Exception:
                pass
                
        return self.snapshots
        
    def reset_to_default(self) -> None:
        """Reset configuration to defaults"""
        self.current_config = {}
        self._save_config()
        
    def merge(self, other_config: Dict[str, Any]) -> None:
        """
        Merge another configuration
        
        Args:
            other_config: Configuration to merge
        """
        def deep_merge(base: Dict, update: Dict) -> Dict:
            """Deep merge dictionaries"""
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value
            return base
            
        deep_merge(self.current_config, other_config)
        self._save_config()
        
    def export(self, path: Path) -> bool:
        """
        Export configuration
        
        Args:
            path: Export path
            
        Returns:
            True if exported successfully
        """
        try:
            with open(path, 'w') as f:
                json.dump(self.current_config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False
            
    def import_config(self, path: Path) -> bool:
        """
        Import configuration
        
        Args:
            path: Import path
            
        Returns:
            True if imported successfully
        """
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                
            self.merge(data)
            return True
        except Exception as e:
            print(f"Error importing config: {e}")
            return False
            
    def get_stats(self) -> Dict[str, Any]:
        """
        Get configuration statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'config_keys': self._count_keys(self.current_config),
            'snapshots': len(self.list_snapshots()),
            'config_file': str(self.config_file),
            'snapshots_dir': str(self.snapshots_dir)
        }
        
    def _count_keys(self, config: Dict) -> int:
        """Count total keys in nested config"""
        count = 0
        for value in config.values():
            if isinstance(value, dict):
                count += self._count_keys(value)
            count += 1
        return count


# Global config manager instance
config_manager = ConfigManager()
