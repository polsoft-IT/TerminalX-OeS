"""
 ============================================================
  MODULE/PLUGIN NAME: TestModules
  VERSION: 1.0.0
  MODULE CLASS: TestModules
  DESCRIPTION:
       Test script for Module management - validates module functionality

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

import sys
sys.path.insert(0, '..')

import asyncio
from libs.module_manager import ModuleManager
from libs.module_loader import ModuleLoader
from libs.module_registry import ModuleRegistry

async def test_modules():
    """Test Module management"""
    try:
        print("Testing ModuleManager...")
        module_manager = ModuleManager()
        print("ModuleManager created successfully")
        
        print("Testing ModuleLoader...")
        module_loader = ModuleLoader()
        print("ModuleLoader created successfully")
        
        print("Testing ModuleRegistry...")
        module_registry = ModuleRegistry()
        print("ModuleRegistry created successfully")
        
        print("All Module tests passed!")
        return True
        
    except Exception as e:
        print(f"Module test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    asyncio.run(test_modules())
