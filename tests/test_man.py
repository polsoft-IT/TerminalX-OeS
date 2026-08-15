"""
 ============================================================
  MODULE/PLUGIN NAME: TestMan
  VERSION: 1.0.0
  MODULE CLASS: TestMan
  DESCRIPTION:
       Test script for Man pages module - validates man functionality

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
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from man import ManEngine, ManParser, ManViewer, ManCache

async def test_man():
    """Test Man pages module"""
    try:
        print("Testing ManEngine...")
        man_engine = ManEngine()
        print("ManEngine created successfully")
        
        print("Testing ManParser...")
        man_parser = ManParser()
        print("ManParser created successfully")
        
        print("Testing ManViewer...")
        man_viewer = ManViewer()
        print("ManViewer created successfully")
        
        print("Testing ManCache...")
        man_cache = ManCache()
        print("ManCache created successfully")
        
        # Test initialization
        print("Testing initialization...")
        await man_engine.initialize()
        print("ManEngine initialized successfully")
        
        # Test list pages
        print("Testing list pages...")
        pages = await man_engine.list_pages()
        print(f"Found {len(pages)} man pages")
        
        # Test search
        print("Testing search...")
        results = await man_engine.search("man")
        print(f"Search results: {results}")
        
        # Test display page
        if results:
            print("Testing display page...")
            content = await man_engine.display_page(results[0])
            print(f"Page content length: {len(content)}")
        
        # Test stats
        print("Testing stats...")
        stats = await man_engine.get_stats()
        print(f"Man engine stats: {stats}")
        
        print("All Man tests passed!")
        return True
        
    except Exception as e:
        print(f"Man test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    asyncio.run(test_man())
