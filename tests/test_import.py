"""
 ============================================================
  MODULE/PLUGIN NAME: TestImport
  VERSION: 1.0.0
  MODULE CLASS: TestImport
  DESCRIPTION:
       Test script for TerminalX main import and initialization

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

import asyncio
import sys
sys.path.insert(0, '..')

from main import TerminalX

async def test():
    try:
        t = TerminalX()
        print('TerminalX created OK')
        await t.initialize()
        print('Initialize OK')
        await t.start()
        print('Start OK')
        await t.stop()
        print('Stop OK')
        print('All tests passed!')
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(test())
