"""
 ============================================================
  MODULE/PLUGIN NAME: TestNetwork
  VERSION: 1.0.0
  MODULE CLASS: TestNetwork
  DESCRIPTION:
       Test script for Network modules - validates network functionality

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
from network import NetworkCore, NetworkManager, NetworkMonitor, NetworkEvents, NetworkHooks, NetworkSandbox

async def test_network():
    """Test Network modules"""
    try:
        print("Testing NetworkCore...")
        network_core = NetworkCore()
        print("NetworkCore created successfully")
        
        print("Testing NetworkManager...")
        network_manager = NetworkManager()
        print("NetworkManager created successfully")
        
        print("Testing NetworkMonitor...")
        network_monitor = NetworkMonitor()
        print("NetworkMonitor created successfully")
        
        print("Testing NetworkEvents...")
        network_events = NetworkEvents()
        print("NetworkEvents created successfully")
        
        print("Testing NetworkHooks...")
        network_hooks = NetworkHooks()
        print("NetworkHooks created successfully")
        
        print("Testing NetworkSandbox...")
        network_sandbox = NetworkSandbox()
        print("NetworkSandbox created successfully")
        
        print("All Network tests passed!")
        return True
        
    except Exception as e:
        print(f"Network test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    asyncio.run(test_network())
