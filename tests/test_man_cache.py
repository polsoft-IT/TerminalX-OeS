import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from man import ManEngine

async def test():
    me = ManEngine()
    
    # Check man_pages BEFORE initialization
    print('=== BEFORE INITIALIZATION ===')
    print('Man pages dict keys:', sorted(me.man_pages.keys()))
    
    await me.initialize({'pages_directory': 'man/pages'})
    
    # Check man_pages AFTER initialization
    print('\n=== AFTER INITIALIZATION ===')
    print('Man pages dict keys:', sorted(me.man_pages.keys()))
    
    # Clear cache
    print('\n=== CLEARING CACHE ===')
    await me.cache.clear()
    print('Cache cleared')
    
    # Check man_pages after cache clear
    print('Man pages dict keys:', sorted(me.man_pages.keys()))
    
    # Print detailed info for suspicious entries
    print('\n=== SUSPICIOUS ENTRIES ===')
    for key in sorted(me.man_pages.keys()):
        page = me.man_pages[key]
        if 'GOD' in key.upper():
            print(f'\nPhantom entry: {key}')
            print(f'  Title: {page.get("title", "N/A")}')
            print(f'  Name: {page.get("name", "N/A")}')
            print(f'  Source: {page.get("source", "unknown")}')
            print(f'  Custom: {page.get("custom", False)}')
            print(f'  Description: {page.get("description", "N/A")}')
            print(f'  Content preview: {page.get("content", "N/A")[:200]}')
    
    # List pages
    pages = await me.list_pages()
    print('\n=== LIST PAGES ===')
    print('Man pages:', sorted(pages))
    print('Total pages:', len(pages))
    
    # Check for phantom entries
    expected_files = ['ai', 'alert', 'anim', 'ansi', 'archive', 'auth', 'bluetooth', 'build', 'cd', 'cloud', 'dev', 'developer', 'display', 'emoji', 'engine', 'ethernet', 'event', 'figlet', 'fs', 'geo', 'gui', 'help', 'kernel', 'lan', 'man', 'metadata', 'module', 'network', 'plugin', 'proc', 'python', 'report', 'shield', 'sysopt', 'system', 'task', 'test_info', 'unicode', 'version', 'widgets', 'wifi']
    
    phantom_found = False
    for page in pages:
        if page not in expected_files:
            print(f'\nPhantom page found: {page}')
            phantom_found = True
    
    if not phantom_found:
        print('\nNo phantom pages found - cache cleared successfully')

asyncio.run(test())
