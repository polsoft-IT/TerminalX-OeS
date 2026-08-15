"""
 ============================================================
  MODULE/PLUGIN NAME: PluginEvents
  VERSION: 1.0.0
  MODULE CLASS: PluginEvents
  DESCRIPTION:
       Event bus for TerminalX plugin system

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
# ============================================================

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime

from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class EventCallback:
    """Event callback"""
    plugin_name: str
    callback: Callable
    once: bool = False


@dataclass
class Event:
    """Event data"""
    name: str
    data: Dict[str, Any]
    timestamp: str


class PluginEvents:
    """
    PLUGIN EVENT BUS:
    - Subscribe to events
    - Unsubscribe from events
    - Emit events
    - Event filtering
    - Event history
    """

    def __init__(self, logger: Optional[CleanLogger] = None):
        self.logger = logger or CleanLogger("PluginEvents", LogLevel.INFO)
        self.subscribers: Dict[str, List[EventCallback]] = {}
        self.event_history: List[Event] = []
        self.max_history = 1000

    # ============================================================
    # EVENT SUBSCRIPTION
    # ============================================================
    def subscribe(self, event_name: str, plugin_name: str, callback: Callable, once: bool = False) -> bool:
        """Subscribe to event"""
        try:
            if event_name not in self.subscribers:
                self.subscribers[event_name] = []

            event_callback = EventCallback(
                plugin_name=plugin_name,
                callback=callback,
                once=once
            )

            self.subscribers[event_name].append(event_callback)
            self.logger.info(f"Subscribed to event: {event_name} by {plugin_name}")
            return True

        except Exception as e:
            self.logger.error(f"Error subscribing to event: {e}")
            return False

    def unsubscribe(self, event_name: str, plugin_name: str) -> bool:
        """Unsubscribe from event"""
        if event_name not in self.subscribers:
            self.logger.error(f"Event not found: {event_name}")
            return False

        # Remove callbacks for plugin
        original_count = len(self.subscribers[event_name])
        self.subscribers[event_name] = [
            cb for cb in self.subscribers[event_name] if cb.plugin_name != plugin_name
        ]

        if len(self.subscribers[event_name]) == 0:
            del self.subscribers[event_name]

        removed = original_count - len(self.subscribers[event_name])
        self.logger.info(f"Unsubscribed {removed} callbacks for {plugin_name}: {event_name}")
        return True

    def unsubscribe_plugin(self, plugin_name: str) -> int:
        """Unsubscribe plugin from all events"""
        removed = 0
        for event_name in list(self.subscribers.keys()):
            original_count = len(self.subscribers[event_name])
            self.subscribers[event_name] = [
                cb for cb in self.subscribers[event_name] if cb.plugin_name != plugin_name
            ]
            removed += original_count - len(self.subscribers[event_name])

            if len(self.subscribers[event_name]) == 0:
                del self.subscribers[event_name]

        self.logger.info(f"Unsubscribed {removed} callbacks for plugin: {plugin_name}")
        return removed

    # ============================================================
    # EVENT EMISSION
    # ============================================================
    def emit(self, event_name: str, data: Dict[str, Any] = None) -> List[Any]:
        """Emit event to all subscribers"""
        if data is None:
            data = {}

        # Create event
        event = Event(
            name=event_name,
            data=data,
            timestamp=str(datetime.now())
        )

        # Add to history
        self.event_history.append(event)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)

        # Emit to subscribers
        results = []
        if event_name in self.subscribers:
            to_remove = []
            for callback in self.subscribers[event_name]:
                try:
                    result = callback.callback(event)
                    results.append(result)
                    
                    if callback.once:
                        to_remove.append(callback)
                except Exception as e:
                    self.logger.error(f"Error in event callback for {event_name} by {callback.plugin_name}: {e}")

            # Remove once callbacks
            for callback in to_remove:
                self.subscribers[event_name].remove(callback)

            if len(self.subscribers[event_name]) == 0:
                del self.subscribers[event_name]

        self.logger.info(f"Event emitted: {event_name} to {len(results)} subscribers")
        return results

    def emit_async(self, event_name: str, data: Dict[str, Any] = None) -> None:
        """Emit event asynchronously (non-blocking)"""
        # In a real implementation, this would use asyncio
        self.emit(event_name, data)

    # ============================================================
    # EVENT QUERIES
    # ============================================================
    def has_subscribers(self, event_name: str) -> bool:
        """Check if event has subscribers"""
        return event_name in self.subscribers and len(self.subscribers[event_name]) > 0

    def get_subscribers(self, event_name: str) -> List[EventCallback]:
        """Get all subscribers for event"""
        return self.subscribers.get(event_name, [])

    def list_events(self) -> List[str]:
        """List all event names"""
        return list(self.subscribers.keys())

    def count_subscribers(self, event_name: str) -> int:
        """Count subscribers for event"""
        return len(self.subscribers.get(event_name, []))

    # ============================================================
    # EVENT HISTORY
    # ============================================================
    def get_history(self, event_name: Optional[str] = None, limit: int = 100) -> List[Event]:
        """Get event history"""
        if event_name:
            events = [e for e in self.event_history if e.name == event_name]
        else:
            events = self.event_history

        return events[-limit:]

    def clear_history(self) -> bool:
        """Clear event history"""
        self.event_history.clear()
        self.logger.info("Event history cleared")
        return True

    # ============================================================
    # STANDARD EVENTS
    # ============================================================
    @staticmethod
    def get_standard_events() -> List[str]:
        """Get list of standard event names"""
        return [
            # Tag events
            "on_tag_added", "on_tag_removed", "on_tags_cleared",
            # Metadata events
            "on_metadata_extracted",
            # Rule events
            "on_rule_triggered",
            # File events
            "on_file_changed", "on_file_created", "on_file_deleted",
            # Sync events
            "on_sync_start", "on_sync_finish",
            # AI events
            "on_ai_classification", "on_ai_similarity",
            # Plugin events
            "on_plugin_loaded", "on_plugin_unloaded", "on_plugin_enabled", "on_plugin_disabled",
        ]
