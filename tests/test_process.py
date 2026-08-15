"""
 ============================================================
  MODULE/PLUGIN NAME: TestProcess
  VERSION: 1.0.0
  MODULE CLASS: TestProcess
  DESCRIPTION:
       Test script for Process monitoring - validates process functionality

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
from libs.process_monitor import ProcessMonitor
from process_monitor import ProcessAnalyzer, ProcessHooks

async def test_process():
    """Test Process monitoring"""
    try:
        print("Testing ProcessMonitor...")
        process_monitor = ProcessMonitor()
        print("ProcessMonitor created successfully")
        
        print("Testing ProcessAnalyzer...")
        process_analyzer = ProcessAnalyzer()
        print("ProcessAnalyzer created successfully")
        
        print("Testing ProcessHooks...")
        process_hooks = ProcessHooks()
        print("ProcessHooks created successfully")
        
        print("All Process tests passed!")
        return True
        
    except Exception as e:
        print(f"Process test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    asyncio.run(test_process())
