"""
 ============================================================
  MODULE/PLUGIN NAME: TestCommandsMain
  VERSION: 1.0.0
  MODULE CLASS: TestCommandsMain
  DESCRIPTION:
       Test script for TerminalX main command execution

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
from main import TerminalX

async def test():
    t = TerminalX()
    
    # Test display commands
    result = await t.execute_command('display color test')
    print('display color test:', result)
    
    # Test dev commands
    result = await t.execute_command('dev calc 2+2')
    print('dev calc 2+2:', result)
    
    # Test fs commands
    result = await t.execute_command('fs ls')
    print('fs ls:', result)
    
    # Test emoji commands
    result = await t.execute_command('emoji all')
    print('emoji all:', result.get('success', False))
    
    # Test unicode commands
    result = await t.execute_command('unicode page 1')
    print('unicode page 1:', result.get('success', False))
    
    # Test figlet commands
    result = await t.execute_command('figlet render test')
    print('figlet render test:', result.get('success', False))
    
    # Test ansi commands
    result = await t.execute_command('ansi rgb 255 0 0')
    print('ansi rgb:', result.get('success', False))
    
    # Test anim commands
    result = await t.execute_command('anim list')
    print('anim list:', result.get('success', False))
    
    # Test widgets commands
    result = await t.execute_command('widgets list')
    print('widgets list:', result.get('success', False))
    
    # Test metadata commands
    result = await t.execute_command('metadata scan test.txt')
    print('metadata scan:', result.get('success', False))
    
    # Test build commands
    result = await t.execute_command('build status')
    print('build status:', result.get('success', False))
    
    # Test task commands
    result = await t.execute_command('task list')
    print('task list:', result.get('success', False))

if __name__ == '__main__':
    asyncio.run(test())
