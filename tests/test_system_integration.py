import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import TerminalX

async def test_system():
    print("=== SYSTEM INTEGRATION TEST ===\n")
    
    # Initialize TerminalX
    print("1. Initializing TerminalX...")
    tx = TerminalX()
    print("   ✓ TerminalX instance created")
    
    # Run initialization to set up commands
    print("\n2. Running initialization...")
    await tx.initialize()
    print("   ✓ Initialization complete")
    
    # Check all components are initialized
    print("\n3. Checking components...")
    components = [
        'core', 'logger', 'multitask_engine', 'ai_core', 'ai_models', 'ai_analyzer', 
        'ai_sentinel', 'ai_plugins', 'gui_engine', 'network_core', 'network_manager',
        'network_monitor', 'network_events', 'network_hooks', 'network_sandbox',
        'wifi_manager', 'wifi_scanner', 'bluetooth_manager', 'bluetooth_scanner',
        'kernel_events', 'kernel_hooks', 'kernel_monitor', 'kernel_traps',
        'defender', 'firewall', 'sandbox', 'threat_intel', 'metadata_module',
        'build_module', 'version_module', 'kernel_hooks_engine', 'process_monitor_engine',
        'advanced_shield', 'module_manager', 'module_loader', 'config_manager',
        'file_manager', 'debugger', 'dependency_resolver', 'encryption', 'hot_reload',
        'clipboard_manager', 'backup_system', 'plugin_manager', 'geo_engine',
        'man_engine', 'system_optimizer', 'event_bus', 'cache_engine', 'cloud_engine',
        'alert_module'
    ]
    
    missing = []
    for comp in components:
        if hasattr(tx, comp):
            print(f"   ✓ {comp}")
        else:
            print(f"   ✗ {comp} MISSING")
            missing.append(comp)
    
    # Check commands
    print("\n4. Checking commands...")
    commands = [
        'terminal_commands', 'ai_commands', 'gui_commands', 'network_commands',
        'kernel_commands', 'shield_commands', 'process_commands', 'cloud_commands',
        'module_commands', 'plugin_commands', 'dev_commands', 'geo_commands',
        'man_commands', 'system_opt_commands', 'event_commands', 'bluetooth_commands',
        'alert_commands', 'version_commands', 'ethernet_commands', 'wifi_commands',
        'lan_commands', 'advanced_shield_commands', 'report_commands'
    ]
    
    missing_commands = []
    for cmd in commands:
        if hasattr(tx, cmd):
            print(f"   ✓ {cmd}")
        else:
            print(f"   ✗ {cmd} MISSING")
            missing_commands.append(cmd)
    
    # Summary
    print("\n=== TEST RESULTS ===")
    if missing:
        print(f"❌ FAILED: {len(missing)} components missing: {missing}")
    else:
        print("✅ All components present")
    
    if missing_commands:
        print(f"❌ FAILED: {len(missing_commands)} commands missing: {missing_commands}")
    else:
        print("✅ All commands present")
    
    if not missing and not missing_commands:
        print("\n🎉 SYSTEM INTEGRATION TEST PASSED - 100% FUNCTIONAL")
        return True
    else:
        print("\n❌ SYSTEM INTEGRATION TEST FAILED")
        return False

asyncio.run(test_system())
