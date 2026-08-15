"""
 ============================================================
  MODULE/PLUGIN NAME: TestKernel
  VERSION: 1.0.0
  MODULE CLASS: TestKernel
  DESCRIPTION:
       Test script for Kernel modules - validates kernel functionality

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
from kernel import KernelEvents, KernelHooks, KernelMonitor, Traps

async def test_kernel():
    """Test Kernel modules"""
    try:
        print("Testing KernelEvents...")
        kernel_events = KernelEvents()
        print("KernelEvents created successfully")
        
        print("Testing KernelHooks...")
        kernel_hooks = KernelHooks()
        print("KernelHooks created successfully")
        
        print("Testing KernelMonitor...")
        kernel_monitor = KernelMonitor()
        print("KernelMonitor created successfully")
        
        print("Testing Traps...")
        traps = Traps()
        print("Traps created successfully")
        
        print("All Kernel tests passed!")
        return True
        
    except Exception as e:
        print(f"Kernel test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    asyncio.run(test_kernel())
