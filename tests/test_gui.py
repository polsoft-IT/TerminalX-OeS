"""
 ============================================================
  MODULE/PLUGIN NAME: TestGUI
  VERSION: 1.0.0
  MODULE CLASS: TestGUI
  DESCRIPTION:
       Test script for GUI modules - validates GUI functionality

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
from gui import GUIEngine, GUIFrameworks, GUIWidgets, GUIWindows, GUIApps

async def test_gui():
    """Test GUI modules"""
    try:
        print("Testing GUIEngine...")
        gui_engine = GUIEngine()
        print("GUIEngine created successfully")
        
        print("Testing GUIFrameworks...")
        gui_frameworks = GUIFrameworks()
        print("GUIFrameworks created successfully")
        
        print("Testing GUIWidgets...")
        gui_widgets = GUIWidgets()
        print("GUIWidgets created successfully")
        
        print("Testing GUIWindows...")
        gui_windows = GUIWindows()
        print("GUIWindows created successfully")
        
        print("Testing GUIApps...")
        gui_apps = GUIApps()
        print("GUIApps created successfully")
        
        print("All GUI tests passed!")
        return True
        
    except Exception as e:
        print(f"GUI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    asyncio.run(test_gui())
