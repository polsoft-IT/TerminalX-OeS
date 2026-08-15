import asyncio
from main import TerminalX

async def test_commands():
    t = TerminalX()
    await t.initialize()
    
    # Test Standard Systems commands
    commands = [
        'ai chat test',
        'gui list',
        'net ping 8.8.8.8',
        'cloud status',
        'modules list',
        'plugins list',
    ]
    
    for cmd in commands:
        print(f"\n=== Testing: {cmd} ===")
        result = await t.execute_command(cmd)
        print(f"Success: {result.get('success')}")
        print(f"Output: {result.get('output')}")
        if result.get('error'):
            print(f"Error: {result.get('error')}")
    
    await t.stop()

if __name__ == '__main__':
    asyncio.run(test_commands())
