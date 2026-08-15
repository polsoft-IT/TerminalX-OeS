import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from commands.terminal import TerminalCommands
from core import CoreEngine

async def test_help_system():
    print("=== HELP SYSTEM TEST ===\n")
    
    # Initialize TerminalCommands
    tc = TerminalCommands(CoreEngine())
    
    # Test advanced_shield help
    print("1. Testing advanced_shield help...")
    result = await tc.cmd_help('advanced_shield')
    if result['success']:
        print("   ✓ advanced_shield help works")
        print(f"   Output preview: {result['output'][:100]}...")
    else:
        print(f"   ✗ advanced_shield help failed: {result.get('error')}")
    
    # Test report help
    print("\n2. Testing report help...")
    result = await tc.cmd_help('report')
    if result['success']:
        print("   ✓ report help works")
        print(f"   Output preview: {result['output'][:100]}...")
    else:
        print(f"   ✗ report help failed: {result.get('error')}")
    
    # Test general help
    print("\n3. Testing general help...")
    result = await tc.cmd_help()
    if result['success']:
        print("   ✓ general help works")
        if 'advanced_shield' in result['output'] and 'report' in result['output']:
            print("   ✓ new commands listed in general help")
        else:
            print("   ✗ new commands not listed in general help")
    else:
        print(f"   ✗ general help failed: {result.get('error')}")
    
    print("\n=== HELP SYSTEM TEST COMPLETE ===")

asyncio.run(test_help_system())
