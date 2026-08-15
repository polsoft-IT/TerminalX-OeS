"""
Config - Configuration management
"""

import json
import os
from typing import Dict, Any, Optional


class Config:
    """Configuration manager"""
    
    def __init__(self, config_dir: str = None):
        self.config_dir = config_dir or os.path.join(
            os.path.dirname(__file__), '..', 'config'
        )
        self.configs: Dict[str, Any] = {}
        
    async def load(self):
        """Load all configuration files"""
        self._load_config('terminal', 'default.json')
        self._load_config('ai', 'ai_core.json')
        self._load_config('gui', 'gui_engine.json')
        self._load_config('kernel', 'events.json')
        self._load_config('network', 'network_core.json')
        self._load_config('shield', 'defender.json')
        self._load_config('cache', 'cache.json')
        self._load_config('cloud', 'cloud.json')
        
    def _load_config(self, module: str, filename: str):
        """Load a specific configuration file"""
        config_path = os.path.join(self.config_dir, module, filename)
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    self.configs[module] = json.load(f)
            except Exception as e:
                print(f"Error loading config {config_path}: {e}")
                self.configs[module] = {}
        else:
            self.configs[module] = {}
            
    def get(self, module: str, key: str = None, default: Any = None) -> Any:
        """Get configuration value"""
        if key is None:
            return self.configs.get(module, {})
        
        module_config = self.configs.get(module, {})
        if isinstance(module_config, dict):
            return module_config.get(key, default)
        return default
        
    def set(self, module: str, key: str, value: Any):
        """Set configuration value"""
        if module not in self.configs:
            self.configs[module] = {}
        self.configs[module][key] = value
        
    async def save(self, module: str):
        """Save configuration to file"""
        config_path = os.path.join(self.config_dir, module, f'{module}.json')
        
        try:
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(self.configs.get(module, {}), f, indent=2)
        except Exception as e:
            print(f"Error saving config {config_path}: {e}")
