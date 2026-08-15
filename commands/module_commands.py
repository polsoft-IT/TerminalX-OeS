"""
 ============================================================
  MODULE/PLUGIN NAME: ModuleCommands
  VERSION: 1.0.0
  MODULE CLASS: ModuleCommands
  DESCRIPTION:
       Enhanced module command handlers using Module Engine

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
from typing import Dict, Any, List
from commands.module_engine import ModuleCommandDispatcher, ModuleManager


class ModuleCommands:
    """Enhanced module command handlers using Module Engine"""

    def __init__(self, core_engine=None):
        self.dispatcher = ModuleCommandDispatcher(core_engine=core_engine)
        self.manager = self.dispatcher.manager
        
    async def execute(self, command: str, args: List[str]) -> Dict[str, Any]:
        """Execute a module command"""
        # The command parameter is the subcommand (e.g., "list"), args are the arguments
        # Build the full command for the dispatcher
        parts = ["module", command] + args
        full_command = " ".join(parts)
        
        # Debug: print what we're sending to dispatcher
        # print(f"DEBUG: Sending to dispatcher: {full_command}")
            
        result = self.dispatcher.dispatch(full_command)
        
        # Convert status to success/error format
        if result.get("status") == "ok":
            return {
                'success': True,
                'output': result
            }
        else:
            # Include the full result in details for debugging
            error_msg = result.get("message", "Unknown error")
            if not error_msg and "status" in result:
                error_msg = f"Command failed with status: {result.get('status')}"
            return {
                'success': False,
                'error': error_msg,
                'details': result
            }
