"""
 ============================================================
  MODULE/PLUGIN NAME: AICore
  VERSION: 1.0.0
  MODULE CLASS: AICore
  DESCRIPTION:
       Main AI engine for TerminalX artificial intelligence operations

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

import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum


class MessageRole(Enum):
    """Message roles in conversation"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class AICore:
    """Main AI engine"""
    
    def __init__(self):
        self.enabled = False
        self.config: Dict[str, Any] = {}
        self.models: Dict[str, Any] = {}
        self.context: List[Dict] = []
        self.max_context = 100
        self.conversation_history: Dict[str, List[Dict]] = {}
        self.active_conversation: Optional[str] = None
        self.notification_callback = None
        self.stats = {
            'total_requests': 0,
            'total_tokens': 0,
            'errors': 0,
        }
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize AI core"""
        self.config = config or {}
        self.enabled = self.config.get('enabled', False)
        
        if self.enabled:
            self.max_context = self.config.get('max_context', 100)
            self.active_conversation = self.config.get('default_conversation', 'default')
            self.conversation_history[self.active_conversation] = []
            
    def set_notification_callback(self, callback):
        """Set callback for AI notifications"""
        self.notification_callback = callback
            
    async def process(self, input_text: str, conversation_id: str = None, context: Optional[List] = None) -> Dict[str, Any]:
        """Process input with AI"""
        self.stats['total_requests'] += 1
        
        if not self.enabled:
            return {
                'success': False,
                'error': 'AI is not enabled',
                'response': None
            }
            
        # Use specified conversation or active one
        conv_id = conversation_id or self.active_conversation
        if conv_id not in self.conversation_history:
            self.conversation_history[conv_id] = []
            
        conversation = self.conversation_history[conv_id]
        
        # Add user message to conversation
        user_message = {
            'role': MessageRole.USER.value,
            'content': input_text,
            'timestamp': datetime.now().isoformat(),
        }
        conversation.append(user_message)
        
        # Trim conversation if needed
        if len(conversation) > self.max_context:
            conversation = conversation[-self.max_context:]
            self.conversation_history[conv_id] = conversation
            
        try:
            # Process (placeholder for actual AI processing)
            response = await self._generate_response(input_text, conversation)
            
            # Add assistant response to conversation
            assistant_message = {
                'role': MessageRole.ASSISTANT.value,
                'content': response,
                'timestamp': datetime.now().isoformat(),
            }
            conversation.append(assistant_message)
            
            # Update stats
            self.stats['total_tokens'] += len(input_text) + len(response)
            
            return {
                'success': True,
                'response': response,
                'conversation_id': conv_id,
                'tokens_used': len(input_text) + len(response),
            }
            
        except Exception as e:
            self.stats['errors'] += 1
            return {
                'success': False,
                'error': str(e),
                'response': None
            }
        
    async def _generate_response(self, input_text: str, conversation: List) -> str:
        """Generate AI response (placeholder)"""
        # This would connect to actual AI models
        # For now, provide a simple contextual response
        
        # Check for common patterns
        input_lower = input_text.lower()
        
        if 'hello' in input_lower or 'hi' in input_lower:
            return "Hello! I'm TerminalX AI assistant. How can I help you today?"
        elif 'help' in input_lower:
            return "I can help you with various tasks including system analysis, command suggestions, and general assistance. What would you like to know?"
        elif 'status' in input_lower:
            return "I'm currently active and ready to assist you. All AI systems are operational."
        elif 'thank' in input_lower:
            return "You're welcome! Is there anything else I can help you with?"
        else:
            return f"I understand you said: '{input_text}'. This is a placeholder response - in a full implementation, this would connect to an actual AI model like GPT, Claude, or a local LLM."
        
    async def create_conversation(self, conversation_id: str, system_prompt: str = None) -> bool:
        """Create a new conversation"""
        if conversation_id in self.conversation_history:
            return False
            
        self.conversation_history[conversation_id] = []
        
        if system_prompt:
            self.conversation_history[conversation_id].append({
                'role': MessageRole.SYSTEM.value,
                'content': system_prompt,
                'timestamp': datetime.now().isoformat(),
            })
            
        return True
        
    async def switch_conversation(self, conversation_id: str) -> bool:
        """Switch to a different conversation"""
        if conversation_id not in self.conversation_history:
            return False
            
        self.active_conversation = conversation_id
        return True
        
    async def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation"""
        if conversation_id not in self.conversation_history:
            return False
            
        del self.conversation_history[conversation_id]
        
        if self.active_conversation == conversation_id:
            self.active_conversation = list(self.conversation_history.keys())[0] if self.conversation_history else None
            
        return True
        
    async def list_conversations(self) -> List[str]:
        """List all conversations"""
        return list(self.conversation_history.keys())
        
    async def get_conversation(self, conversation_id: str = None) -> Optional[List[Dict]]:
        """Get conversation history"""
        conv_id = conversation_id or self.active_conversation
        return self.conversation_history.get(conv_id, []).copy()
        
    async def clear_context(self, conversation_id: str = None):
        """Clear conversation context"""
        conv_id = conversation_id or self.active_conversation
        if conv_id in self.conversation_history:
            self.conversation_history[conv_id].clear()
            
    async def get_context(self) -> List[Dict]:
        """Get current context (deprecated, use get_conversation)"""
        if self.active_conversation:
            return self.conversation_history.get(self.active_conversation, []).copy()
        return []
        
    async def set_model(self, model_name: str, model_config: Dict[str, Any]):
        """Set AI model"""
        self.models[model_name] = model_config
        
    async def get_model(self, model_name: str) -> Optional[Dict]:
        """Get AI model configuration"""
        return self.models.get(model_name)
        
    async def list_models(self) -> List[str]:
        """List available models"""
        return list(self.models.keys())
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get AI statistics"""
        return {
            'enabled': self.enabled,
            'active_conversation': self.active_conversation,
            'total_conversations': len(self.conversation_history),
            'max_context': self.max_context,
            'stats': self.stats.copy(),
        }
        
    async def enable(self):
        """Enable AI core"""
        self.enabled = True
        
    async def disable(self):
        """Disable AI core"""
        self.enabled = False
        
    async def export_conversation(self, conversation_id: str, filepath: str):
        """Export conversation to JSON file"""
        if conversation_id not in self.conversation_history:
            return False
            
        with open(filepath, 'w') as f:
            json.dump(self.conversation_history[conversation_id], f, indent=2)
        return True
        
    async def import_conversation(self, conversation_id: str, filepath: str):
        """Import conversation from JSON file"""
        with open(filepath, 'r') as f:
            self.conversation_history[conversation_id] = json.load(f)
        return True
