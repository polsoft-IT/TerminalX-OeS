"""
 ============================================================
  MODULE/PLUGIN NAME: TestPlugins
  VERSION: 1.0.0
  MODULE CLASS: TestPlugins
  DESCRIPTION:
       Test script for Plugin system - validates plugin functionality

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
from plugin.core.plugin_manager import PluginManager
from plugin.core.loader import PluginLoader
from plugin.core.registry import PluginRegistry

async def test_plugins():
    """Test Plugin system"""
    try:
        print("Testing PluginManager...")
        plugin_manager = PluginManager()
        print("PluginManager created successfully")
        
        print("Testing PluginLoader...")
        plugin_loader = PluginLoader()
        print("PluginLoader created successfully")
        
        print("Testing PluginRegistry...")
        plugin_registry = PluginRegistry()
        print("PluginRegistry created successfully")
        
        print("All Plugin tests passed!")
        return True
        
    except Exception as e:
        print(f"Plugin test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    asyncio.run(test_plugins())
