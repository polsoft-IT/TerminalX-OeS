#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test suite for ReportEngine and ReportCommands
Tests all report functionality and integration with TerminalX
"""

import asyncio
import os
import sys
import json
import importlib.util
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Direct imports to avoid __init__.py issues
spec = importlib.util.spec_from_file_location("report_engine", os.path.join(os.path.dirname(__file__), "..", "report", "report_engine.py"))
report_engine_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report_engine_module)
ReportEngine = report_engine_module.ReportEngine
Report = report_engine_module.Report
ReportSection = report_engine_module.ReportSection

spec = importlib.util.spec_from_file_location("report_commands", os.path.join(os.path.dirname(__file__), "..", "commands", "report.py"))
commands_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(commands_module)
ReportCommands = commands_module.ReportCommands

from core import Logger


class TestReportEngine:
    """Test suite for ReportEngine"""
    
    def __init__(self):
        self.report_engine = report_engine_module.create_default_engine()
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
        self.report_engine.set_logger(self.logger)
        await self.report_engine.initialize()
        print("Setup complete")
        
    async def teardown(self):
        """Cleanup test environment"""
        print("\n=== Cleaning up test environment ===")
        print("Teardown complete")
        
    async def test_report_creation(self):
        """Test report creation"""
        print("\n=== Testing report creation ===")
        
        # Test create_report
        report = self.report_engine.create_report("Test Report")
        
        self.log_result(
            "Report created with ID",
            report.id is not None,
            f"ID: {report.id}"
        )
        
        self.log_result(
            "Report title set correctly",
            report.title == "Test Report",
            f"Title: {report.title}"
        )
        
        self.log_result(
            "Report has created_at timestamp",
            report.created_at > 0,
            f"Created: {report.created_at}"
        )
        
        self.log_result(
            "Report has empty sections list",
            len(report.sections) == 0,
            f"Sections: {len(report.sections)}"
        )
        
    async def test_report_sections(self):
        """Test report sections"""
        print("\n=== Testing report sections ===")
        
        report = self.report_engine.create_report("Section Test Report")
        
        # Test add_section
        section = report.add_section("Section 1", "Content 1")
        
        self.log_result(
            "Section added successfully",
            section.id is not None,
            f"Section ID: {section.id}"
        )
        
        self.log_result(
            "Section title set correctly",
            section.title == "Section 1",
            f"Title: {section.title}"
        )
        
        self.log_result(
            "Section content set correctly",
            section.content == "Content 1",
            f"Content: {section.content}"
        )
        
        self.log_result(
            "Section added to report",
            len(report.sections) == 1,
            f"Sections: {len(report.sections)}"
        )
        
        # Test multiple sections
        report.add_section("Section 2", "Content 2", level=2)
        report.add_section("Section 3", "Content 3", level=3)
        
        self.log_result(
            "Multiple sections added",
            len(report.sections) == 3,
            f"Sections: {len(report.sections)}"
        )
        
    async def test_template_generation(self):
        """Test template generation"""
        print("\n=== Testing template generation ===")
        
        data = {
            "title": "Template Test Report",
            "sections": [
                {"title": "Overview", "content": "System overview"},
                {"title": "Details", "content": "Detailed information", "level": 2}
            ]
        }
        
        try:
            report = self.report_engine.from_template("simple_template", data)
            
            self.log_result(
                "Report generated from template",
                report.id is not None,
                f"ID: {report.id}"
            )
            
            self.log_result(
                "Report title from data",
                report.title == "Template Test Report",
                f"Title: {report.title}"
            )
            
            self.log_result(
                "Sections generated from data",
                len(report.sections) == 2,
                f"Sections: {len(report.sections)}"
            )
            
        except Exception as e:
            self.log_result(
                "Template generation",
                False,
                f"Error: {str(e)}"
            )
    
    async def test_rendering(self):
        """Test report rendering"""
        print("\n=== Testing report rendering ===")
        
        report = self.report_engine.create_report("Render Test Report")
        report.add_section("Section 1", "Content 1")
        
        # Test TXT format
        try:
            output = self.report_engine.render(report, "txt")
            self.log_result(
                "TXT rendering successful",
                len(output) > 0,
                f"Size: {len(output)} bytes"
            )
            
            text = output.decode('utf-8')
            self.log_result(
                "TXT contains report title",
                "Render Test Report" in text,
                "Title found in output"
            )
            
        except Exception as e:
            self.log_result(
                "TXT rendering",
                False,
                f"Error: {str(e)}"
            )
        
        # Test JSON format
        try:
            output = self.report_engine.render(report, "json")
            self.log_result(
                "JSON rendering successful",
                len(output) > 0,
                f"Size: {len(output)} bytes"
            )
            
            # Verify it's valid JSON
            json_data = json.loads(output.decode('utf-8'))
            self.log_result(
                "JSON is valid",
                json_data is not None,
                "JSON parsed successfully"
            )
            
            self.log_result(
                "JSON contains report data",
                'id' in json_data and 'title' in json_data,
                "Required fields present"
            )
            
        except Exception as e:
            self.log_result(
                "JSON rendering",
                False,
                f"Error: {str(e)}"
            )
        
        # Test MD format
        try:
            output = self.report_engine.render(report, "md")
            self.log_result(
                "MD rendering successful",
                len(output) > 0,
                f"Size: {len(output)} bytes"
            )
            
            text = output.decode('utf-8')
            self.log_result(
                "MD contains markdown header",
                "# Render Test Report" in text,
                "Markdown header found"
            )
            
        except Exception as e:
            self.log_result(
                "MD rendering",
                False,
                f"Error: {str(e)}"
            )
    
    async def test_save_to_file(self):
        """Test saving report to file"""
        print("\n=== Testing save to file ===")
        
        report = self.report_engine.create_report("Save Test Report")
        report.add_section("Section 1", "Content 1")
        
        test_file = os.path.join(os.path.dirname(__file__), "test_report.txt")
        
        try:
            saved_path = self.report_engine.save_to_file(report, test_file, "txt")
            
            self.log_result(
                "Report saved to file",
                os.path.exists(saved_path),
                f"File: {saved_path}"
            )
            
            # Verify file content
            with open(saved_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            self.log_result(
                "File contains report content",
                "Save Test Report" in content,
                "Content verified"
            )
            
            # Cleanup
            if os.path.exists(saved_path):
                os.remove(saved_path)
                
        except Exception as e:
            self.log_result(
                "Save to file",
                False,
                f"Error: {str(e)}"
            )
    
    async def test_plugin_system(self):
        """Test plugin system"""
        print("\n=== Testing plugin system ===")
        
        # Test plugin registry
        template_plugins = self.report_engine.registry.get_template_plugins()
        self.log_result(
            "Template plugins available",
            len(template_plugins) > 0,
            f"Count: {len(template_plugins)}"
        )
        
        output_plugins = self.report_engine.registry.get_output_plugins()
        self.log_result(
            "Output plugins available",
            len(output_plugins) > 0,
            f"Count: {len(output_plugins)}"
        )
        
        filter_plugins = self.report_engine.registry.get_filter_plugins()
        self.log_result(
            "Filter plugins available",
            len(filter_plugins) > 0,
            f"Count: {len(filter_plugins)}"
        )
        
        postprocess_plugins = self.report_engine.registry.get_postprocess_plugins()
        self.log_result(
            "Post-process plugins available",
            len(postprocess_plugins) > 0,
            f"Count: {len(postprocess_plugins)}"
        )
        
        # Test supported formats
        formats = set()
        for plugin in output_plugins:
            formats.update(plugin.supported_formats())
        
        self.log_result(
            "Output formats available",
            len(formats) > 0,
            f"Formats: {sorted(formats)}"
        )
    
    async def test_commands_api(self):
        """Test commands API"""
        print("\n=== Testing commands API ===")
        
        commands = self.report_engine.get_commands()
        self.log_result(
            "Commands API returns dict",
            isinstance(commands, dict),
            f"Type: {type(commands)}"
        )
        
        self.log_result(
            "Commands available",
            len(commands) > 0,
            f"Count: {len(commands)}"
        )
        
        # Check for expected commands
        expected_commands = ['create', 'template', 'render', 'save', 'display', 'plugins', 'formats']
        for cmd in expected_commands:
            self.log_result(
                f"Commands map contains '{cmd}'",
                cmd in commands,
                f"Description: {commands.get(cmd, 'N/A')}"
            )
    
    async def test_enable_disable(self):
        """Test enable/disable functionality"""
        print("\n=== Testing enable/disable ===")
        
        # Test disable
        await self.report_engine.disable()
        self.log_result(
            "Report engine disabled",
            not self.report_engine.enabled,
            "Engine disabled"
        )
        
        # Test enable
        await self.report_engine.enable()
        self.log_result(
            "Report engine enabled",
            self.report_engine.enabled,
            "Engine enabled"
        )


class TestReportCommands:
    """Test suite for ReportCommands"""
    
    def __init__(self):
        self.report_engine = report_engine_module.create_default_engine()
        self.report_commands = ReportCommands(self.report_engine)
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
        self.report_engine.set_logger(self.logger)
        await self.report_engine.initialize()
        print("Setup complete")
        
    async def teardown(self):
        """Cleanup test environment"""
        print("\n=== Cleaning up test environment ===")
        print("Teardown complete")
        
    async def test_create_command(self):
        """Test create command"""
        print("\n=== Testing create command ===")
        
        result = await self.report_commands.cmd_create("Test Report")
        
        self.log_result(
            "cmd_create() success",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        self.log_result(
            "cmd_create() returns report_id",
            'report_id' in result,
            f"ID: {result.get('report_id', '')}"
        )
        
        self.log_result(
            "Report stored in commands",
            result.get('report_id') in self.report_commands.reports,
            "Report accessible"
        )
        
        # Test without args
        result = await self.report_commands.cmd_create()
        self.log_result(
            "cmd_create() without args fails",
            not result['success'],
            f"Error: {result.get('error', '')}"
        )
    
    async def test_template_command(self):
        """Test template command"""
        print("\n=== Testing template command ===")
        
        data = {
            "title": "Template Test",
            "sections": [{"title": "Section 1", "content": "Content 1"}]
        }
        
        result = await self.report_commands.cmd_template("simple_template", json.dumps(data))
        
        self.log_result(
            "cmd_template() success",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        self.log_result(
            "cmd_template() returns report_id",
            'report_id' in result,
            f"ID: {result.get('report_id', '')}"
        )
        
        # Test without args
        result = await self.report_commands.cmd_template()
        self.log_result(
            "cmd_template() without args fails",
            not result['success'],
            f"Error: {result.get('error', '')}"
        )
    
    async def test_render_command(self):
        """Test render command"""
        print("\n=== Testing render command ===")
        
        # First create a report
        create_result = await self.report_commands.cmd_create("Render Test")
        report_id = create_result['report_id']
        
        # Test render
        result = await self.report_commands.cmd_render(report_id, "txt")
        
        self.log_result(
            "cmd_render() success",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        self.log_result(
            "cmd_render() returns content",
            'content' in result,
            f"Content length: {len(result.get('content', ''))}"
        )
        
        # Test with invalid report_id
        result = await self.report_commands.cmd_render("invalid_id", "txt")
        self.log_result(
            "cmd_render() with invalid ID fails",
            not result['success'],
            f"Error: {result.get('error', '')}"
        )
    
    async def test_save_command(self):
        """Test save command"""
        print("\n=== Testing save command ===")
        
        # First create a report
        create_result = await self.report_commands.cmd_create("Save Test")
        report_id = create_result['report_id']
        
        test_file = os.path.join(os.path.dirname(__file__), "test_save.txt")
        
        # Test save
        result = await self.report_commands.cmd_save(report_id, test_file)
        
        self.log_result(
            "cmd_save() success",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        self.log_result(
            "File created",
            os.path.exists(test_file),
            f"File: {test_file}"
        )
        
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        
        # Test without args
        result = await self.report_commands.cmd_save()
        self.log_result(
            "cmd_save() without args fails",
            not result['success'],
            f"Error: {result.get('error', '')}"
        )
    
    async def test_display_command(self):
        """Test display command"""
        print("\n=== Testing display command ===")
        
        # First create a report
        create_result = await self.report_commands.cmd_create("Display Test")
        report_id = create_result['report_id']
        
        # Test display
        result = await self.report_commands.cmd_display(report_id)
        
        self.log_result(
            "cmd_display() success",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        # Test with invalid report_id
        result = await self.report_commands.cmd_display("invalid_id")
        self.log_result(
            "cmd_display() with invalid ID fails",
            not result['success'],
            f"Error: {result.get('error', '')}"
        )
    
    async def test_plugins_command(self):
        """Test plugins command"""
        print("\n=== Testing plugins command ===")
        
        result = await self.report_commands.cmd_plugins()
        
        self.log_result(
            "cmd_plugins() success",
            result['success'],
            f"Output contains plugin info"
        )
        
        self.log_result(
            "cmd_plugins() returns output",
            'output' in result,
            f"Output length: {len(result.get('output', ''))}"
        )
    
    async def test_formats_command(self):
        """Test formats command"""
        print("\n=== Testing formats command ===")
        
        result = await self.report_commands.cmd_formats()
        
        self.log_result(
            "cmd_formats() success",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        self.log_result(
            "cmd_formats() returns formats list",
            'formats' in result,
            f"Formats: {result.get('formats', [])}"
        )
    
    async def test_list_command(self):
        """Test list command"""
        print("\n=== Testing list command ===")
        
        # First create some reports
        await self.report_commands.cmd_create("Report 1")
        await self.report_commands.cmd_create("Report 2")
        
        result = await self.report_commands.cmd_list()
        
        self.log_result(
            "cmd_list() success",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        self.log_result(
            "cmd_list() returns count",
            'count' in result,
            f"Count: {result.get('count', 0)}"
        )
        
        self.log_result(
            "cmd_list() shows reports",
            result.get('count', 0) > 0,
            f"Reports found: {result.get('count', 0)}"
        )
    
    async def test_add_section_command(self):
        """Test add_section command"""
        print("\n=== Testing add_section command ===")
        
        # First create a report
        create_result = await self.report_commands.cmd_create("Section Test")
        report_id = create_result['report_id']
        
        # Test add_section
        result = await self.report_commands.cmd_add_section(report_id, "New Section", "New Content")
        
        self.log_result(
            "cmd_add_section() success",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        self.log_result(
            "cmd_add_section() returns section_id",
            'section_id' in result,
            f"Section ID: {result.get('section_id', '')}"
        )
        
        # Test without args
        result = await self.report_commands.cmd_add_section()
        self.log_result(
            "cmd_add_section() without args fails",
            not result['success'],
            f"Error: {result.get('error', '')}"
        )
    
    async def test_enable_disable_commands(self):
        """Test enable/disable commands"""
        print("\n=== Testing enable/disable commands ===")
        
        # Test enable
        result = await self.report_commands.cmd_enable()
        self.log_result(
            "cmd_enable() success",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        # Test disable
        result = await self.report_commands.cmd_disable()
        self.log_result(
            "cmd_disable() success",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        # Re-enable for cleanup
        await self.report_engine.enable()
    
    async def test_commands_command(self):
        """Test commands command"""
        print("\n=== Testing commands command ===")
        
        result = await self.report_commands.cmd_commands()
        
        self.log_result(
            "cmd_commands() success",
            result['success'],
            f"Output: {result.get('output', '')}"
        )
        
        self.log_result(
            "cmd_commands() returns commands dict",
            'commands' in result,
            f"Commands: {list(result.get('commands', {}).keys())}"
        )


async def main():
    """Main test runner"""
    print("=" * 60)
    print("ReportEngine Test Suite")
    print("=" * 60)
    
    # Test ReportEngine
    engine_tester = TestReportEngine()
    try:
        await engine_tester.setup()
        await engine_tester.test_report_creation()
        await engine_tester.test_report_sections()
        await engine_tester.test_template_generation()
        await engine_tester.test_rendering()
        await engine_tester.test_save_to_file()
        await engine_tester.test_plugin_system()
        await engine_tester.test_commands_api()
        await engine_tester.test_enable_disable()
        await engine_tester.teardown()
        
        engine_passed = sum(1 for r in engine_tester.test_results if r['passed'])
        engine_total = len(engine_tester.test_results)
        
        print("\n" + "=" * 60)
        print("ReportEngine Test Summary")
        print("=" * 60)
        print(f"Total tests: {engine_total}")
        print(f"Passed: {engine_passed}")
        print(f"Failed: {engine_total - engine_passed}")
        print(f"Success rate: {(engine_passed/engine_total)*100:.1f}%")
        
    except Exception as e:
        print(f"\n✗ ReportEngine test suite failed: {e}")
        import traceback
        traceback.print_exc()
        engine_passed = 0
        engine_total = 0
    
    # Test ReportCommands
    print("\n" + "=" * 60)
    print("ReportCommands Test Suite")
    print("=" * 60)
    
    commands_tester = TestReportCommands()
    try:
        await commands_tester.setup()
        await commands_tester.test_create_command()
        await commands_tester.test_template_command()
        await commands_tester.test_render_command()
        await commands_tester.test_save_command()
        await commands_tester.test_display_command()
        await commands_tester.test_plugins_command()
        await commands_tester.test_formats_command()
        await commands_tester.test_list_command()
        await commands_tester.test_add_section_command()
        await commands_tester.test_enable_disable_commands()
        await commands_tester.test_commands_command()
        await commands_tester.teardown()
        
        commands_passed = sum(1 for r in commands_tester.test_results if r['passed'])
        commands_total = len(commands_tester.test_results)
        
        print("\n" + "=" * 60)
        print("ReportCommands Test Summary")
        print("=" * 60)
        print(f"Total tests: {commands_total}")
        print(f"Passed: {commands_passed}")
        print(f"Failed: {commands_total - commands_passed}")
        print(f"Success rate: {(commands_passed/commands_total)*100:.1f}%")
        
    except Exception as e:
        print(f"\n✗ ReportCommands test suite failed: {e}")
        import traceback
        traceback.print_exc()
        commands_passed = 0
        commands_total = 0
    
    # Overall summary
    total_passed = engine_passed + commands_passed
    total_tests = engine_total + commands_total
    
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
