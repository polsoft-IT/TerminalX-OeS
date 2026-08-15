import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import TerminalX

async def test_alias_system():
    print("=== ALIAS SYSTEM TEST ===\n")
    
    # Initialize TerminalX
    terminal = TerminalX()
    await terminal.initialize()
    
    # Test 1: Scan for commands
    print("1. Testing command scanning...")
    result = await terminal.alias_commands.cmd_cmd()
    if result['success']:
        print(f"   ✓ Command scan works")
        print(f"   Found commands in output")
    else:
        print(f"   ✗ Command scan failed: {result.get('error')}")
    
    # Test 2: Add an alias
    print("\n2. Testing alias addition...")
    result = await terminal.alias_commands.cmd_add("network list", ";", "netlist", ";", "Quick network list", ";", "network")
    if result['success']:
        print(f"   ✓ Alias added successfully")
    else:
        print(f"   ✗ Alias addition failed: {result.get('error')}")
    
    # Test 3: List aliases
    print("\n3. Testing alias listing...")
    result = await terminal.alias_commands.cmd_list()
    if result['success']:
        print(f"   ✓ Alias list works")
        if "netlist" in result['output']:
            print(f"   ✓ New alias visible in list")
    else:
        print(f"   ✗ Alias list failed: {result.get('error')}")
    
    # Test 4: Test the alias
    print("\n4. Testing alias functionality...")
    result = await terminal.alias_commands.cmd_test("netlist")
    if result['success']:
        print(f"   ✓ Alias test works")
        if 'command' in result:
            print(f"   Command: {result['command']}")
    else:
        print(f"   ✗ Alias test failed: {result.get('error')}")
    
    # Test 5: Show statistics
    print("\n5. Testing alias statistics...")
    result = await terminal.alias_commands.cmd_stats()
    if result['success']:
        print(f"   ✓ Statistics work")
        print(f"   Total aliases: {result['output'].split('Total Aliases:')[1].split('\\n')[0].strip()}")
    else:
        print(f"   ✗ Statistics failed: {result.get('error')}")
    
    # Test 6: Delete the test alias
    print("\n6. Testing alias deletion...")
    result = await terminal.alias_commands.cmd_del("netlist")
    if result['success']:
        print(f"   ✓ Alias deleted successfully")
    else:
        print(f"   ✗ Alias deletion failed: {result.get('error')}")
    
    print("\n=== ALIAS SYSTEM TEST COMPLETE ===")
    
    await terminal.stop()

asyncio.run(test_alias_system())
