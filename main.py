"""
 ============================================================
  MODULE/PLUGIN NAME: TerminalX
  VERSION: 1.3.0
  UPDATED: 2026-08-15
  MODULE CLASS: TerminalX
  DESCRIPTION:
       Main entry point of TerminalX system integrating all modules.
       Fully integrated with all libs/ libraries (ModuleLoader, ConfigManager, 
       FileManager, AdvancedDebugger, DependencyResolver, Encryption, 
       HotReloadManager, ClipboardManager, BackupSystem), ReportEngine,
       AdvancedShieldCommands, ReportCommands and AliasEngine (GODMODE v5).
       All components properly initialized and configured with notification
       callbacks and subsystems.

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

import asyncio
import sys
from pathlib import Path
from core import CoreEngine, Logger, MultiTaskEngine, TaskPriority, Framebuffer, GUIManager, emoji_library, unicode_library, figlet_engine, ansi_colors_engine, animations_engine, gui_widgets_library, EventBus, AlertModule, AlertLevel, AlertChannel, AliasEngine
from ai import AICore, AIModels, AIAnalyzer, AISentinel, AIPlugins
from gui import GUIEngine, GUIFrameworks, GUIWidgets, GUIWindows, GUIApps
from network import NetworkCore, NetworkManager, NetworkMonitor, NetworkEvents, NetworkHooks, NetworkSandbox
from network.wifi import WiFiManager, WiFiScanner
from network.bluetooth import BluetoothManager, BluetoothScanner
from kernel import KernelEvents, KernelHooks, KernelMonitor, Traps
from shield import Defender, Firewall, Sandbox, ThreatIntel
from metadata import MetadataModule
from build import BuildModule
from geo import GeoEngine, IPInfoProvider, GeoPyProvider, FreeGeoIPProvider, IPAPICOProvider, LoggerPlugin, CachePlugin, StatsPlugin
from man import ManEngine
from system_optimizer import SystemOptimizer, SystemOptConfig, LoggerPlugin as SysOptLoggerPlugin, StatsPlugin as SysOptStatsPlugin
from modules.version import VersionModule
from report.report_engine import ReportEngine
from libs.kernel_hooks import KernelHooksEngine
from libs.process_monitor import ProcessMonitor
from libs.advanced_shield import AdvancedShield
from libs.module_manager import ModuleManager
from libs.module_loader import ModuleLoader
from libs.config_manager import ConfigManager
from libs.file_manager import FileManager
from libs.debugger import AdvancedDebugger
from libs.dependency_resolver import DependencyResolver
from libs.encryption import Encryption
from libs.hot_reload import HotReloadManager
from libs.clipboard_manager import ClipboardManager
from libs.backup_system import BackupSystem
from plugin.core.plugin_manager import PluginManager
from commands import (
    TerminalCommands, AICommands, GUICommands, NetworkCommands,
    KernelCommands, ShieldCommands, ProcessCommands, CloudCommands,
    AdvancedShieldCommands, ModuleCommands,
    PluginCommands, GeoCommands, SystemOptCommands, ManCommands, EventCommands, BluetoothCommands,
    VersionCommands, AlertCommands, CDCommands, DevCommands, AliasCommands
)
from core import CacheEngine, CloudEngine


class TerminalX:
    """Main TerminalX application"""
    
    def __init__(self):
        self.core = CoreEngine()
        self.logger = Logger()
        
        # Multi-Task Engine
        self.multitask_engine = MultiTaskEngine(max_workers=8, time_slice=0.002)
        
        # GUI Enhancements
        self.framebuffer = None
        self.gui_manager = None
        
        # AI Module
        self.ai_core = AICore()
        self.ai_models = AIModels()
        self.ai_analyzer = AIAnalyzer()
        self.ai_sentinel = AISentinel()
        self.ai_plugins = AIPlugins()
        
        # GUI Module
        self.gui_engine = GUIEngine()
        self.gui_frameworks = GUIFrameworks()
        self.gui_widgets = GUIWidgets()
        self.gui_windows = GUIWindows()
        self.gui_apps = GUIApps()
        
        # Network Module
        self.network_core = NetworkCore()
        self.network_manager = NetworkManager()
        self.network_monitor = NetworkMonitor()
        self.network_events = NetworkEvents()
        self.network_hooks = NetworkHooks()
        self.network_sandbox = NetworkSandbox()
        self.wifi_manager = WiFiManager()
        self.wifi_scanner = WiFiScanner()
        self.bluetooth_manager = BluetoothManager()
        self.bluetooth_scanner = BluetoothScanner()
        
        # Kernel Module
        self.kernel_events = KernelEvents()
        self.kernel_hooks = KernelHooks()
        self.kernel_monitor = KernelMonitor()
        self.kernel_traps = Traps()
        
        # Shield Module
        self.defender = Defender()
        self.firewall = Firewall()
        self.sandbox = Sandbox()
        self.threat_intel = ThreatIntel()
        
        # Metadata Module
        self.metadata_module = MetadataModule()
        
        # Build Module
        self.build_module = BuildModule()
        
        # Version Module
        self.version_module = VersionModule()
        
        # Report Engine (GODMODE)
        self.report_engine = ReportEngine()
        
        # Kernel Hooks Engine (GODMODE)
        self.kernel_hooks_engine = KernelHooksEngine()
        
        # Process Monitor Engine (GODMODE)
        self.process_monitor_engine = ProcessMonitor()
        
        # Advanced Shield (GODMODE)
        self.advanced_shield = AdvancedShield()
        
        # Module Manager (GODMODE)
        self.module_manager = ModuleManager()
        
        # Module Loader (GODMODE)
        self.module_loader = ModuleLoader()
        
        # Config Manager (GODMODE)
        self.config_manager = None
        
        # File Manager (GODMODE)
        self.file_manager = FileManager()
        
        # Debugger (GODMODE)
        self.debugger = AdvancedDebugger()
        
        # Dependency Resolver (GODMODE)
        self.dependency_resolver = DependencyResolver()
        
        # Encryption (GODMODE)
        self.encryption = Encryption()
        
        # Hot Reload (GODMODE)
        self.hot_reload = HotReloadManager()
        
        # Clipboard Manager (GODMODE)
        self.clipboard_manager = ClipboardManager()
        
        # Backup System (GODMODE)
        self.backup_system = BackupSystem()
        
        # Alias Engine (GODMODE v5)
        self.alias_engine = AliasEngine()
        
        # Plugin Manager (GODMODE)
        self.plugin_manager = PluginManager()
        
        # Geo Engine (GODMODE)
        self.geo_engine = GeoEngine()
        
        # Man Engine (Documentation)
        self.man_engine = ManEngine()
        
        # System Optimizer (GODMODE)
        self.system_optimizer = SystemOptimizer()
        
        # Event Bus (GODMODE)
        self.event_bus = EventBus()
        
        # Cache and Cloud
        self.cache_engine = CacheEngine()
        self.cloud_engine = CloudEngine()
        
        # Alert Module
        self.alert_module = AlertModule()
        
        # Commands
        self.terminal_commands = None
        self.ai_commands = None
        self.gui_commands = None
        self.network_commands = None
        self.kernel_commands = None
        self.shield_commands = None
        self.process_commands = None
        self.cloud_commands = None
        self.plugin_commands = None
        self.dev_commands = None
        self.geo_commands = None
        self.man_commands = None
        self.system_opt_commands = None
        self.event_commands = None
        self.cd_commands = None
        self.bluetooth_commands = None
        self.alert_commands = None
        self.version_commands = None
        self.ethernet_commands = None
        self.wifi_commands = None
        self.lan_commands = None
        self.advanced_shield_commands = None
        self.report_commands = None
        
    async def initialize(self):
        """Initialize all modules"""
        self.logger.info("Initializing TerminalX...")
        
        # Initialize core
        await self.core.initialize()
        
        # Initialize Multi-Task Engine
        multitask_config = self.core.config.get('multitask') or {}
        max_workers = multitask_config.get('max_workers', 8)
        time_slice = multitask_config.get('time_slice', 0.002)
        self.multitask_engine = MultiTaskEngine(max_workers=max_workers, time_slice=time_slice)
        
        # Connect notification callback to Multi-Task Engine
        self.multitask_engine.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        
        # Create IPC channels
        self.multitask_engine.bus.create_channel("gui")
        self.multitask_engine.bus.create_channel("syslog")
        self.multitask_engine.bus.create_channel("tasks")
        
        # Initialize GUI Enhancements (optional, disabled by default for terminal mode)
        gui_config = self.core.config.get('gui_enhancements') or {}
        self.gui_enabled = gui_config.get('enabled', False)
        
        if self.gui_enabled:
            fb_width = gui_config.get('framebuffer_width', 120)
            fb_height = gui_config.get('framebuffer_height', 40)
            self.framebuffer = Framebuffer(fb_width, fb_height)
            self.gui_manager = GUIManager(self.framebuffer, self.multitask_engine, self.multitask_engine.bus)
            
            # Connect notification callback to GUI Manager
            self.gui_manager.set_notification_callback(
                lambda title, message, ntype, priority: 
                self.core.notification_system.create(title, message, ntype, priority)
            )
        else:
            self.framebuffer = None
            self.gui_manager = None
        
        # Initialize AI module
        ai_config = self.core.config.get('ai') or {}
        await self.ai_core.initialize(ai_config)
        await self.ai_analyzer.initialize(ai_config)
        await self.ai_sentinel.initialize(ai_config)
        await self.ai_plugins.initialize()
        
        # Connect notification callbacks to AI modules
        self.ai_core.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        self.ai_analyzer.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        self.ai_plugins.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        
        # Initialize GUI module
        gui_config = self.core.config.get('gui') or {}
        await self.gui_engine.initialize(gui_config)
        
        # Initialize network module
        network_config = self.core.config.get('network') or {}
        await self.network_core.initialize(network_config)
        await self.network_manager.initialize(network_config)
        await self.network_monitor.initialize(network_config)
        await self.network_sandbox.initialize(network_config)
        await self.wifi_manager.initialize(network_config)
        await self.bluetooth_manager.initialize(network_config)
        
        # Initialize kernel module
        kernel_config = self.core.config.get('kernel') or {}
        await self.kernel_monitor.initialize(kernel_config)
        await self.kernel_events.initialize(kernel_config)
        await self.kernel_hooks.initialize(kernel_config)
        await self.kernel_traps.initialize(kernel_config)
        
        # Connect notification callbacks to kernel modules
        self.kernel_monitor.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        self.kernel_events.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        self.kernel_hooks.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        self.kernel_traps.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        
        # Initialize shield module
        shield_config = self.core.config.get('shield') or {}
        await self.defender.initialize(shield_config)
        await self.firewall.initialize(shield_config)
        await self.sandbox.initialize(shield_config)
        await self.threat_intel.initialize(shield_config)
        
        # Connect notification callbacks to shield modules
        self.defender.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        self.firewall.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        self.sandbox.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        self.threat_intel.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        
        # Initialize cache and cloud
        cache_config = self.core.config.get('cache') or {}
        await self.cache_engine.initialize()
        
        cloud_config = self.core.config.get('cloud') or {}
        await self.cloud_engine.initialize(cloud_config)
        
        # Initialize metadata module
        metadata_config = self.core.config.get('metadata') or {}
        await self.metadata_module.initialize(metadata_config)
        
        # Connect notification callback to metadata module
        self.metadata_module.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        
        # Initialize Alert Module
        alert_config = self.core.config.get('alert') or {}
        await self.alert_module.initialize(alert_config)
        self.alert_module.set_notification_system(self.core.notification_system)
        
        # Connect notification callback to alert module
        self.alert_module.set_notification_system(self.core.notification_system)
        
        # Initialize build module
        build_config = self.core.config.get('build') or {}
        await self.build_module.initialize(build_config)
        
        # Set logger for build module
        self.build_module.set_logger(self.logger)
        
        # Connect notification callback to build module
        self.build_module.set_notification_callback(
            lambda title, message, ntype, priority: 
            self.core.notification_system.create(title, message, ntype, priority)
        )
        
        # Initialize Kernel Hooks Engine (GODMODE)
        kernel_hooks_config = self.core.config.get('kernel_hooks') or {}
        self.kernel_hooks_engine.config_set("mode", kernel_hooks_config.get("mode", "monitor"))
        self.kernel_hooks_engine.config_set("log_level", kernel_hooks_config.get("log_level", "normal"))
        self.kernel_hooks_engine.config_set("trap_policy", kernel_hooks_config.get("trap_policy", "strict"))
        
        # Initialize Process Monitor Engine (GODMODE)
        process_monitor_config = self.core.config.get('process_monitor') or {}
        self.process_monitor_engine.config_set("interval", process_monitor_config.get("interval", 1.0))
        self.process_monitor_engine.config_set("auto_alert", process_monitor_config.get("auto_alert", True))
        self.process_monitor_engine.config_set("cpu_threshold", process_monitor_config.get("cpu_threshold", 80.0))
        self.process_monitor_engine.config_set("ram_threshold", process_monitor_config.get("ram_threshold", 80.0))
        self.process_monitor_engine.config_set("io_threshold", process_monitor_config.get("io_threshold", 1000000))
        self.process_monitor_engine.config_set("thread_threshold", process_monitor_config.get("thread_threshold", 200))
        
        # Initialize Advanced Shield (GODMODE)
        shield_config = self.core.config.get('advanced_shield') or {}
        self.advanced_shield.config_set("auto_rules", shield_config.get("auto_rules", True))
        self.advanced_shield.config_set("auto_response", shield_config.get("auto_response", True))
        self.advanced_shield.config_set("auto_learning", shield_config.get("auto_learning", True))
        self.advanced_shield.config_set("realtime_interval", shield_config.get("realtime_interval", 1.0))
        
        # Initialize Module Manager (GODMODE)
        modman_config = self.core.config.get('module_manager') or {}
        self.module_manager.config_set("auto_mode", modman_config.get("auto_mode", True))
        
        # Initialize Module Loader (GODMODE)
        loader_config = self.core.config.get('module_loader') or {}
        self.module_loader.add_load_path(str(Path(__file__).parent / "modules"))
        self.module_loader.add_load_path(str(Path(__file__).parent / "libs"))
        
        # Initialize Config Manager (GODMODE)
        config_dir = Path.home() / ".terminalx"
        self.config_manager = ConfigManager(config_dir)
        
        # Initialize File Manager (GODMODE)
        fileman_config = self.core.config.get('file_manager') or {}
        self.file_manager.logger = self.logger
        
        # Initialize Debugger (GODMODE)
        debugger_config = self.core.config.get('debugger') or {}
        self.debugger.logger = self.logger
        
        # Initialize Dependency Resolver (GODMODE)
        dep_config = self.core.config.get('dependency_resolver') or {}
        self.dependency_resolver.logger = self.logger
        
        # Initialize Encryption (GODMODE)
        enc_config = self.core.config.get('encryption') or {}
        if enc_config.get('auto_key', True):
            key = self.encryption.generate_key()
            self.encryption.set_key(key)
        
        # Initialize Hot Reload (GODMODE)
        reload_config = self.core.config.get('hot_reload') or {}
        self.hot_reload.auto_reload_enabled = reload_config.get('auto_reload', False)
        self.hot_reload.check_interval = reload_config.get('check_interval', 1.0)
        
        # Initialize Clipboard Manager (GODMODE)
        clip_config = self.core.config.get('clipboard_manager') or {}
        self.clipboard_manager.logger = self.logger
        
        # Initialize Backup System (GODMODE)
        backup_config = self.core.config.get('backup_system') or {}
        self.backup_system.logger = self.logger
        self.module_manager.config_set("auto_reload", modman_config.get("auto_reload", False))
        self.module_manager.config_set("auto_fix", modman_config.get("auto_fix", True))
        self.module_manager.config_set("check_interval", modman_config.get("check_interval", 5.0))
        
        # Initialize Plugin Manager (GODMODE)
        self.plugin_manager.initialize()
        plugin_config = self.core.config.get('plugin_manager') or {}
        self.plugin_manager.config_set("auto_load", plugin_config.get("auto_load", True))
        self.plugin_manager.config_set("auto_verify", plugin_config.get("auto_verify", True))
        self.plugin_manager.config_set("sandbox_enabled", plugin_config.get("sandbox_enabled", True))
        self.plugin_manager.config_set("strict_permissions", plugin_config.get("strict_permissions", True))
        
        # Set up version callbacks for module and plugin count changes
        self.module_manager.set_version_callback(lambda count: self.version_module.set_module_count(count))
        self.plugin_manager.set_version_callback(lambda count: self.version_module.set_plugin_count(count))
        
        # Initialize version module with current counts
        await self.version_module.initialize()
        self.version_module.set_logger(self.logger)
        module_count = len(self.module_manager.list_modules())
        plugin_count = len(self.plugin_manager.list_plugins())
        self.version_module.update_counts(module_count, plugin_count)
        
        # Register subsystems
        await self.core.register_subsystem('multitask_engine', self.multitask_engine)
        await self.core.register_subsystem('emoji_library', emoji_library)
        await self.core.register_subsystem('unicode_library', unicode_library)
        await self.core.register_subsystem('figlet_engine', figlet_engine)
        await self.core.register_subsystem('ansi_colors_engine', ansi_colors_engine)
        await self.core.register_subsystem('animations_engine', animations_engine)
        await self.core.register_subsystem('gui_widgets_library', gui_widgets_library)
        if self.gui_manager:
            await self.core.register_subsystem('gui_manager', self.gui_manager)
        await self.core.register_subsystem('ai_core', self.ai_core)
        await self.core.register_subsystem('ai_analyzer', self.ai_analyzer)
        await self.core.register_subsystem('ai_sentinel', self.ai_sentinel)
        await self.core.register_subsystem('ai_plugins', self.ai_plugins)
        await self.core.register_subsystem('gui_engine', self.gui_engine)
        await self.core.register_subsystem('network_core', self.network_core)
        await self.core.register_subsystem('kernel_monitor', self.kernel_monitor)
        await self.core.register_subsystem('kernel_events', self.kernel_events)
        await self.core.register_subsystem('kernel_hooks', self.kernel_hooks)
        await self.core.register_subsystem('kernel_traps', self.kernel_traps)
        await self.core.register_subsystem('defender', self.defender)
        await self.core.register_subsystem('firewall', self.firewall)
        await self.core.register_subsystem('sandbox', self.sandbox)
        await self.core.register_subsystem('threat_intel', self.threat_intel)
        await self.core.register_subsystem('metadata_module', self.metadata_module)
        await self.core.register_subsystem('build_module', self.build_module)
        await self.core.register_subsystem('version_module', self.version_module)
        await self.core.register_subsystem('report_engine', self.report_engine)
        await self.core.register_subsystem('kernel_hooks_engine', self.kernel_hooks_engine)
        await self.core.register_subsystem('process_monitor_engine', self.process_monitor_engine)
        await self.core.register_subsystem('advanced_shield', self.advanced_shield)
        await self.core.register_subsystem('module_manager', self.module_manager)
        await self.core.register_subsystem('module_loader', self.module_loader)
        await self.core.register_subsystem('config_manager', self.config_manager)
        await self.core.register_subsystem('file_manager', self.file_manager)
        await self.core.register_subsystem('debugger', self.debugger)
        await self.core.register_subsystem('dependency_resolver', self.dependency_resolver)
        await self.core.register_subsystem('encryption', self.encryption)
        await self.core.register_subsystem('hot_reload', self.hot_reload)
        await self.core.register_subsystem('clipboard_manager', self.clipboard_manager)
        await self.core.register_subsystem('backup_system', self.backup_system)
        await self.core.register_subsystem('alias_engine', self.alias_engine)
        await self.core.register_subsystem('plugin_manager', self.plugin_manager)
        await self.core.register_subsystem('geo_engine', self.geo_engine)
        await self.core.register_subsystem('man_engine', self.man_engine)
        await self.core.register_subsystem('cache_engine', self.cache_engine)
        await self.core.register_subsystem('cloud_engine', self.cloud_engine)
        await self.core.register_subsystem('notification_system', self.core.notification_system)
        await self.core.register_subsystem('alert_module', self.alert_module)
        
        # Initialize commands
        self.terminal_commands = TerminalCommands(self.core, self)
        self.ai_commands = AICommands(self.ai_core)
        self.gui_commands = GUICommands(self.gui_engine)
        self.network_commands = NetworkCommands(self.network_core, self.network_manager)
        self.kernel_commands = KernelCommands(self.kernel_monitor, self.kernel_hooks_engine)
        self.shield_commands = ShieldCommands(self.defender, self.firewall, self.threat_intel, self.advanced_shield)
        self.process_commands = ProcessCommands(self.process_monitor_engine)
        self.cloud_commands = CloudCommands(self.cloud_engine)
        self.module_commands = ModuleCommands(self.core)
        self.plugin_commands = PluginCommands(self.plugin_manager, self.ai_plugins)
        self.dev_commands = DevCommands(self.core, self.build_module, self.ai_core)
        self.geo_commands = GeoCommands(self.geo_engine)
        self.man_commands = ManCommands(self.man_engine)
        self.system_opt_commands = SystemOptCommands(self.system_optimizer)
        self.cd_commands = CDCommands(self)
        self.event_commands = EventCommands(self.event_bus)
        self.bluetooth_commands = BluetoothCommands(self.bluetooth_manager, self.bluetooth_scanner)
        self.alert_commands = AlertCommands(self.alert_module)
        
        # Initialize alias commands (GODMODE v5)
        self.alias_commands = AliasCommands(self.alias_engine)

        # Initialize version and ethernet commands
        import importlib
        import os
        spec = importlib.util.spec_from_file_location("version_commands", os.path.join(os.path.dirname(__file__), "commands", "version.py"))
        version_commands_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(version_commands_module)
        self.version_commands = version_commands_module.VersionCommands(self.version_module)

        from commands.ethernet import EthernetCommands
        self.ethernet_commands = EthernetCommands(self.network_core, self.network_manager)
        
        # Initialize wifi and lan commands
        from commands.wifi import WiFiCommands
        from commands.lan import LANCommands
        self.wifi_commands = WiFiCommands(self.network_core, self.network_manager)
        self.lan_commands = LANCommands(self.network_core, self.network_manager)
        
        # Initialize advanced_shield and report commands
        from commands.advanced_shield import AdvancedShieldCommands
        from commands.report import ReportCommands
        self.advanced_shield_commands = AdvancedShieldCommands(self.advanced_shield)
        self.report_commands = ReportCommands(self.report_engine)
        
        # Initialize Event Bus
        await self.event_bus.initialize()
        
        # Initialize ManEngine with pages directory
        man_pages_dir = os.path.join(os.path.dirname(__file__), 'man', 'pages')
        await self.man_engine.initialize({'pages_directory': man_pages_dir})
        
        # Initialize GeoEngine with providers and plugins
        self.geo_engine.register_provider(FreeGeoIPProvider())
        self.geo_engine.register_provider(IPAPICOProvider())
        try:
            self.geo_engine.register_provider(GeoPyProvider())
        except Exception:
            pass  # GeoPy not available
        self.geo_engine.register_plugin(LoggerPlugin(verbose=False))
        self.geo_engine.register_plugin(CachePlugin(ttl_seconds=3600))
        self.geo_engine.register_plugin(StatsPlugin())
        self.geo_engine.configure(
            default_provider='freegeoip',
            timeout=10,
            max_retries=3,
            enable_fallback=True
        )
        
        self.logger.info("TerminalX initialized successfully")
    
    async def start(self):
        """Start all modules"""
        self.logger.info("Starting TerminalX...")
        
        await self.core.start()
        
        # Start Multi-Task Engine
        self.multitask_engine.start()
        
        # Start GUI Manager (only if enabled)
        if self.gui_manager:
            self.gui_manager.start()
        
        # Start monitors
        await self.kernel_monitor.start()
        await self.network_monitor.start()
        
        self.logger.info("TerminalX started")
    
    async def stop(self):
        """Stop all modules"""
        self.logger.info("Stopping TerminalX...")
        
        # Stop GUI Manager (only if enabled)
        if self.gui_manager:
            self.gui_manager.stop()
        
        # Stop Multi-Task Engine
        self.multitask_engine.stop()
        
        await self.core.stop()
        
        # Shutdown cloud engine
        await self.cloud_engine.shutdown()
        
        self.logger.info("TerminalX stopped")
    
    async def execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a command"""
        parts = command.strip().split()
        if not parts:
            return {'success': False, 'error': 'Empty command'}
        
        # Handle "?" as alias for help
        if parts[0] == '?':
            parts[0] = 'help'
        
        # Check for module prefix (e.g., "ai process", "net list")
        if len(parts) >= 2 and parts[0] in ['ai', 'gui', 'net', 'kernel', 'shield', 'proc', 'cloud', 'module', 'plugins', 'plugin', 'geo', 'man', 'sysopt', 'event', 'bluetooth', 'display', 'dev', 'developer', 'system', 'auth', 'archive', 'python', 'engine', 'fs', 'emoji', 'unicode', 'figlet', 'ansi', 'anim', 'widgets', 'metadata', 'build', 'task', 'alert', 'plug', 'mod', 'dbg', 'krl', 'py', 'nets', 'sbx', 'enet', 'ver', 'bt', 'meta', 'diag', 'eve', 'cfg', 'lib', 'network', 'version', 'ethernet', 'debug', 'sandbox', 'diagnostic', 'config', 'library', 'wifi', 'lan', 'advanced_shield', 'report', 'alias']:
            module = parts[0]
            cmd = parts[1]
            args = parts[2:]
            
            command_map = {
                'ai': self.ai_commands,
                'gui': self.gui_commands,
                'net': self.network_commands,
                'kernel': self.kernel_commands,
                'krl': self.kernel_commands,
                'shield': self.shield_commands,
                'proc': self.process_commands,
                'cloud': self.cloud_commands,
                'module': self.module_commands,
                'mod': self.module_commands,
                'plugin': self.plugin_commands,
                'plugins': self.plugin_commands,
                'plug': self.plugin_commands,
                'geo': self.geo_commands,
                'man': self.man_commands,
                'sysopt': self.system_opt_commands,
                'event': self.event_commands,
                'eve': self.event_commands,
                'bluetooth': self.bluetooth_commands,
                'bt': self.bluetooth_commands,
                'alert': self.alert_commands,
                'cd': self.cd_commands,
                'dev': self.dev_commands,
                'developer': self.dev_commands,
                'python': self.terminal_commands,
                'py': self.terminal_commands,
                'network': self.network_commands,
                'nets': self.network_commands,
                'metadata': self.terminal_commands,
                'meta': self.terminal_commands,
                'version': self.version_commands,
                'ver': self.version_commands,
                'ethernet': self.ethernet_commands,
                'enet': self.ethernet_commands,
                'debug': self.terminal_commands,
                'dbg': self.terminal_commands,
                'sandbox': self.terminal_commands,
                'sbx': self.terminal_commands,
                'diagnostic': self.terminal_commands,
                'diag': self.terminal_commands,
                'config': self.terminal_commands,
                'cfg': self.terminal_commands,
                'library': self.terminal_commands,
                'lib': self.terminal_commands,
                'wifi': self.wifi_commands,
                'lan': self.lan_commands,
                'advanced_shield': self.advanced_shield_commands,
                'report': self.report_commands,
                'alias': self.alias_commands,
            }
            
            if module in command_map:
                return await command_map[module].execute(cmd, args)
            else:
                # Handle system-level prefixes (display, dev, sys, auth, archive, python, engine)
                # These are handled by terminal_commands with the prefix as part of the command name
                combined_cmd = f"{module}_{cmd}"
                return await self.terminal_commands.execute(combined_cmd, args)
        else:
            # Terminal command
            cmd = parts[0]
            args = parts[1:]
            return await self.terminal_commands.execute(cmd, args)
            
        return {'success': False, 'error': 'Unknown command'}
        
    async def run_interactive(self):
        """Run interactive terminal"""
        from core import ANSI
        
        config = self.core.config.get('terminal') or {}
        prompt = config.get('prompt', 'TerminalX> ')
        welcome = config.get('welcome_message', '2026 (c) polsoft.ITS (TM)  |  TerminalOS v2.5.0  |  Cross-platform  |  Sebastian Januchowski')
        
        try:
            print(f"{ANSI.blue_gradient_banner(welcome)}")
        except UnicodeEncodeError:
            print(f"{ANSI.CYAN}{welcome}{ANSI.RESET}")
        print(f"{ANSI.DIM}Type 'help' or '?' for available commands{ANSI.RESET}\n")
        
        while self.core.running:
            try:
                command = input(f"{ANSI.GREEN}{prompt}{ANSI.RESET}")
                
                if command.strip():
                    result = await self.execute_command(command)
                    
                    if result.get('success'):
                        output = result.get('output')
                        if output:
                            if isinstance(output, str):
                                print(output)
                            else:
                                import json
                                print(json.dumps(output, indent=2))
                    else:
                        print(f"{ANSI.RED}Error: {result.get('error')}{ANSI.RESET}")
                        
            except KeyboardInterrupt:
                print(f"\n{ANSI.YELLOW}Interrupted. Type 'exit' to quit.{ANSI.RESET}")
            except EOFError:
                break
                
    async def run(self):
        """Main run loop"""
        try:
            await self.initialize()
            await self.start()
            await self.run_interactive()
        finally:
            await self.stop()


async def main():
    """Main entry point"""
    terminal = TerminalX()
    await terminal.run()


if __name__ == '__main__':
    asyncio.run(main())
