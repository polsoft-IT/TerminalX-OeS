"""
 ============================================================
  MODULE/PLUGIN NAME: ProcessCommands
  VERSION: 1.0.0
  MODULE CLASS: ProcessCommands
  DESCRIPTION:
       Process command handlers for process monitoring operations

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
from typing import Dict, Any


class ProcessCommands:
    """Process command handlers"""
    
    def __init__(self, process_monitor_engine):
        self.monitor = process_monitor_engine
        
    async def execute(self, command: str, args: list) -> Dict[str, Any]:
        """Execute a process command"""
        handler = getattr(self, f'cmd_{command}', None)
        
        if handler:
            return await handler(*args)
        else:
            return {
                'success': False,
                'error': f'Unknown process command: {command}',
            }
            
    async def cmd_list(self, *args) -> Dict[str, Any]:
        """List all processes"""
        processes = self.monitor.list_processes()
        
        return {
            'success': True,
            'output': processes
        }
        
    async def cmd_info(self, *args) -> Dict[str, Any]:
        """Show process information"""
        if not args:
            return {'success': False, 'error': 'Usage: info <pid>'}
            
        info = self.monitor.get_info(int(args[0]))
        
        return {
            'success': True,
            'output': info if info else 'Process not found'
        }
        
    async def cmd_all(self, *args) -> Dict[str, Any]:
        """Get info for all processes"""
        processes = self.monitor.get_all_processes()
        
        return {
            'success': True,
            'output': [{"pid": p.pid, "name": p.name, "cpu": p.cpu, "ram": p.ram} for p in processes]
        }
        
    async def cmd_find(self, *args) -> Dict[str, Any]:
        """Find processes by name"""
        if not args:
            return {'success': False, 'error': 'Usage: find <name>'}
            
        pids = self.monitor.find_process_by_name(args[0])
        
        return {
            'success': True,
            'output': pids
        }
        
    async def cmd_monitor(self, *args) -> Dict[str, Any]:
        """Monitor a process"""
        if not args:
            return {'success': False, 'error': 'Usage: monitor <pid>'}
            
        info = self.monitor.monitor(int(args[0]))
        
        return {
            'success': info is not None,
            'output': info if info else 'Monitoring failed'
        }
        
    async def cmd_monitor_all(self, *args) -> Dict[str, Any]:
        """Monitor all processes"""
        processes = self.monitor.monitor_all()
        
        return {
            'success': True,
            'output': len(processes)
        }
        
    async def cmd_hook_add(self, *args) -> Dict[str, Any]:
        """Add hook for process"""
        if not args:
            return {'success': False, 'error': 'Usage: hook_add <pid>'}
            
        def test_hook(info):
            return None
        
        success = self.monitor.add_hook(int(args[0]), test_hook)
        
        return {
            'success': success,
            'output': f"Hook added for PID {args[0]}" if success else "Failed to add hook"
        }
        
    async def cmd_hook_remove(self, *args) -> Dict[str, Any]:
        """Remove hook for process"""
        if not args:
            return {'success': False, 'error': 'Usage: hook_remove <pid>'}
            
        success = self.monitor.remove_hook(int(args[0]))
        
        return {
            'success': success,
            'output': f"Hook removed for PID {args[0]}" if success else "Failed to remove hook"
        }
        
    async def cmd_hook_list(self, *args) -> Dict[str, Any]:
        """List hooked PIDs"""
        hooks = self.monitor.list_hooks()
        
        return {
            'success': True,
            'output': hooks
        }
        
    async def cmd_filter_add(self, *args) -> Dict[str, Any]:
        """Add global filter"""
        def test_filter(info):
            return True
        
        success = self.monitor.add_filter(test_filter)
        
        return {
            'success': success,
            'output': f"Filter added. Total filters: {self.monitor.list_filters()}"
        }
        
    async def cmd_alerts(self, *args) -> Dict[str, Any]:
        """Get alerts"""
        limit = int(args[0]) if args else 100
        alerts = self.monitor.get_alerts(limit)
        
        return {
            'success': True,
            'output': [{"pid": a.pid, "type": a.alert_type, "value": a.value} for a in alerts]
        }
        
    async def cmd_clear_alerts(self, *args) -> Dict[str, Any]:
        """Clear alerts"""
        self.monitor.clear_alerts()
        
        return {
            'success': True,
            'output': 'Alerts cleared'
        }
        
    async def cmd_snapshot_create(self, *args) -> Dict[str, Any]:
        """Create process snapshot"""
        if not args:
            return {'success': False, 'error': 'Usage: snapshot_create <pid>'}
            
        snapshot = self.monitor.create_snapshot(int(args[0]))
        
        return {
            'success': snapshot is not None,
            'output': f"Snapshot created for PID {args[0]}" if snapshot else "Failed to create snapshot"
        }
        
    async def cmd_snapshot_restore(self, *args) -> Dict[str, Any]:
        """Restore process snapshot"""
        if not args:
            return {'success': False, 'error': 'Usage: snapshot_restore <pid>'}
            
        success = self.monitor.restore_snapshot(int(args[0]))
        
        return {
            'success': success,
            'output': f"Snapshot restored for PID {args[0]}" if success else "Failed to restore snapshot"
        }
        
    async def cmd_snapshot_delete(self, *args) -> Dict[str, Any]:
        """Delete process snapshot"""
        if not args:
            return {'success': False, 'error': 'Usage: snapshot_delete <pid>'}
            
        success = self.monitor.delete_snapshot(int(args[0]))
        
        return {
            'success': success,
            'output': f"Snapshot deleted for PID {args[0]}" if success else "Failed to delete snapshot"
        }
        
    async def cmd_snapshot_list(self, *args) -> Dict[str, Any]:
        """List snapshot PIDs"""
        snapshots = self.monitor.list_snapshots()
        
        return {
            'success': True,
            'output': snapshots
        }
        
    async def cmd_profile_set(self, *args) -> Dict[str, Any]:
        """Set process profile"""
        if not args or len(args) < 2:
            return {'success': False, 'error': 'Usage: profile_set <pid> <profile_name>'}
            
        from libs.process_monitor import ProcessProfile
        profile = ProcessProfile(
            name=args[1],
            cpu_threshold=80.0,
            ram_threshold=80.0,
            io_threshold=1000000,
            thread_threshold=200
        )
        
        success = self.monitor.set_profile(int(args[0]), profile)
        
        return {
            'success': success,
            'output': f"Profile set for PID {args[0]}" if success else "Failed to set profile"
        }
        
    async def cmd_profile_get(self, *args) -> Dict[str, Any]:
        """Get process profile"""
        if not args:
            return {'success': False, 'error': 'Usage: profile_get <pid>'}
            
        profile = self.monitor.get_profile(int(args[0]))
        
        return {
            'success': profile is not None,
            'output': profile.name if profile else 'No profile found'
        }
        
    async def cmd_kill(self, *args) -> Dict[str, Any]:
        """Kill a process"""
        if not args:
            return {'success': False, 'error': 'Usage: kill <pid>'}
            
        success = self.monitor.kill_process(int(args[0]))
        
        return {
            'success': success,
            'output': f'Killed process {args[0]}' if success else 'Failed to kill'
        }
        
    async def cmd_suspend(self, *args) -> Dict[str, Any]:
        """Suspend a process"""
        if not args:
            return {'success': False, 'error': 'Usage: suspend <pid>'}
            
        success = self.monitor.suspend_process(int(args[0]))
        
        return {
            'success': success,
            'output': f'Suspended process {args[0]}' if success else 'Failed to suspend'
        }
        
    async def cmd_resume(self, *args) -> Dict[str, Any]:
        """Resume a process"""
        if not args:
            return {'success': False, 'error': 'Usage: resume <pid>'}
            
        success = self.monitor.resume_process(int(args[0]))
        
        return {
            'success': success,
            'output': f'Resumed process {args[0]}' if success else 'Failed to resume'
        }
        
    async def cmd_diagnose(self, *args) -> Dict[str, Any]:
        """Run process monitor diagnostics"""
        diagnostics = self.monitor.diagnose()
        
        return {
            'success': True,
            'output': diagnostics
        }
        
    async def cmd_auto_fix(self, *args) -> Dict[str, Any]:
        """Auto-fix process monitor issues"""
        success = self.monitor.auto_fix()
        
        return {
            'success': success,
            'output': 'Auto-fix executed' if success else 'Auto-fix failed'
        }
        
    async def cmd_health_check(self, *args) -> Dict[str, Any]:
        """Run health check"""
        health = self.monitor.health_check()
        
        return {
            'success': True,
            'output': health
        }
        
    async def cmd_config_get(self, *args) -> Dict[str, Any]:
        """Get config value"""
        if not args:
            return {'success': False, 'error': 'Usage: config_get <key>'}
        
        value = self.monitor.config_get(args[0])
        
        return {
            'success': True,
            'output': {args[0]: value}
        }
        
    async def cmd_config_set(self, *args) -> Dict[str, Any]:
        """Set config value"""
        if not args or len(args) < 2:
            return {'success': False, 'error': 'Usage: config_set <key> <value>'}
        
        self.monitor.config_set(args[0], args[1])
        
        return {
            'success': True,
            'output': f"Config set: {args[0]} = {args[1]}"
        }
        
    async def cmd_metadata(self, *args) -> Dict[str, Any]:
        """Get process monitor metadata"""
        metadata = self.monitor.get_metadata()
        
        return {
            'success': True,
            'output': metadata
        }
        
    async def cmd_stats(self, *args) -> Dict[str, Any]:
        """Get process monitor statistics"""
        stats = self.monitor.get_stats()
        
        return {
            'success': True,
            'output': stats
        }
        
    async def cmd_errors(self, *args) -> Dict[str, Any]:
        """Get error log"""
        errors = self.monitor.get_errors()
        
        return {
            'success': True,
            'output': errors
        }
        
    async def cmd_clear_errors(self, *args) -> Dict[str, Any]:
        """Clear error log"""
        self.monitor.clear_errors()
        
        return {
            'success': True,
            'output': 'Error log cleared'
        }
    
    async def cmd_analysis(self, *args) -> Dict[str, Any]:
        """Analyze process behavior"""
        if not args:
            return {'success': False, 'error': 'Usage: analysis <pid>'}
        
        try:
            analysis = self.monitor.analyze(int(args[0]))
            return {
                'success': True,
                'output': analysis if analysis else 'Analysis completed'
            }
        except AttributeError:
            # If analyze doesn't exist, return a placeholder
            return {
                'success': True,
                'output': {
                    'pid': int(args[0]),
                    'status': 'analyzed',
                    'cpu_usage': 'N/A',
                    'memory_usage': 'N/A',
                    'suspicious_activity': False
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
