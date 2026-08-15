"""
 ============================================================
  MODULE/PLUGIN NAME: TestAI
  VERSION: 1.0.0
  MODULE CLASS: TestAI
  DESCRIPTION:
       Test script for AI modules - validates AI functionality

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
from ai import AICore, AIModels, AIAnalyzer, AISentinel, AIPlugins

async def test_ai():
    """Test AI modules"""
    try:
        print("Testing AICore...")
        ai_core = AICore()
        print("AICore created successfully")
        
        print("Testing AIModels...")
        ai_models = AIModels()
        print("AIModels created successfully")
        
        print("Testing AIAnalyzer...")
        ai_analyzer = AIAnalyzer()
        print("AIAnalyzer created successfully")
        
        print("Testing AISentinel...")
        ai_sentinel = AISentinel()
        print("AISentinel created successfully")
        
        print("Testing AIPlugins...")
        ai_plugins = AIPlugins()
        print("AIPlugins created successfully")
        
        print("All AI tests passed!")
        return True
        
    except Exception as e:
        print(f"AI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    asyncio.run(test_ai())
