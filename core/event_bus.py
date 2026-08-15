"""
 ============================================================
  EVENT BUS ENGINE — GLOBAL EVENT SYSTEM
  Terminal Hybrid Architecture (GODMODE / ULTRA / PRO)
  AUTHOR:  Sebastian Januchowski
  COMPANY: polsoft.ITS™ Dev
  VERSION: 2.0.0
 ============================================================
"""

import asyncio
import time
import traceback
from datetime import datetime
from typing import Dict, Callable, List, Any, Optional
from collections import defaultdict
from core.ansi import ANSI


class EventBus:
    """Advanced event bus for inter-module communication with GODMODE features"""
    
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = defaultdict(list)
        self.event_queue: asyncio.Queue = asyncio.Queue()
        self.running = False
        
        # Advanced features
        self.logs: List[str] = []
        self.errors: List[str] = []
        self.filters: List[Callable] = []
        self.hooks: Dict[str, Callable] = {}
        self.snapshots: Dict[str, Any] = {}
        self.config = {
            "mode": "async",          # sync / async
            "log_level": "normal",    # normal / verbose / silent
            "max_queue": 10000,
            "auto_flush": True,
        }
        
    # ============================================================
    # LOGGING
    # ============================================================
    def _get_event_type(self, msg: str) -> str:
        """Detect event type from message"""
        msg_lower = msg.lower()
        if any(keyword in msg_lower for keyword in ['error', 'fail', 'critical', 'exception', 'crash']):
            return 'error'
        elif any(keyword in msg_lower for keyword in ['success', 'complete', 'done', 'ok', 'ready', 'initialized', 'started']):
            return 'success'
        elif any(keyword in msg_lower for keyword in ['warning', 'warn', 'caution', 'alert', 'deprecated']):
            return 'warning'
        else:
            return 'info'
    
    def _format_event(self, msg: str, event_type: str) -> str:
        """Format event with color coding, gradients, and special effects"""
        timestamp = f"[{datetime.now().strftime('%H:%M:%S')}]"
        
        if event_type == 'error':
            # Fire effect with red gradient and blink
            colored_msg = ANSI.fire(msg)
            return f"{ANSI.BOLD}{ANSI.RED}{timestamp}{ANSI.RESET} {ANSI.BOLD}{ANSI.BLINK}{colored_msg}{ANSI.RESET}"
        elif event_type == 'success':
            # Matrix effect with green gradient
            colored_msg = ANSI.matrix(msg)
            return f"{ANSI.BOLD}{ANSI.GREEN}{timestamp}{ANSI.RESET} {ANSI.BOLD}{colored_msg}{ANSI.RESET}"
        elif event_type == 'warning':
            # Sunset effect with yellow/orange gradient
            colored_msg = ANSI.sunset(msg)
            return f"{ANSI.BOLD}{ANSI.YELLOW}{timestamp}{ANSI.RESET} {ANSI.BOLD}{colored_msg}{ANSI.RESET}"
        else:
            # Ocean effect with blue/cyan gradient for info
            colored_msg = ANSI.ocean(msg)
            return f"{ANSI.BOLD}{ANSI.CYAN}{timestamp}{ANSI.RESET} {ANSI.BOLD}{colored_msg}{ANSI.RESET}"
    
    def log(self, msg: str):
        """Log a message with color coding and effects"""
        event_type = self._get_event_type(msg)
        formatted_msg = self._format_event(msg, event_type)
        entry = f"[{datetime.now()}] {msg}"
        self.logs.append(entry)
        if self.config["log_level"] != "silent":
            print(formatted_msg)

    def get_errors(self) -> List[str]:
        """Get error logs"""
        return self.errors

    # ============================================================
    # METADATA
    # ============================================================
    def get_metadata(self) -> Dict[str, Any]:
        """Get event bus metadata"""
        return {
            "name": "event_bus",
            "version": "2.0.0",
            "dependencies": [],
            "compatibility": {
                "shield": True,
                "sandbox": True,
                "kernel_hooks": True,
                "firewall": True,
                "threat_intel": True,
                "plugins": True,
                "modules": True,
            }
        }

    # ============================================================
    # CONFIG
    # ============================================================
    def config_get(self, key: str) -> Any:
        """Get config value"""
        return self.config.get(key)

    def config_set(self, key: str, value: Any):
        """Set config value"""
        self.config[key] = value
        self.log(f"Config updated: {key} = {value}")

    # ============================================================
    # SUBSCRIPTIONS
    # ============================================================
    async def subscribe(self, event: str, callback: Callable):
        """Subscribe to an event"""
        self.listeners[event].append(callback)
        self.log(f"Subscribed: {event}")
        
    async def unsubscribe(self, event: str, callback: Callable):
        """Unsubscribe from an event"""
        if callback in self.listeners[event]:
            self.listeners[event].remove(callback)
            self.log(f"Unsubscribed: {event}")

    def list_subscribers(self, event: str) -> List[Callable]:
        """List subscribers for an event"""
        return self.listeners.get(event, [])

    # ============================================================
    # FILTERS
    # ============================================================
    def add_filter(self, func: Callable):
        """Add a global filter"""
        self.filters.append(func)
        self.log("Filter added")

    # ============================================================
    # HOOKS
    # ============================================================
    def add_hook(self, event: str, func: Callable):
        """Add an event hook"""
        self.hooks[event] = func
        self.log(f"Hook added: {event}")

    def remove_hook(self, event: str):
        """Remove an event hook"""
        if event in self.hooks:
            del self.hooks[event]
            self.log(f"Hook removed: {event}")

    # ============================================================
    # EVENT EMIT
    # ============================================================
    async def emit(self, event: str, data: Any = None):
        """Emit an event"""
        self.log(f"Event emitted: {event}")

        # Apply filters
        for f in self.filters:
            if not f(event, data):
                self.log(f"Event filtered: {event}")
                return False

        # Execute hooks
        if event in self.hooks:
            try:
                self.hooks[event](event, data)
            except Exception as e:
                self.errors.append(str(e))
                self.log(f"Hook error: {e}")
                self.log(traceback.format_exc())

        # Async queue mode
        if self.config["mode"] == "async":
            if len(self.logs) < self.config["max_queue"]:
                await self.event_queue.put((event, data))
            else:
                self.log("Queue overflow")
            return True

        # Sync dispatch mode
        return self.dispatch(event, data)

    # ============================================================
    # DISPATCH
    # ============================================================
    def dispatch(self, event: str, data: Any = None) -> bool:
        """Dispatch event to subscribers (sync)"""
        handlers = self.listeners.get(event, [])
        for h in handlers:
            try:
                if asyncio.iscoroutinefunction(h):
                    asyncio.create_task(h(data))
                else:
                    h(event, data)
            except Exception as e:
                self.errors.append(str(e))
                self.log(f"Dispatch error: {e}")
                self.log(traceback.format_exc())
        return True

    # ============================================================
    # QUEUE PROCESSING
    # ============================================================
    async def flush(self):
        """Flush event queue"""
        self.log("Flushing event queue")
        while not self.event_queue.empty():
            event, data = await self.event_queue.get()
            self.dispatch(event, data)

    async def _process_events(self):
        """Process events from queue"""
        while self.running:
            try:
                event, data = await asyncio.wait_for(
                    self.event_queue.get(), timeout=0.1
                )
                
                # Notify all listeners
                for callback in self.listeners.get(event, []):
                    try:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(data)
                        else:
                            callback(data)
                    except Exception as e:
                        self.errors.append(str(e))
                        self.log(f"Error in event handler: {e}")
                        
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.errors.append(str(e))
                self.log(f"Error processing event: {e}")

    # ============================================================
    # SNAPSHOTS
    # ============================================================
    def export_state(self) -> Dict[str, Any]:
        """Export event bus state"""
        return {
            "subscribers": {k: len(v) for k, v in self.listeners.items()},
            "queue_size": self.event_queue.qsize(),
            "config": self.config,
        }

    def import_state(self, state: Dict[str, Any]):
        """Import event bus state"""
        self.config = state.get("config", self.config)
        self.log("EventBus state restored")

    # ============================================================
    # DIAGNOSTICS
    # ============================================================
    def diagnose(self) -> Dict[str, Any]:
        """Get diagnostic information"""
        return {
            "subscribers": sum(len(v) for v in self.listeners.values()),
            "queue_size": self.event_queue.qsize(),
            "filters": len(self.filters),
            "hooks": len(self.hooks),
            "errors": len(self.errors),
        }

    def auto_fix(self) -> bool:
        """Auto-fix common issues"""
        self.errors.clear()
        # Clear queue if needed
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except:
                break
        self.log("EventBus auto-fix executed")
        return True

    # ============================================================
    # API
    # ============================================================
    def api_list(self) -> List[str]:
        """List available API methods"""
        return [
            "emit",
            "subscribe",
            "unsubscribe",
            "flush",
            "add_filter",
            "add_hook",
            "diagnose",
            "auto_fix",
        ]

    def api_call(self, func: str, *args, **kwargs) -> Optional[Any]:
        """Call API method"""
        if hasattr(self, func):
            return getattr(self, func)(*args, **kwargs)
        return None

    # ============================================================
    # INITIALIZATION & SHUTDOWN
    # ============================================================
    async def initialize(self):
        """Initialize event bus"""
        self.running = True
        self.log("EventBus initialized")
        asyncio.create_task(self._process_events())
        
    async def shutdown(self):
        """Shutdown event bus"""
        self.running = False
        self.log("EventBus shutdown")
        if self.config["auto_flush"]:
            await self.flush()
