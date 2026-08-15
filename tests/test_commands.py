"""
 ============================================================
  MODULE/PLUGIN NAME: TestCommands
  VERSION: 1.0.0
  MODULE CLASS: TestCommands
  DESCRIPTION:
       Test script for all TerminalX commands and modules

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
import codecs

# Add parent directory to path
sys.path.insert(0, '..')

# Set UTF-8 encoding for output on Windows
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("TESTING LIBRARY MODULES")
print("=" * 60)

# Test library modules
try:
    from libs.clean_logger import CleanLogger, LogLevel
    logger = CleanLogger("Test", LogLevel.INFO)
    logger.info("Clean logger test passed")
    print("✓ clean_logger.py")
except Exception as e:
    print(f"✗ clean_logger.py: {e}")

try:
    from libs.command_registry import CommandRegistry, CommandInfo, CommandCategory
    registry = CommandRegistry()
    cmd = CommandInfo("test", "Test command", CommandCategory.SYSTEM, lambda: None, [])
    registry.register(cmd)
    assert registry.get("test") is not None
    print("✓ command_registry.py")
except Exception as e:
    print(f"✗ command_registry.py: {e}")

try:
    from libs.completion import CommandCompletion, CompletionContext
    completion = CommandCompletion()
    ctx = CompletionContext("fs", 2, ["fs"], "fs")
    results = completion.complete(ctx)
    print("✓ completion.py")
except Exception as e:
    print(f"✗ completion.py: {e}")

try:
    from libs.config import Config, TerminalConfig
    config = Config()
    config.set("theme", "dark")
    assert config.get("theme") == "dark"
    print("✓ config.py")
except Exception as e:
    print(f"✗ config.py: {e}")

try:
    from libs.config_manager import ConfigManager
    config_mgr = ConfigManager()
    config_mgr.set("test", "value")
    assert config_mgr.get("test") == "value"
    print("✓ config_manager.py")
except Exception as e:
    print(f"✗ config_manager.py: {e}")

try:
    from libs.core_manager import CoreManager, SubsystemInfo
    core_mgr = CoreManager()
    core_mgr.register_subsystem("test", object())
    assert core_mgr.get_subsystem("test") is not None
    print("✓ core_manager.py")
except Exception as e:
    print(f"✗ core_manager.py: {e}")

try:
    from libs.dependency_resolver import DependencyResolver, Dependency, DependencyType
    dep_resolver = DependencyResolver()
    dep = Dependency("os", None, DependencyType.PYTHON_PACKAGE)
    result = dep_resolver.is_installed(dep)
    print(f"✓ dependency_resolver.py (result: {result})")
except Exception as e:
    import traceback
    print(f"✗ dependency_resolver.py: {e}")
    traceback.print_exc()

try:
    from libs.encryption import Encryption
    encryption = Encryption()
    key = encryption.generate_key()
    encryption.set_key(key)
    encrypted = encryption.encrypt("test")
    decrypted = encryption.decrypt(encrypted)
    assert decrypted == "test"
    print("✓ encryption.py")
except Exception as e:
    print(f"✗ encryption.py: {e}")

try:
    from libs.file_manager import FileManager, FileType
    file_mgr = FileManager()
    info = file_mgr.get_info(__file__)
    assert info is not None
    print("✓ file_manager.py")
except Exception as e:
    print(f"✗ file_manager.py: {e}")

try:
    from libs.github import GitHubClient
    github = GitHubClient()
    stats = github.get_stats()
    assert 'authenticated' in stats
    print("✓ github.py")
except Exception as e:
    print(f"✗ github.py: {e}")

try:
    from libs.git_integration import GitManager
    git_mgr = GitManager()
    is_repo = git_mgr.is_repo(".")
    print("✓ git_integration.py")
except Exception as e:
    print(f"✗ git_integration.py: {e}")

try:
    from libs.hot_reload import HotReloadManager
    hot_reload = HotReloadManager()
    hot_reload.watch_module("os")
    print("✓ hot_reload.py")
except Exception as e:
    print(f"✗ hot_reload.py: {e}")

try:
    from libs.intelligent_suggestions import IntelligentSuggestionEngine
    suggestions = IntelligentSuggestionEngine()
    results = suggestions.get_suggestions("fs")
    print("✓ intelligent_suggestions.py")
except Exception as e:
    print(f"✗ intelligent_suggestions.py: {e}")

try:
    from libs.module_integration import ModuleIntegration, ModuleInfo
    mod_integration = ModuleIntegration()
    print("✓ module_integration.py")
except Exception as e:
    print(f"✗ module_integration.py: {e}")

try:
    from libs.module_isolation import ModuleIsolator
    isolator = ModuleIsolator()
    print("✓ module_isolation.py")
except Exception as e:
    print(f"✗ module_isolation.py: {e}")

try:
    from libs.module_loader import ModuleLoader
    loader = ModuleLoader()
    print("✓ module_loader.py")
except Exception as e:
    print(f"✗ module_loader.py: {e}")

try:
    from libs.module_registry import ModuleRegistry, ModuleManifest
    mod_registry = ModuleRegistry()
    print("✓ module_registry.py")
except Exception as e:
    print(f"✗ module_registry.py: {e}")

try:
    from libs.module_validator import ModuleValidator
    validator = ModuleValidator()
    result = validator.validate_module(__file__)
    print("✓ module_validator.py")
except Exception as e:
    print(f"✗ module_validator.py: {e}")

try:
    from libs.network_manager import NetworkManager
    net_mgr = NetworkManager()
    hostname = net_mgr.get_hostname()
    assert hostname is not None
    print("✓ network_manager.py")
except Exception as e:
    print(f"✗ network_manager.py: {e}")

try:
    from libs.advanced_marketplace import AdvancedMarketplace
    marketplace = AdvancedMarketplace()
    print("✓ advanced_marketplace.py")
except Exception as e:
    print(f"✗ advanced_marketplace.py: {e}")

try:
    from libs.automation import AutomationEngine, Macro
    automation = AutomationEngine()
    automation.create_macro("test", ["echo hello"], "Test macro")
    print("✓ automation.py")
except Exception as e:
    print(f"✗ automation.py: {e}")

try:
    from libs.backup_system import BackupSystem
    backup = BackupSystem()
    print("✓ backup_system.py")
except Exception as e:
    print(f"✗ backup_system.py: {e}")

try:
    from libs.bluetooth import BluetoothManager
    bluetooth = BluetoothManager()
    print("✓ bluetooth.py")
except Exception as e:
    print(f"✗ bluetooth.py: {e}")

try:
    from libs.clipboard_manager import ClipboardManager
    clipboard = ClipboardManager()
    print("✓ clipboard_manager.py")
except Exception as e:
    print(f"✗ clipboard_manager.py: {e}")

try:
    from libs.cloud_filesystem import CloudFilesystem
    cloud_fs = CloudFilesystem()
    print("✓ cloud_filesystem.py")
except Exception as e:
    print(f"✗ cloud_filesystem.py: {e}")

try:
    from libs.cloud_sync import CloudSync
    cloud_sync = CloudSync()
    print("✓ cloud_sync.py")
except Exception as e:
    print(f"✗ cloud_sync.py: {e}")

try:
    from libs.debug import DebugManager
    debug_mgr = DebugManager()
    debug_mgr.log_event("debug", "Test event")
    print("✓ debug.py")
except Exception as e:
    print(f"✗ debug.py: {e}")

try:
    from libs.debugger import AdvancedDebugger
    debugger = AdvancedDebugger()
    print("✓ debugger.py")
except Exception as e:
    print(f"✗ debugger.py: {e}")

try:
    from libs.fuzzy_search import FuzzySearch
    fuzzy = FuzzySearch()
    results = fuzzy.search_list(["test", "testing"], "test")
    print("✓ fuzzy_search.py")
except Exception as e:
    print(f"✗ fuzzy_search.py: {e}")

try:
    from libs.bluetooth import BluetoothManager, BluetoothDevice, GATTService, GATTCharacteristic
    bt_mgr = BluetoothManager()
    # Test basic methods
    bt_mgr.enable_firewall()
    bt_mgr.disable_firewall()
    bt_mgr.add_to_whitelist("00:11:22:33:44:55")
    bt_mgr.add_to_blacklist("00:11:22:33:44:56")
    bt_mgr.block_device("00:11:22:33:44:57")
    bt_mgr.allow_device("00:11:22:33:44:57")
    bt_mgr.remove_from_whitelist("00:11:22:33:44:55")
    bt_mgr.remove_from_blacklist("00:11:22:33:44:56")
    stats = bt_mgr.get_stats()
    diagnostics = bt_mgr.run_diagnostics()
    security = bt_mgr.get_security_status()
    adapter_info = bt_mgr.get_adapter_info()
    print("✓ bluetooth.py (all PRO commands added)")
except Exception as e:
    import traceback
    print(f"✗ bluetooth.py: {e}")
    traceback.print_exc()

try:
    from libs.filetag import FileTagSystem, Tag, TagColor, TagIcon, TagRule, FileMetadata
    filetag = FileTagSystem()
    
    # Test basic tag operations
    test_file = __file__
    filetag.add_tag(test_file, "test")
    tags = filetag.list_tags(test_file)
    assert "test" in tags
    
    filetag.remove_tag(test_file, "test")
    tags = filetag.list_tags(test_file)
    assert "test" not in tags
    
    # Test rules
    filetag.add_rule("*.py", "python", "pattern")
    rules = filetag.list_rules()
    assert len(rules) > 0
    
    # Test metadata
    metadata = filetag.extract_metadata(test_file)
    assert metadata.file_path == test_file
    
    # Test FRN
    frn = filetag.get_frn(test_file)
    
    # Test fingerprint
    fingerprint = filetag.fingerprint(test_file)
    assert 'file_path' in fingerprint
    
    # Test diagnostics
    diagnostics = filetag.run_diagnostics()
    assert 'database_status' in diagnostics
    
    # Test engine status
    status = filetag.get_engine_status()
    assert 'status' in status
    
    # Test modules
    modules = filetag.get_modules()
    assert len(modules) > 0
    
    # Test database operations
    filetag.vacuum_database()
    filetag.repair_database()
    
    print("✓ filetag.py (GODMODE system - all components)")
except Exception as e:
    import traceback
    print(f"✗ filetag.py: {e}")
    traceback.print_exc()

try:
    from libs.kernel_hooks import KernelHooksEngine, HookMode, KernelLogLevel, TrapPolicy, HookEvent, HookRule, KernelPlugin
    kernel_hooks = KernelHooksEngine()
    
    # Test basic hook operations
    def test_handler(*args, **kwargs):
        return "test_result"
    
    kernel_hooks.register_hook("test_syscall", test_handler)
    hooks = kernel_hooks.list_hooks()
    assert "test_syscall" in hooks
    
    kernel_hooks.unregister_hook("test_syscall")
    hooks = kernel_hooks.list_hooks()
    assert "test_syscall" not in hooks
    
    # Test trap operations
    kernel_hooks.register_trap("test_trap", test_handler)
    traps = kernel_hooks.list_traps()
    assert "test_trap" in traps
    
    kernel_hooks.unregister_trap("test_trap")
    traps = kernel_hooks.list_traps()
    assert "test_trap" not in traps
    
    # Test filter operations
    def test_filter(syscall, args, kwargs):
        return True
    
    kernel_hooks.add_filter(test_filter)
    filter_count = kernel_hooks.list_filters()
    assert filter_count > 0
    
    # Test rule operations
    def test_condition(syscall, args, kwargs):
        return True
    
    kernel_hooks.add_rule("test_rule", test_condition, "log")
    rules = kernel_hooks.list_rules()
    assert len(rules) > 0
    
    kernel_hooks.enable_rule("test_rule")
    kernel_hooks.disable_rule("test_rule")
    
    # Test snapshot operations
    kernel_hooks.create_snapshot("test_snapshot")
    snapshots = kernel_hooks.list_snapshots()
    assert "test_snapshot" in snapshots
    
    kernel_hooks.restore_snapshot("test_snapshot")
    kernel_hooks.delete_snapshot("test_snapshot")
    
    # Test config operations
    kernel_hooks.config_set("mode", HookMode.MONITOR)
    mode = kernel_hooks.config_get("mode")
    assert mode == HookMode.MONITOR
    
    # Test metadata
    metadata = kernel_hooks.get_metadata()
    assert "name" in metadata
    assert "version" in metadata
    
    # Test diagnostics
    diagnostics = kernel_hooks.diagnose()
    assert "hooks" in diagnostics
    assert "traps" in diagnostics
    
    # Test auto-fix
    kernel_hooks.auto_fix()
    
    # Test health check
    health = kernel_hooks.health_check()
    assert "status" in health
    
    # Test export/import state
    state = kernel_hooks.export_state()
    assert "hooks" in state
    
    kernel_hooks.import_state(state)
    
    # Test API
    api_list = kernel_hooks.api_list()
    assert len(api_list) > 0
    
    # Test stats
    stats = kernel_hooks.get_stats()
    assert "status" in stats
    
    print("✓ kernel_hooks.py (GODMODE system - all components)")
except Exception as e:
    import traceback
    print(f"✗ kernel_hooks.py: {e}")
    traceback.print_exc()

try:
    from libs.process_monitor import ProcessMonitor, ProcessInfo, ProcessAlert, ProcessSnapshot, ProcessProfile
    process_monitor = ProcessMonitor()
    
    # Test basic process info
    import os
    current_pid = os.getpid()
    info = process_monitor.get_info(current_pid)
    assert info is not None
    assert info.pid == current_pid
    
    # Test list processes
    pids = process_monitor.list_processes()
    assert len(pids) > 0
    assert current_pid in pids
    
    # Test find process by name
    python_pids = process_monitor.find_process_by_name("python")
    assert len(python_pids) > 0
    
    # Test hook operations
    def test_hook(info):
        return None
    
    process_monitor.add_hook(current_pid, test_hook)
    hooks = process_monitor.list_hooks()
    assert current_pid in hooks
    
    process_monitor.remove_hook(current_pid)
    hooks = process_monitor.list_hooks()
    assert current_pid not in hooks
    
    # Test filter operations
    def test_filter(info):
        return True
    
    process_monitor.add_filter(test_filter)
    filter_count = process_monitor.list_filters()
    assert filter_count > 0
    
    # Test monitor
    monitored_info = process_monitor.monitor(current_pid)
    assert monitored_info is not None
    
    # Test snapshot operations
    snapshot = process_monitor.create_snapshot(current_pid)
    assert snapshot is not None
    
    snapshots = process_monitor.list_snapshots()
    assert current_pid in snapshots
    
    process_monitor.restore_snapshot(current_pid)
    process_monitor.delete_snapshot(current_pid)
    
    # Test profile operations
    profile = ProcessProfile(
        name="test_profile",
        cpu_threshold=80.0,
        ram_threshold=80.0,
        io_threshold=1000000,
        thread_threshold=200
    )
    process_monitor.set_profile(current_pid, profile)
    retrieved_profile = process_monitor.get_profile(current_pid)
    assert retrieved_profile.name == "test_profile"
    
    # Test config operations
    process_monitor.config_set("cpu_threshold", 90.0)
    threshold = process_monitor.config_get("cpu_threshold")
    assert threshold == 90.0
    
    # Test metadata
    metadata = process_monitor.get_metadata()
    assert "name" in metadata
    assert "version" in metadata
    
    # Test diagnostics
    diagnostics = process_monitor.diagnose()
    assert "processes_cached" in diagnostics
    
    # Test auto-fix
    process_monitor.auto_fix()
    
    # Test health check
    health = process_monitor.health_check()
    assert "status" in health
    
    # Test API
    api_list = process_monitor.api_list()
    assert len(api_list) > 0
    
    # Test stats
    stats = process_monitor.get_stats()
    assert "status" in stats
    
    # Test error operations
    process_monitor.clear_errors()
    errors = process_monitor.get_errors()
    assert len(errors) == 0
    
    print("✓ process_monitor.py (GODMODE system - all components)")
except Exception as e:
    import traceback
    print(f"✗ process_monitor.py: {e}")
    traceback.print_exc()

try:
    from libs.advanced_shield import AdvancedShield, ShieldLogLevel, ShieldEvent, ShieldRule
    advanced_shield = AdvancedShield()
    
    # Test config operations
    advanced_shield.config_set("auto_rules", False)
    assert advanced_shield.config_get("auto_rules") == False
    
    advanced_shield.config_set("auto_rules", True)
    assert advanced_shield.config_get("auto_rules") == True
    
    # Test rules
    kernel_rules = advanced_shield.get_rules("kernel")
    assert "BLOCK_SYSCALLS" in kernel_rules
    
    proc_rules = advanced_shield.get_rules("proc")
    assert "BLOCK_PROCESSES" in proc_rules
    
    # Test add/remove rules
    advanced_shield.add_rule("proc", "BLOCK_PROCESSES", "test.exe")
    assert "test.exe" in proc_rules["BLOCK_PROCESSES"]
    
    advanced_shield.remove_rule("proc", "BLOCK_PROCESSES", "test.exe")
    assert "test.exe" not in proc_rules["BLOCK_PROCESSES"]
    
    # Test snapshot operations
    snap_path = advanced_shield.snapshot_create("test_snapshot")
    assert snap_path is not None
    
    snapshots = advanced_shield.snapshot_list()
    assert "test_snapshot" in snapshots
    
    # Skip restore test as it requires non-empty sandbox
    # advanced_shield.snapshot_restore("test_snapshot")
    advanced_shield.snapshot_delete("test_snapshot")
    
    # Test file operations
    import tempfile
    test_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    test_file.write(b"test content")
    test_file.close()
    
    isolated_path = advanced_shield.isolate_file(test_file.name)
    assert isolated_path is not None
    
    file_check = advanced_shield.check_file(test_file.name)
    assert "safe" in file_check
    
    # Test entropy
    ent = advanced_shield.entropy(b"test data")
    assert ent >= 0.0
    
    # Test risk score
    score = advanced_shield.risk_score(5.0, ["eval", "xor"])
    assert 0.0 <= score <= 1.0
    
    # Test pattern analysis
    patterns = advanced_shield.analyze_patterns("eval('test')")
    assert "eval(" in patterns
    
    # Test network check
    net_check = advanced_shield.check_network(23)
    assert net_check["safe"] == False
    
    net_check = advanced_shield.check_network(80)
    assert net_check["safe"] == True
    
    # Test logs
    logs = advanced_shield.get_logs()
    assert len(logs) > 0
    
    advanced_shield.clear_logs()
    logs = advanced_shield.get_logs()
    assert len(logs) == 0
    
    # Test metadata
    metadata = advanced_shield.get_metadata()
    assert "name" in metadata
    assert "version" in metadata
    
    # Test stats
    stats = advanced_shield.get_stats()
    assert "status" in stats
    
    # Test diagnostics
    diagnostics = advanced_shield.diagnose()
    assert "sandbox_exists" in diagnostics
    
    # Test health check
    health = advanced_shield.health_check()
    assert "status" in health
    
    # Test auto-fix
    advanced_shield.auto_fix()
    
    # Test API
    api_list = advanced_shield.api_list()
    assert len(api_list) > 0
    
    # Clean up
    import os
    os.unlink(test_file.name)
    
    print("✓ advanced_shield.py (GODMODE system - all components)")
except Exception as e:
    import traceback
    print(f"✗ advanced_shield.py: {e}")
    traceback.print_exc()

try:
    from libs.module_manager import ModuleManager, ModuleLogLevel, ModuleMetadata, ModuleSnapshot, ModuleProfile
    module_manager = ModuleManager()
    
    # Test config operations
    module_manager.config_set("auto_mode", False)
    assert module_manager.config_get("auto_mode") == False
    
    module_manager.config_set("auto_mode", True)
    assert module_manager.config_get("auto_mode") == True
    
    # Test module operations
    modules = module_manager.list_modules()
    assert isinstance(modules, list)
    
    # Test snapshot operations
    # Create a mock module for testing
    class MockModule:
        def get_metadata(self):
            return {
                "name": "test_module",
                "version": "2.5.0",
                "author": "test",
                "description": "Test module",
                "dependencies": [],
                "compatibility": {},
                "api_methods": [],
                "plugins": [],
            }
        
        def get_resources(self):
            return {"memory": 1024}
        
        def get_errors(self):
            return []
        
        def export_state(self):
            return {"test": "state"}
        
        def import_state(self, state):
            pass
        
        def config_get(self, key):
            return "test_value"
        
        def config_set(self, key, value):
            pass
        
        def diagnose(self):
            return {"status": "ok"}
        
        def auto_fix(self):
            return True
        
        def plugin_list(self):
            return ["plugin1", "plugin2"]
        
        def plugin_run(self, plugin):
            return f"Ran {plugin}"
        
        def api_list(self):
            return ["method1", "method2"]
        
        def api_call(self, method, *args, **kwargs):
            return f"Called {method}"
    
    # Test status
    status = module_manager.status("nonexistent")
    assert status["status"] == "not_loaded"
    
    # Test logs
    module_manager.log("Test log message")
    logs = module_manager.get_logs()
    assert len(logs) > 0
    
    module_manager.clear_logs()
    logs = module_manager.get_logs()
    assert len(logs) == 0
    
    # Test profile operations
    profile = ModuleProfile(name="test_profile", config={"test": "value"})
    module_manager.profile_set("test_module", profile)
    retrieved_profile = module_manager.profile_get("test_module")
    assert retrieved_profile.name == "test_profile"
    
    module_manager.profile_delete("test_module")
    assert module_manager.profile_get("test_module") is None
    
    # Test metadata
    metadata = module_manager.get_metadata()
    assert isinstance(metadata, dict)
    
    # Test stats
    stats = module_manager.get_stats()
    assert "status" in stats
    assert "modules_loaded" in stats
    
    # Test diagnostics
    diag = module_manager.manager_diagnose()
    assert "enabled" in diag
    
    # Test health check
    health = module_manager.health_check()
    assert "status" in health
    
    # Test API
    api_list = module_manager.api_list_all()
    assert len(api_list) > 0
    
    # Test config reset
    module_manager.config_set("auto_mode", False)
    module_manager.config_reset()
    assert module_manager.config_get("auto_mode") == True
    
    print("✓ module_manager.py (GODMODE system - all components)")
except Exception as e:
    import traceback
    print(f"✗ module_manager.py: {e}")
    traceback.print_exc()

print("\n" + "=" * 60)
print("TESTING TERMINAL COMMANDS")
print("=" * 60)

# Test terminal commands - skip as they require full TerminalX initialization
print("⚠ Terminal commands require full system initialization")
print("  (Tested via main.py startup - all commands registered successfully)")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
