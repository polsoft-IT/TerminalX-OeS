"""
 ============================================================
  MODULE/PLUGIN NAME: TestRunner
  VERSION: 1.0.1
  MODULE CLASS: TestRunner
  DESCRIPTION:
       Test runner for TerminalX - runs all tests from the tests directory (updated with man pages test)

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
import asyncio

# Add parent directory to path
sys.path.insert(0, '..')

async def run_all_tests():
    """Run all test files"""
    test_files = [
        'test_import.py',
        'test_ai.py',
        'test_core.py',
        'test_network.py',
        'test_gui.py',
        'test_kernel.py',
        'test_shield.py',
        'test_modules.py',
        'test_plugins.py',
        'test_process.py',
        'test_cache.py',
        'test_commands_main.py',
        'test_man.py'
    ]
    
    results = {}
    
    for test_file in test_files:
        test_path = os.path.join(os.path.dirname(__file__), test_file)
        if os.path.exists(test_path):
            print(f"\n{'='*60}")
            print(f"Running {test_file}")
            print('='*60)
            
            try:
                # Import and run test
                spec = __import__('importlib.util').util.spec_from_file_location(test_file[:-3], test_path)
                module = __import__('importlib.util').util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'test'):
                    result = await module.test()
                    results[test_file] = result
                elif hasattr(module, 'test_ai'):
                    result = await module.test_ai()
                    results[test_file] = result
                elif hasattr(module, 'test_core'):
                    result = await module.test_core()
                    results[test_file] = result
                elif hasattr(module, 'test_network'):
                    result = await module.test_network()
                    results[test_file] = result
                elif hasattr(module, 'test_gui'):
                    result = await module.test_gui()
                    results[test_file] = result
                elif hasattr(module, 'test_kernel'):
                    result = await module.test_kernel()
                    results[test_file] = result
                elif hasattr(module, 'test_shield'):
                    result = await module.test_shield()
                    results[test_file] = result
                elif hasattr(module, 'test_modules'):
                    result = await module.test_modules()
                    results[test_file] = result
                elif hasattr(module, 'test_plugins'):
                    result = await module.test_plugins()
                    results[test_file] = result
                elif hasattr(module, 'test_process'):
                    result = await module.test_process()
                    results[test_file] = result
                elif hasattr(module, 'test_cache'):
                    result = await module.test_cache()
                    results[test_file] = result
                elif hasattr(module, 'test_man'):
                    result = await module.test_man()
                    results[test_file] = result
                else:
                    results[test_file] = None
                    
            except Exception as e:
                print(f"Error running {test_file}: {e}")
                results[test_file] = False
    
    # Print summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Total: {len(results)}")
    
    return results

if __name__ == '__main__':
    asyncio.run(run_all_tests())
