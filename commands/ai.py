"""
 ============================================================
  MODULE/PLUGIN NAME: AICommands
  VERSION: 1.0.0
  MODULE CLASS: AICommands
  DESCRIPTION:
       AI command handlers for AI operations

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
from typing import Dict, Any


class AICommands:
    """AI command handlers"""
    
    def __init__(self, ai_core):
        self.ai = ai_core
        
    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute an AI command"""
        handler = getattr(self, f'cmd_{command}', None)
        
        if handler:
            return await handler(*args)
        else:
            return {
                'success': False,
                'error': f'Unknown AI command: {command}',
            }
            
    async def cmd_process(self, *args) -> Dict[str, Any]:
        """Process text with AI"""
        if not args:
            return {'success': False, 'error': 'No text provided'}
            
        text = ' '.join(args)
        response = await self.ai.process(text)
        
        return {
            'success': True,
            'output': response
        }
        
    async def cmd_analyze(self, *args) -> Dict[str, Any]:
        """Analyze text with AI"""
        if not args:
            return {'success': False, 'error': 'No text provided'}
            
        from ai.ai_analyzer import AIAnalyzer
        analyzer = AIAnalyzer()
        await analyzer.initialize()
        
        text = ' '.join(args)
        result = await analyzer.analyze_text(text)
        
        return {
            'success': True,
            'output': result
        }
        
    async def cmd_clear(self, *args) -> Dict[str, Any]:
        """Clear AI context"""
        await self.ai.clear_context()
        
        return {
            'success': True,
            'output': 'Context cleared'
        }
        
    async def cmd_context(self, *args) -> Dict[str, Any]:
        """Show AI context"""
        context = await self.ai.get_context()
        
        return {
            'success': True,
            'output': context
        }
        
    async def cmd_status(self, *args) -> Dict[str, Any]:
        """Show AI status"""
        return {
            'success': True,
            'output': {
                'enabled': self.ai.enabled,
                'context_size': len(self.ai.context),
                'max_context': self.ai.max_context,
            }
        }
