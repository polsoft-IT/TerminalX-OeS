#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test suite for VersionModule and VersionCommands
Tests all version functionality and integration with TerminalX
"""

import asyncio
import os
import sys
import json
from datetime import datetime
import importlib.util

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Direct imports to avoid __init__.py issues
spec = importlib.util.spec_from_file_location("version", os.path.join(os.path.dirname(__file__), "..", "modules", "version.py"))
version_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(version_module)
VersionModule = version_module.VersionModule
VersionInfo = version_module.VersionInfo

spec = importlib.util.spec_from_file_location("version_commands", os.path.join(os.path.dirname(__file__), "..", "commands", "version.py"))
commands_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(commands_module)
VersionCommands = commands_module.VersionCommands

from core import Logger


class TestVersionModule:
    """Test suite for VersionModule"""
    
    def __init__(self):
        self.version_module = VersionModule()
        self.test_results = []
        self.logger = Logger()
        
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
        self.version_module.set_logger(self.logger)
        await self.version_module.initialize()
        print("Setup complete")
        
    async def teardown(self):
        """Cleanup test environment"""
        print("\n=== Cleaning up test environment ===")
        print("Teardown complete")
        
    async def test_version_info(self):
        """Test VersionInfo dataclass"""
        print("\n=== Testing VersionInfo ===")
        
        info = VersionInfo()
        
        # Test semver
        semver = info.semver()
        self.log_result(
            "VersionInfo.semver()",
            semver == "1.0.9",
            f"Got: {semver}"
        )
        
        # Test full version
        full = info.full_version()
        self.log_result(
            "VersionInfo.full_version()",
            "1.0.9" in full and "build" in full,
            f"Got: {full}"
        )
        
        # Test short
        short = info.short()
        self.log_result(
            "VersionInfo.short()",
            "TerminalX" in short and "1.0.9" in short,
            f"Got: {short}"
        )
        
        # Test to_dict
        data = info.to_dict()
        self.log_result(
            "VersionInfo.to_dict()",
            isinstance(data, dict) and 'name' in data and 'major' in data,
            f"Keys: {list(data.keys())}"
        )
        
    async def test_version_module_api(self):
        """Test VersionModule API"""
        print("\n=== Testing VersionModule API ===")
        
        # Test get_semver
        semver = self.version_module.get_semver()
        self.log_result(
            "VersionModule.get_semver()",
            semver == "1.0.9",
            f"Got: {semver}"
        )
        
        # Test get_full_version
        full = self.version_module.get_full_version()
        self.log_result(
            "VersionModule.get_full_version()",
            "1.0.9" in full and "build" in full,
            f"Got: {full}"
        )
        
        # Test get_info_dict
        info_dict = self.version_module.get_info_dict()
        self.log_result(
            "VersionModule.get_info_dict()",
            isinstance(info_dict, dict) and 'name' in info_dict,
            f"Keys: {list(info_dict.keys())}"
        )
        
        # Test set_build
        self.version_module.set_build(999)
        new_build = self.version_module.info.build
        self.log_result(
            "VersionModule.set_build()",
            new_build == 999,
            f"Build set to: {new_build}"
        )
        
        # Test set_tag
        self.version_module.set_tag("beta")
        new_tag = self.version_module.info.tag
        self.log_result(
            "VersionModule.set_tag()",
            new_tag == "beta",
            f"Tag set to: {new_tag}"
        )
        
    async def test_formatting(self):
        """Test output formatting"""
        print("\n=== Testing output formatting ===")
        
        # Test format_human
        human = self.version_module.format_human()
        self.log_result(
            "VersionModule.format_human()",
            "TerminalX" in human and "Version:" in human,
            f"Contains expected fields"
        )
        
        # Test format_short
        short = self.version_module.format_short()
        self.log_result(
            "VersionModule.format_short()",
            "TerminalX" in short,
            f"Got: {short}"
        )
        
        # Test format_json (pretty)
        json_pretty = self.version_module.format_json(pretty=True)
        self.log_result(
            "VersionModule.format_json(pretty=True)",
            json_pretty.count('\n') > 0,  # Should have newlines
            "Pretty formatted"
        )
        
        # Test format_json (compact)
        json_compact = self.version_module.format_json(pretty=False)
        self.log_result(
            "VersionModule.format_json(pretty=False)",
            json_compact.count('\n') == 0,  # Should be single line
            "Compact formatted"
        )
        
        # Verify JSON is valid
        try:
            json.loads(json_pretty)
            self.log_result(
                "VersionModule.format_json() - valid JSON",
                True,
                "JSON is valid"
            )
        except:
            self.log_result(
                "VersionModule.format_json() - valid JSON",
                False,
                "JSON is invalid"
            )
        
    async def test_commands_map(self):
        """Test commands mapping"""
        print("\n=== Testing commands mapping ===")
        
        commands = self.version_module.get_commands()
        self.log_result(
            "VersionModule.get_commands()",
            isinstance(commands, dict) and len(commands) > 0,
            f"Found {len(commands)} commands"
        )
        
        # Check for expected commands
        expected_commands = ['version', 'semver', 'short', 'info', 'json', 'set-build', 'set-tag']
        for cmd in expected_commands:
            self.log_result(
                f"Commands map contains '{cmd}'",
                cmd in commands,
                f"Description: {commands.get(cmd, 'N/A')}"
            )
        
    async def test_enable_disable(self):
        """Test enable/disable functionality"""
        print("\n=== Testing enable/disable ===")
        
        # Test enable
        await self.version_module.enable()
        self.log_result(
            "VersionModule.enable()",
            self.version_module.enabled == True,
            "Module enabled"
        )
        
        # Test disable
        await self.version_module.disable()
        self.log_result(
            "VersionModule.disable()",
            self.version_module.enabled == False,
            "Module disabled"
        )
        
        # Re-enable for other tests
        await self.version_module.enable()


class TestVersionCommands:
    """Test suite for VersionCommands"""
    
    def __init__(self):
        self.version_module = VersionModule()
        self.version_commands = VersionCommands(self.version_module)
        self.test_results = []
        self.logger = Logger()
        
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
        self.version_module.set_logger(self.logger)
        await self.version_module.initialize()
        print("Setup complete")
        
    async def teardown(self):
        """Cleanup test environment"""
        print("\n=== Cleaning up test environment ===")
        print("Teardown complete")
        
    async def test_version_commands(self):
        """Test all version commands"""
        print("\n=== Testing version commands ===")
        
        # Test cmd_version
        result = await self.version_commands.cmd_version()
        self.log_result(
            "cmd_version()",
            result['success'] and 'version' in result,
            f"Output: {result.get('output', '')[:50]}"
        )
        
        # Test cmd_semver
        result = await self.version_commands.cmd_semver()
        self.log_result(
            "cmd_semver()",
            result['success'] and result['semver'] == "1.0.9",
            f"Got: {result.get('semver', '')}"
        )
        
        # Test cmd_short
        result = await self.version_commands.cmd_short()
        self.log_result(
            "cmd_short()",
            result['success'] and 'TerminalX' in result['output'],
            f"Output: {result.get('output', '')[:50]}"
        )
        
        # Test cmd_info
        result = await self.version_commands.cmd_info()
        self.log_result(
            "cmd_info()",
            result['success'] and 'Version:' in result['output'],
            f"Contains version info"
        )
        
        # Test cmd_json
        result = await self.version_commands.cmd_json()
        self.log_result(
            "cmd_json()",
            result['success'],
            f"JSON output generated"
        )
        
        # Verify JSON is valid
        try:
            json.loads(result['json'])
            self.log_result(
                "cmd_json() - valid JSON",
                True,
                "JSON is valid"
            )
        except:
            self.log_result(
                "cmd_json() - valid JSON",
                False,
                "JSON is invalid"
            )
        
        # Test cmd_json_compact
        result = await self.version_commands.cmd_json_compact()
        self.log_result(
            "cmd_json_compact()",
            result['success'],
            f"Compact JSON generated"
        )
        
        # Test cmd_all
        result = await self.version_commands.cmd_all()
        self.log_result(
            "cmd_all()",
            result['success'] and 'human' in result and 'json' in result,
            f"Contains both formats"
        )
        
        # Test cmd_set_build
        result = await self.version_commands.cmd_set_build("1234")
        self.log_result(
            "cmd_set_build()",
            result['success'] and result['build'] == 1234,
            f"Build set to: {result.get('build', '')}"
        )
        
        # Test cmd_set_build with invalid input
        result = await self.version_commands.cmd_set_build("invalid")
        self.log_result(
            "cmd_set_build() - invalid input",
            not result['success'],
            f"Error: {result.get('error', '')}"
        )
        
        # Test cmd_set_tag
        result = await self.version_commands.cmd_set_tag("alpha")
        self.log_result(
            "cmd_set_tag()",
            result['success'] and result['tag'] == "alpha",
            f"Tag set to: {result.get('tag', '')}"
        )
        
        # Test cmd_commands
        result = await self.version_commands.cmd_commands()
        self.log_result(
            "cmd_commands()",
            result['success'] and 'commands' in result,
            f"Found {len(result.get('commands', {}))} commands"
        )
        
        # Test cmd_enable
        result = await self.version_commands.cmd_enable()
        self.log_result(
            "cmd_enable()",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        # Test cmd_disable
        result = await self.version_commands.cmd_disable()
        self.log_result(
            "cmd_disable()",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        # Re-enable for cleanup
        await self.version_module.enable()
        
    async def test_error_handling(self):
        """Test error handling"""
        print("\n=== Testing error handling ===")
        
        # Test unknown command
        result = await self.version_commands.execute("unknown_command", [])
        self.log_result(
            "execute() - unknown command",
            not result['success'],
            f"Error: {result.get('error', '')}"
        )
        
        # Test cmd_set_build without args
        result = await self.version_commands.cmd_set_build()
        self.log_result(
            "cmd_set_build() - no args",
            not result['success'],
            f"Error: {result.get('error', '')}"
        )
        
        # Test cmd_set_tag without args
        result = await self.version_commands.cmd_set_tag()
        self.log_result(
            "cmd_set_tag() - no args",
            not result['success'],
            f"Error: {result.get('error', '')}"
        )


async def main():
    """Main test runner"""
    print("=" * 60)
    print("VersionModule Test Suite")
    print("=" * 60)
    
    # Test VersionModule
    module_tester = TestVersionModule()
    try:
        await module_tester.setup()
        await module_tester.test_version_info()
        await module_tester.test_version_module_api()
        await module_tester.test_formatting()
        await module_tester.test_commands_map()
        await module_tester.test_enable_disable()
        await module_tester.teardown()
        
        module_passed = sum(1 for r in module_tester.test_results if r['passed'])
        module_total = len(module_tester.test_results)
        
        print("\n" + "=" * 60)
        print("VersionModule Test Summary")
        print("=" * 60)
        print(f"Total tests: {module_total}")
        print(f"Passed: {module_passed}")
        print(f"Failed: {module_total - module_passed}")
        print(f"Success rate: {(module_passed/module_total)*100:.1f}%")
        
    except Exception as e:
        print(f"\n✗ VersionModule test suite failed: {e}")
        import traceback
        traceback.print_exc()
        module_passed = 0
        module_total = 0
    
    # Test VersionCommands
    print("\n" + "=" * 60)
    print("VersionCommands Test Suite")
    print("=" * 60)
    
    commands_tester = TestVersionCommands()
    try:
        await commands_tester.setup()
        await commands_tester.test_version_commands()
        await commands_tester.test_error_handling()
        await commands_tester.teardown()
        
        commands_passed = sum(1 for r in commands_tester.test_results if r['passed'])
        commands_total = len(commands_tester.test_results)
        
        print("\n" + "=" * 60)
        print("VersionCommands Test Summary")
        print("=" * 60)
        print(f"Total tests: {commands_total}")
        print(f"Passed: {commands_passed}")
        print(f"Failed: {commands_total - commands_passed}")
        print(f"Success rate: {(commands_passed/commands_total)*100:.1f}%")
        
    except Exception as e:
        print(f"\n✗ VersionCommands test suite failed: {e}")
        import traceback
        traceback.print_exc()
        commands_passed = 0
        commands_total = 0
    
    # Overall summary
    total_passed = module_passed + commands_passed
    total_tests = module_total + commands_total
    
    print("\n" + "=" * 60)
    print("Overall Test Summary")
    print("=" * 60)
    print(f"Total tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    print(f"Success rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_passed == total_tests:
        print("\n✓ All tests passed!")
        return True
    else:
        print("\n✗ Some tests failed")
        return False


if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
