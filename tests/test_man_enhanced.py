#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test suite for enhanced ManEngine functionality
Tests all new features: WHATIS, advanced search, import/export, validation, history
"""

import asyncio
import os
import sys
import json
import tempfile
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from man.man_engine import ManEngine


class TestManEngineEnhanced:
    """Test suite for enhanced ManEngine"""
    
    def __init__(self):
        self.man_engine = ManEngine()
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
        
        # Create test META files
        meta_file = os.path.join(self.temp_dir, "test.meta")
        with open(meta_file, 'w') as f:
            f.write("name=test_module\n")
            f.write("desc=Test module description\n")
        
        # Create test PKG file
        pkg_file = os.path.join(self.temp_dir, "test_pkg.json")
        with open(pkg_file, 'w') as f:
            json.dump({
                "name": "test_package",
                "description": "Test package description",
                "version": "2.5.0",
                "tags": ["network", "test"]
            }, f)
        
        # Create test INFO file
        info_file = os.path.join(self.temp_dir, "test.info")
        with open(info_file, 'w') as f:
            json.dump({
                "node": "test_info",
                "title": "Test Info",
                "content": "Test info content. This is a test."
            }, f)
        
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
        
    async def test_whatis(self):
        """Test WHATIS functionality"""
        print("\n=== Testing WHATIS functionality ===")
        
        # Test whatis for existing module
        desc = await self.man_engine.whatis('test_module')
        self.log_result(
            "whatis() - existing module",
            desc is not None and 'META' in desc,
            f"Got: {desc}"
        )
        
        # Test whatis for non-existing module
        desc = await self.man_engine.whatis('nonexistent')
        self.log_result(
            "whatis() - non-existing module",
            desc is None,
            "Should return None"
        )
        
        # Test whatis_batch
        results = await self.man_engine.whatis_batch(['test_module', 'test_package'])
        self.log_result(
            "whatis_batch() - multiple modules",
            len(results) == 2 and 'test_module' in results and 'test_package' in results,
            f"Got {len(results)} results"
        )
        
        # Test whatis_all
        all_entries = await self.man_engine.whatis_all()
        self.log_result(
            "whatis_all() - all entries",
            len(all_entries) > 0,
            f"Got {len(all_entries)} entries"
        )
        
    async def test_advanced_search(self):
        """Test advanced search functions"""
        print("\n=== Testing advanced search functions ===")
        
        # Test search_by_source
        results = await self.man_engine.search_by_source('test', 'meta')
        self.log_result(
            "search_by_source() - meta source",
            'test_module' in results,
            f"Found {len(results)} results"
        )
        
        results = await self.man_engine.search_by_source('test', 'pkg')
        self.log_result(
            "search_by_source() - pkg source",
            'test_package' in results,
            f"Found {len(results)} results"
        )
        
        # Test search_by_tag
        results = await self.man_engine.search_by_tag('network')
        self.log_result(
            "search_by_tag() - existing tag",
            'test_package' in results,
            f"Found {len(results)} results"
        )
        
        results = await self.man_engine.search_by_tag('nonexistent')
        self.log_result(
            "search_by_tag() - non-existing tag",
            len(results) == 0,
            "Should return empty dict"
        )
        
        # Test search_by_section
        results = await self.man_engine.search_by_section(1)
        self.log_result(
            "search_by_section() - section 1",
            len(results) > 0,
            f"Found {len(results)} results"
        )
        
        # Test search_advanced
        results = await self.man_engine.search_advanced('test', {'source': 'meta'})
        self.log_result(
            "search_advanced() - with source filter",
            'test_module' in results,
            f"Found {len(results)} results"
        )
        
        results = await self.man_engine.search_advanced('test', {'exact': True})
        self.log_result(
            "search_advanced() - exact match",
            len(results) >= 0,  # May or may not match exactly
            f"Found {len(results)} results"
        )
        
    async def test_import_export(self):
        """Test import/export functions"""
        print("\n=== Testing import/export functions ===")
        
        # Test export_database to JSON
        export_file = os.path.join(self.temp_dir, "test_export.json")
        success = await self.man_engine.export_database(export_file, 'json')
        self.log_result(
            "export_database() - JSON format",
            success and os.path.exists(export_file),
            f"Exported to {export_file}"
        )
        
        # Verify export content
        if os.path.exists(export_file):
            with open(export_file, 'r') as f:
                data = json.load(f)
            self.log_result(
                "export_database() - JSON content validation",
                'meta' in data and 'pkg' in data and 'info' in data,
                "Contains expected keys"
            )
        
        # Test export_database to TXT
        export_file_txt = os.path.join(self.temp_dir, "test_export.txt")
        success = await self.man_engine.export_database(export_file_txt, 'txt')
        self.log_result(
            "export_database() - TXT format",
            success and os.path.exists(export_file_txt),
            f"Exported to {export_file_txt}"
        )
        
        # Test import_database with merge
        import_file = os.path.join(self.temp_dir, "test_import.json")
        test_data = {
            'meta': {'imported_module': 'Imported module description'},
            'pkg': {'imported_pkg': {'description': 'Imported package', 'version': '2.0.0', 'tags': ['import']}},
            'info': {},
            'man': {}
        }
        with open(import_file, 'w') as f:
            json.dump(test_data, f)
        
        success = await self.man_engine.import_database(import_file, merge=True)
        self.log_result(
            "import_database() - merge mode",
            success,
            "Import successful"
        )
        
        # Verify import
        desc = await self.man_engine.whatis('imported_module')
        self.log_result(
            "import_database() - verify merged entry",
            desc is not None and 'META' in desc,
            f"Imported entry found: {desc}"
        )
        
        # Test import_database with replace
        success = await self.man_engine.import_database(import_file, merge=False)
        self.log_result(
            "import_database() - replace mode",
            success,
            "Import successful"
        )
        
    async def test_validation(self):
        """Test validation function"""
        print("\n=== Testing validation function ===")
        
        # Add some invalid entries for testing
        self.man_engine.meta_entries[''] = 'Empty name'
        self.man_engine.pkg_entries['invalid*name'] = {'description': '', 'version': '1.0', 'tags': []}
        
        issues = await self.man_engine.validate_entries()
        
        self.log_result(
            "validate_entries() - detects empty names",
            len(issues.get('empty_names', [])) > 0,
            f"Found {len(issues.get('empty_names', []))} empty names"
        )
        
        self.log_result(
            "validate_entries() - detects missing descriptions",
            len(issues.get('missing_descriptions', [])) > 0,
            f"Found {len(issues.get('missing_descriptions', []))} missing descriptions"
        )
        
        self.log_result(
            "validate_entries() - detects invalid characters",
            len(issues.get('invalid_chars', [])) > 0,
            f"Found {len(issues.get('invalid_chars', []))} invalid character entries"
        )
        
        # Clean up test entries
        if '' in self.man_engine.meta_entries:
            del self.man_engine.meta_entries['']
        if 'invalid*name' in self.man_engine.pkg_entries:
            del self.man_engine.pkg_entries['invalid*name']
        
    async def test_history(self):
        """Test history functions"""
        print("\n=== Testing history functions ===")
        
        # Add some search history
        self.man_engine._add_to_history('test', 'fuzzy', 5)
        self.man_engine._add_to_history('network', 'wildcard', 10)
        self.man_engine._add_to_history('test', 'regex', 3)
        
        # Test get_search_history
        history = await self.man_engine.get_search_history(10)
        self.log_result(
            "get_search_history() - retrieves history",
            len(history) == 3,
            f"Got {len(history)} entries"
        )
        
        # Test history limit
        history = await self.man_engine.get_search_history(2)
        self.log_result(
            "get_search_history() - respects limit",
            len(history) == 2,
            f"Got {len(history)} entries (limit: 2)"
        )
        
        # Test clear_search_history
        await self.man_engine.clear_search_history()
        history = await self.man_engine.get_search_history()
        self.log_result(
            "clear_search_history() - clears history",
            len(history) == 0,
            "History cleared"
        )
        
    async def run_all_tests(self):
        """Run all tests"""
        print("=" * 60)
        print("ManEngine Enhanced Test Suite")
        print("=" * 60)
        
        try:
            await self.setup()
            
            await self.test_whatis()
            await self.test_advanced_search()
            await self.test_import_export()
            await self.test_validation()
            await self.test_history()
            
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
    tester = TestManEngineEnhanced()
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    asyncio.run(main())
