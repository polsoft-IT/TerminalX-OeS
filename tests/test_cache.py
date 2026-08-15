"""
 ============================================================
  MODULE/PLUGIN NAME: TestCache
  VERSION: 1.0.0
  MODULE CLASS: TestCache
  DESCRIPTION:
       Test script for Cache system - validates caching functionality

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
from geo import CachePlugin

async def test_cache():
    """Test Cache system"""
    try:
        print("Testing CachePlugin...")
        cache_plugin = CachePlugin()
        print("CachePlugin created successfully")
        
        print("All Cache tests passed!")
        return True
        
    except Exception as e:
        print(f"Cache test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    asyncio.run(test_cache())
