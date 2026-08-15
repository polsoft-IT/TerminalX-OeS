"""
 ============================================================
  MODULE/PLUGIN NAME: TestCore
  VERSION: 1.0.0
  MODULE CLASS: TestCore
  DESCRIPTION:
       Test script for Core modules - validates core functionality

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
from core import CoreEngine, Logger, MultiTaskEngine

async def test_core():
    """Test Core modules"""
    try:
        print("Testing CoreEngine...")
        core_engine = CoreEngine()
        print("CoreEngine created successfully")
        
        print("Testing Logger...")
        logger = Logger()
        print("Logger created successfully")
        
        print("Testing MultiTaskEngine...")
        task_engine = MultiTaskEngine()
        print("MultiTaskEngine created successfully")
        
        print("All Core tests passed!")
        return True
        
    except Exception as e:
        print(f"Core test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    asyncio.run(test_core())
