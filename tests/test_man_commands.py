#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test suite for enhanced ManCommands
Tests all new command handlers
"""

import asyncio
import os
import sys
import tempfile
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from man.man_engine import ManEngine
from commands.man import ManCommands


class TestManCommandsEnhanced:
    """Test suite for enhanced ManCommands"""
    
    def __init__(self):
        self.man_engine = ManEngine()
        self.man_commands = ManCommands(self.man_engine)
        self.test_results = []
        self.temp_dir = None
        
    def log_result(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✓ PASS" if passed else "✗ FAIL"
        result = f"{status}: {test_name}"
        if message:
            result += f" - {message}"
        print(result)
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'message': message
        })
        
    async def setup(self):
        """Setup test environment"""
        print("\n=== Setting up test environment ===")
        self.temp_dir = tempfile.mkdtemp()
        
        # Initialize man engine with test config
        config = {
            'enabled': True,
            'cache': {'enabled': True},
            'parser': {},
            'viewer': {},
            'load_external': False
        }
        
        await self.man_engine.initialize(config)
        
        # Manually add test entries
        self.man_engine.meta_entries['test_module'] = 'Test module description'
        self.man_engine.pkg_entries['test_package'] = {
            'description': 'Test package description',
            'version': '2.5.0',
            'tags': ['network', 'test']
        }
        self.man_engine.info_entries['test_info'] = 'Test Info — Test info content'
        
        # Add to man_pages
        self.man_engine.man_pages['test_module'] = {
            'name': 'test_module',
            'description': 'Test module description',
            'section': 1,
            'custom': True,
            'source': 'meta',
            'created': datetime.now().isoformat()
        }
        
        self.man_engine.man_pages['test_package'] = {
            'name': 'test_package',
            'description': 'Test package description',
            'section': 1,
            'custom': True,
            'source': 'pkg',
            'version': '2.5.0',
            'tags': ['network', 'test'],
            'created': datetime.now().isoformat()
        }
        
        self.man_engine._build_index()
        print("Setup complete")
        
    async def teardown(self):
        """Cleanup test environment"""
        print("\n=== Cleaning up test environment ===")
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
        print("Teardown complete")
        
    async def test_whatis_commands(self):
        """Test WHATIS commands"""
        print("\n=== Testing WHATIS commands ===")
        
        # Test cmd_whatis
        result = await self.man_commands.cmd_whatis('test_module')
        self.log_result(
            "cmd_whatis() - existing module",
            result['success'] and 'test_module' in result['output'],
            f"Output: {result.get('output', '')[:50]}"
        )
        
        result = await self.man_commands.cmd_whatis('nonexistent')
        self.log_result(
            "cmd_whatis() - non-existing module",
            not result['success'],
            f"Error: {result.get('error', '')}"
        )
        
        # Test cmd_whatis_all
        result = await self.man_commands.cmd_whatis_all()
        self.log_result(
            "cmd_whatis_all() - all entries",
            result['success'] and result['count'] > 0,
            f"Got {result.get('count', 0)} entries"
        )
        
    async def test_search_source_commands(self):
        """Test search source commands"""
        print("\n=== Testing search source commands ===")
        
        # Test cmd_search_source
        result = await self.man_commands.cmd_search_source('test', 'meta')
        self.log_result(
            "cmd_search_source() - meta source",
            result['success'] and result['count'] > 0,
            f"Found {result.get('count', 0)} results"
        )
        
        result = await self.man_commands.cmd_search_source('test', 'pkg')
        self.log_result(
            "cmd_search_source() - pkg source",
            result['success'] and result['count'] > 0,
            f"Found {result.get('count', 0)} results"
        )
        
        result = await self.man_commands.cmd_search_source('test', 'invalid')
        self.log_result(
            "cmd_search_source() - invalid source",
            result['success'] and result['count'] == 0,
            "Should return 0 results"
        )
        
    async def test_search_tag_commands(self):
        """Test search tag commands"""
        print("\n=== Testing search tag commands ===")
        
        # Test cmd_search_tag
        result = await self.man_commands.cmd_search_tag('network')
        self.log_result(
            "cmd_search_tag() - existing tag",
            result['success'] and result['count'] > 0,
            f"Found {result.get('count', 0)} results"
        )
        
        result = await self.man_commands.cmd_search_tag('nonexistent')
        self.log_result(
            "cmd_search_tag() - non-existing tag",
            result['success'] and result['count'] == 0,
            "Should return 0 results"
        )
        
    async def test_search_section_commands(self):
        """Test search section commands"""
        print("\n=== Testing search section commands ===")
        
        # Test cmd_search_section
        result = await self.man_commands.cmd_search_section('1')
        self.log_result(
            "cmd_search_section() - section 1",
            result['success'] and result['count'] > 0,
            f"Found {result.get('count', 0)} results"
        )
        
        result = await self.man_commands.cmd_search_section('invalid')
        self.log_result(
            "cmd_search_section() - invalid section",
            not result['success'],
            f"Error: {result.get('error', '')}"
        )
        
    async def test_search_advanced_commands(self):
        """Test advanced search commands"""
        print("\n=== Testing advanced search commands ===")
        
        # Test cmd_search_advanced with source filter
        result = await self.man_commands.cmd_search_advanced('test', '--source', 'meta')
        self.log_result(
            "cmd_search_advanced() - with source filter",
            result['success'],
            f"Found {result.get('count', 0)} results"
        )
        
        # Test cmd_search_advanced with exact match
        result = await self.man_commands.cmd_search_advanced('test', '--exact')
        self.log_result(
            "cmd_search_advanced() - exact match",
            result['success'],
            f"Found {result.get('count', 0)} results"
        )
        
        # Test cmd_search_advanced with multiple options
        result = await self.man_commands.cmd_search_advanced('test', '--source', 'pkg', '--exact')
        self.log_result(
            "cmd_search_advanced() - multiple options",
            result['success'],
            f"Found {result.get('count', 0)} results"
        )
        
    async def test_import_export_commands(self):
        """Test import/export commands"""
        print("\n=== Testing import/export commands ===")
        
        # Test cmd_export_db
        export_file = os.path.join(self.temp_dir, "test_export.json")
        result = await self.man_commands.cmd_export_db(export_file, 'json')
        self.log_result(
            "cmd_export_db() - JSON format",
            result['success'] and os.path.exists(export_file),
            f"Exported to {export_file}"
        )
        
        # Test cmd_export_db with TXT
        export_file_txt = os.path.join(self.temp_dir, "test_export.txt")
        result = await self.man_commands.cmd_export_db(export_file_txt, 'txt')
        self.log_result(
            "cmd_export_db() - TXT format",
            result['success'] and os.path.exists(export_file_txt),
            f"Exported to {export_file_txt}"
        )
        
        # Test cmd_import_db with merge
        import_file = os.path.join(self.temp_dir, "test_import.json")
        import json
        test_data = {
            'meta': {'imported_module': 'Imported module description'},
            'pkg': {'imported_pkg': {'description': 'Imported package', 'version': '2.0.0', 'tags': ['import']}},
            'info': {},
            'man': {}
        }
        with open(import_file, 'w') as f:
            json.dump(test_data, f)
        
        result = await self.man_commands.cmd_import_db(import_file)
        self.log_result(
            "cmd_import_db() - merge mode",
            result['success'],
            f"Mode: {result.get('mode', '')}"
        )
        
        # Test cmd_import_db with replace
        result = await self.man_commands.cmd_import_db(import_file, '--replace')
        self.log_result(
            "cmd_import_db() - replace mode",
            result['success'],
            f"Mode: {result.get('mode', '')}"
        )
        
    async def test_validate_commands(self):
        """Test validation commands"""
        print("\n=== Testing validation commands ===")
        
        # Add some invalid entries for testing
        self.man_engine.meta_entries[''] = 'Empty name'
        self.man_engine.pkg_entries['invalid*name'] = {'description': '', 'version': '1.0', 'tags': []}
        
        # Test cmd_validate
        result = await self.man_commands.cmd_validate()
        self.log_result(
            "cmd_validate() - validation",
            result['success'],
            f"Total issues: {result.get('total_issues', 0)}"
        )
        
        # Clean up test entries
        if '' in self.man_engine.meta_entries:
            del self.man_engine.meta_entries['']
        if 'invalid*name' in self.man_engine.pkg_entries:
            del self.man_engine.pkg_entries['invalid*name']
        
    async def test_history_commands(self):
        """Test history commands"""
        print("\n=== Testing history commands ===")
        
        # Add some search history
        self.man_engine._add_to_history('test', 'fuzzy', 5)
        self.man_engine._add_to_history('network', 'wildcard', 10)
        
        # Test cmd_history
        result = await self.man_commands.cmd_history()
        self.log_result(
            "cmd_history() - retrieves history",
            result['success'] and result['count'] > 0,
            f"Got {result.get('count', 0)} entries"
        )
        
        # Test cmd_history with limit
        result = await self.man_commands.cmd_history('1')
        self.log_result(
            "cmd_history() - with limit",
            result['success'] and result['count'] == 1,
            f"Got {result.get('count', 0)} entries (limit: 1)"
        )
        
        # Test cmd_clear_history
        result = await self.man_commands.cmd_clear_history()
        self.log_result(
            "cmd_clear_history() - clears history",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        # Verify history is cleared
        result = await self.man_commands.cmd_history()
        self.log_result(
            "cmd_clear_history() - verification",
            result['success'] and result['count'] == 0,
            "History should be empty"
        )
        
    async def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("ManCommands Enhanced Test Suite")
        print("=" * 60)
        
        try:
            await self.setup()
            
            await self.test_whatis_commands()
            await self.test_search_source_commands()
            await self.test_search_tag_commands()
            await self.test_search_section_commands()
            await self.test_search_advanced_commands()
            await self.test_import_export_commands()
            await self.test_validate_commands()
            await self.test_history_commands()
            
            await self.teardown()
            
            # Print summary
            print("\n" + "=" * 60)
            print("Test Summary")
            print("=" * 60)
            
            passed = sum(1 for r in self.test_results if r['passed'])
            total = len(self.test_results)
            
            print(f"Total tests: {total}")
            print(f"Passed: {passed}")
            print(f"Failed: {total - passed}")
            print(f"Success rate: {(passed/total)*100:.1f}%")
            
            if passed == total:
                print("\n✓ All tests passed!")
                return True
            else:
                print("\n✗ Some tests failed:")
                for result in self.test_results:
                    if not result['passed']:
                        print(f"  - {result['test']}: {result['message']}")
                return False
                
        except Exception as e:
            print(f"\n✗ Test suite failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """Main test runner"""
    tester = TestManCommandsEnhanced()
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    asyncio.run(main())
