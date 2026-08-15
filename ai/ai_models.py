"""
 ============================================================
  MODULE/PLUGIN NAME: AIModels
  VERSION: 1.0.0
  MODULE CLASS: AIModels
  DESCRIPTION:
       AI model management system for loading and managing AI models

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

from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class ModelType(Enum):
    """Model types"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    MULTIMODAL = "multimodal"
    CODE = "code"
    EMBEDDING = "embedding"


class ModelProvider(Enum):
    """Model providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LOCAL = "local"
    HUGGINGFACE = "huggingface"
    CUSTOM = "custom"


class AIModels:
    """AI model manager"""
    
    def __init__(self):
        self.models: Dict[str, Dict] = {}
        self.active_model: Optional[str] = None
        self.model_stats: Dict[str, Dict] = {}
        self.notification_callback = None
        
    def set_notification_callback(self, callback):
        """Set callback for model notifications"""
        self.notification_callback = callback
        
    async def register(self, name: str, config: Dict[str, Any]) -> bool:
        """Register an AI model"""
        if name in self.models:
            return False
            
        self.models[name] = {
            'name': name,
            'type': config.get('type', ModelType.TEXT.value),
            'provider': config.get('provider', ModelProvider.LOCAL.value),
            'endpoint': config.get('endpoint'),
            'api_key': config.get('api_key'),
            'parameters': config.get('parameters', {}),
            'enabled': config.get('enabled', True),
            'max_tokens': config.get('max_tokens', 4096),
            'temperature': config.get('temperature', 0.7),
            'registered_at': datetime.now().isoformat(),
        }
        
        self.model_stats[name] = {
            'requests': 0,
            'tokens_used': 0,
            'errors': 0,
            'last_used': None,
        }
        
        return True
        
    async def unregister(self, name: str) -> bool:
        """Unregister an AI model"""
        if name not in self.models:
            return False
            
        del self.models[name]
        del self.model_stats[name]
        
        if self.active_model == name:
            self.active_model = None
            
        return True
                
    async def activate(self, name: str) -> bool:
        """Activate a model"""
        if name in self.models and self.models[name]['enabled']:
            self.active_model = name
            return True
        return False
        
    async def get_active(self) -> Optional[Dict]:
        """Get active model"""
        if self.active_model:
            return self.models.get(self.active_model)
        return None
        
    async def list_models(self) -> List[Dict]:
        """List all models"""
        return list(self.models.values())
        
    async def get_model(self, name: str) -> Optional[Dict]:
        """Get specific model"""
        return self.models.get(name)
        
    async def update_model(self, name: str, config: Dict[str, Any]) -> bool:
        """Update model configuration"""
        if name not in self.models:
            return False
            
        for key, value in config.items():
            if key in self.models[name]:
                self.models[name][key] = value
                
        return True
        
    async def enable_model(self, name: str) -> bool:
        """Enable a model"""
        if name in self.models:
            self.models[name]['enabled'] = True
            return True
        return False
        
    async def disable_model(self, name: str) -> bool:
        """Disable a model"""
        if name in self.models:
            self.models[name]['enabled'] = False
            if self.active_model == name:
                self.active_model = None
            return True
        return False
        
    async def record_usage(self, name: str, tokens: int = 0, error: bool = False):
        """Record model usage statistics"""
        if name in self.model_stats:
            self.model_stats[name]['requests'] += 1
            self.model_stats[name]['tokens_used'] += tokens
            self.model_stats[name]['last_used'] = datetime.now().isoformat()
            if error:
                self.model_stats[name]['errors'] += 1
                
    async def get_model_stats(self, name: str) -> Optional[Dict]:
        """Get model statistics"""
        return self.model_stats.get(name)
        
    async def get_all_stats(self) -> Dict[str, Dict]:
        """Get all model statistics"""
        return self.model_stats.copy()
        
    async def validate_model(self, name: str) -> bool:
        """Validate model configuration"""
        if name not in self.models:
            return False
            
        model = self.models[name]
        
        # Check required fields
        if not model.get('name'):
            return False
            
        # Check provider-specific requirements
        if model['provider'] == ModelProvider.OPENAI.value:
            return bool(model.get('api_key'))
        elif model['provider'] == ModelProvider.ANTHROPIC.value:
            return bool(model.get('api_key'))
        elif model['provider'] == ModelProvider.LOCAL.value:
            return bool(model.get('endpoint'))
            
        return True
