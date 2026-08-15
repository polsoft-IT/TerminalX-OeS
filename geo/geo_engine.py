"""
 ============================================================
  MODULE/PLUGIN NAME: GeoEngine
  VERSION: 6.0.0
  MODULE CLASS: GeoEngine
  DESCRIPTION:
       Advanced Geolocation Engine with multiple providers, plugin system, GPS daemon for real-time location tracking, map rendering capabilities, and fusion engine for unified location

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
import random
import time
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Callable, List, Any
from abc import ABC, abstractmethod
from datetime import datetime

from .exceptions import GeoProviderError, GeoEngineError


# ============================================================
# GPS DAEMON MODELS
# ============================================================

@dataclass
class GPSFix:
    """GPS fix data model"""
    latitude: float
    longitude: float
    accuracy: float
    timestamp: float
    raw: Optional[Dict] = None


# ============================================================
# GPS DAEMON EVENT BUS
# ============================================================

class GPSEventBus:
    """Event bus for GPS daemon events"""

    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event: str, callback: Callable):
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event: str, data):
        for cb in self._listeners.get(event, []):
            cb(data)


# ============================================================
# GPS DAEMON PLUGIN SYSTEM
# ============================================================

class GPSPlugin:
    """Base plugin class for GPS daemon"""
    name = "base"

    def on_fix(self, fix: GPSFix):
        pass

    def on_error(self, error: Exception):
        pass


class GPSLoggerPlugin(GPSPlugin):
    """Plugin that logs GPS fixes"""
    name = "logger"

    def on_fix(self, fix: GPSFix):
        print(f"[GPS] Fix: {fix.latitude}, {fix.longitude} (±{fix.accuracy}m)")

    def on_error(self, error: Exception):
        print(f"[GPS] Error: {error}")


class GPSRecordPlugin(GPSPlugin):
    """Plugin that records GPS fixes"""
    name = "record"

    def __init__(self):
        self.history: List[GPSFix] = []

    def on_fix(self, fix: GPSFix):
        self.history.append(fix)


# ============================================================
# GPS PROVIDERS
# ============================================================

class GPSProvider(ABC):
    """Base class for GPS providers"""

    async def get_fix(self) -> GPSFix:
        raise NotImplementedError


class MockGPSProvider(GPSProvider):
    """Generates random GPS positions for testing"""
    name = "mock"

    async def get_fix(self) -> GPSFix:
        lat = 52.0 + random.uniform(-0.1, 0.1)
        lon = 21.0 + random.uniform(-0.1, 0.1)
        accuracy = random.uniform(3, 15)

        return GPSFix(
            latitude=lat,
            longitude=lon,
            accuracy=accuracy,
            timestamp=time.time(),
            raw={"mock": True}
        )


# ============================================================
# GPS DAEMON CORE
# ============================================================

class GPSDaemon:
    """GPS streaming daemon for real-time location tracking"""

    def __init__(self, provider: GPSProvider):
        self.provider = provider
        self.plugins: List[GPSPlugin] = []
        self.events = GPSEventBus()
        self.running = False
        self.last_fix: Optional[GPSFix] = None
        self.update_interval = 1.0  # seconds
        self.daemon_task: Optional[asyncio.Task] = None

    def register_plugin(self, plugin: GPSPlugin):
        self.plugins.append(plugin)

    def subscribe(self, event: str, callback: Callable):
        self.events.subscribe(event, callback)

    async def start(self):
        """Start the GPS daemon"""
        self.running = True
        print("[GPS] Daemon started")

        self.daemon_task = asyncio.create_task(self._daemon_loop())

    async def _daemon_loop(self):
        """Main daemon loop"""
        while self.running:
            try:
                fix = await self.provider.get_fix()
                self.last_fix = fix

                # Plugins
                for plugin in self.plugins:
                    try:
                        plugin.on_fix(fix)
                    except Exception as e:
                        plugin.on_error(e)

                # EventBus
                self.events.emit("gps_fix", fix)

            except Exception as e:
                for plugin in self.plugins:
                    plugin.on_error(e)

            await asyncio.sleep(self.update_interval)

    def stop(self):
        """Stop the GPS daemon"""
        self.running = False
        if self.daemon_task:
            self.daemon_task.cancel()
        print("[GPS] Daemon stopped")

    def get_last_fix(self) -> Optional[GPSFix]:
        """Get the last GPS fix"""
        return self.last_fix

    def get_status(self) -> Dict[str, Any]:
        """Get GPS daemon status"""
        fix = self.get_last_fix()
        return {
            'running': self.running,
            'last_fix': fix,
            'plugins': [p.name for p in self.plugins],
            'update_interval': self.update_interval
        }


# ============================================================
# GPS COMMANDS
# ============================================================

class GPSCommands:
    """Command interface for GPS daemon"""

    def __init__(self, daemon: GPSDaemon):
        self.daemon = daemon

    def status(self) -> Dict[str, Any]:
        """Get GPS daemon status"""
        status = self.daemon.get_status()
        fix = status['last_fix']
        
        if not fix:
            return {
                'success': True,
                'running': status['running'],
                'message': 'No GPS fix yet'
            }
        
        return {
            'success': True,
            'running': status['running'],
            'latitude': fix.latitude,
            'longitude': fix.longitude,
            'accuracy': fix.accuracy,
            'timestamp': fix.timestamp,
            'message': f"GPS Fix: {fix.latitude}, {fix.longitude}, accuracy={fix.accuracy}m"
        }

    def stop(self) -> Dict[str, Any]:
        """Stop GPS daemon"""
        self.daemon.stop()
        return {
            'success': True,
            'message': 'GPS daemon stopped'
        }

    def start(self) -> Dict[str, Any]:
        """Start GPS daemon (async)"""
        return {
            'success': True,
            'message': 'GPS daemon start requested (async)'
        }


# ============================================================
# GEO ENGINE MODELS
# ============================================================


@dataclass
class GeoLocation:
    """Geolocation data model"""
    latitude: float
    longitude: float
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    postal_code: Optional[str] = None
    timezone: Optional[str] = None
    isp: Optional[str] = None
    org: Optional[str] = None
    raw: Optional[Dict] = None
    provider: Optional[str] = None
    timestamp: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    def __str__(self) -> str:
        """String representation"""
        parts = []
        if self.city:
            parts.append(self.city)
        if self.region:
            parts.append(self.region)
        if self.country:
            parts.append(self.country)
        location = ", ".join(parts) if parts else "Unknown"
        return f"{location} ({self.latitude}, {self.longitude})"


class EventBus:
    """Event bus for geo engine events"""

    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event: str, callback: Callable):
        """Subscribe to an event"""
        self._listeners.setdefault(event, []).append(callback)

    def unsubscribe(self, event: str, callback: Callable):
        """Unsubscribe from an event"""
        if event in self._listeners:
            self._listeners[event].remove(callback)

    def emit(self, event: str, data: Any):
        """Emit an event"""
        for cb in self._listeners.get(event, []):
            try:
                cb(data)
            except Exception as e:
                print(f"[EventBus] Error in callback for event '{event}': {e}")


class GeoPlugin(ABC):
    """Base plugin class for geo engine"""
    name = "base"

    def on_before_query(self, query: str) -> Optional[GeoLocation]:
        """Called before query - can return cached result"""
        return None

    def on_after_query(self, result: GeoLocation):
        """Called after successful query"""
        pass

    def on_error(self, error: Exception):
        """Called on error"""
        pass

    def on_provider_switch(self, from_provider: str, to_provider: str):
        """Called when switching providers"""
        pass


class GeoProvider(ABC):
    """Base provider class for geolocation services"""
    name = "base"
    priority = 100

    @abstractmethod
    async def locate(self, query: str) -> GeoLocation:
        """Locate a query (IP address or location name)"""
        pass

    async def is_available(self) -> bool:
        """Check if provider is available"""
        return True


class GeoEngine:
    """Advanced geolocation engine with plugin system, multiple providers, and GPS daemon"""

    def __init__(self):
        self.providers: Dict[str, GeoProvider] = {}
        self.plugins: List[GeoPlugin] = []
        self.events = EventBus()
        self.config: Dict[str, Any] = {
            'default_provider': None,
            'timeout': 10,
            'max_retries': 3,
            'enable_fallback': True,
        }
        self.stats: Dict[str, Any] = {
            'queries': 0,
            'successes': 0,
            'failures': 0,
            'cache_hits': 0,
            'provider_usage': {},
        }
        
        # GPS Daemon integration
        self.gps_daemon: Optional[GPSDaemon] = None
        self.gps_commands: Optional[GPSCommands] = None
        self.gps_enabled = False
        
        # Map Engine integration
        self.map_engine = None
        self.map_enabled = False
        
        # Fusion Engine integration
        self.fusion_engine = None
        self.fusion_enabled = False

    def register_provider(self, provider: GeoProvider):
        """Register a geolocation provider"""
        self.providers[provider.name] = provider
        self.stats['provider_usage'][provider.name] = 0

    def unregister_provider(self, name: str):
        """Unregister a provider"""
        if name in self.providers:
            del self.providers[name]
            if name in self.stats['provider_usage']:
                del self.stats['provider_usage'][name]

    def register_plugin(self, plugin: GeoPlugin):
        """Register a plugin"""
        self.plugins.append(plugin)

    def unregister_plugin(self, name: str):
        """Unregister a plugin by name"""
        self.plugins = [p for p in self.plugins if p.name != name]

    def configure(self, **kwargs):
        """Configure the geo engine"""
        self.config.update(kwargs)

    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics"""
        return self.stats.copy()

    def reset_stats(self):
        """Reset statistics"""
        self.stats = {
            'queries': 0,
            'successes': 0,
            'failures': 0,
            'cache_hits': 0,
            'provider_usage': {name: 0 for name in self.providers},
        }
    
    # ============================================================
    # GPS DAEMON INTEGRATION
    # ============================================================
    
    def enable_gps(self, provider: GPSProvider = None):
        """Enable GPS daemon with specified provider"""
        if provider is None:
            provider = MockGPSProvider()
        
        self.gps_daemon = GPSDaemon(provider)
        self.gps_commands = GPSCommands(self.gps_daemon)
        self.gps_enabled = True
        
        # Register default plugins
        self.gps_daemon.register_plugin(GPSLoggerPlugin())
        
    def disable_gps(self):
        """Disable GPS daemon"""
        if self.gps_daemon:
            self.gps_daemon.stop()
        self.gps_daemon = None
        self.gps_commands = None
        self.gps_enabled = False
    
    async def start_gps(self):
        """Start GPS daemon"""
        if self.gps_daemon and self.gps_enabled:
            await self.gps_daemon.start()
            return True
        return False
    
    def stop_gps(self):
        """Stop GPS daemon"""
        if self.gps_daemon:
            self.gps_daemon.stop()
            return True
        return False
    
    def get_gps_status(self) -> Dict[str, Any]:
        """Get GPS daemon status"""
        if self.gps_commands:
            return self.gps_commands.status()
        return {
            'success': False,
            'message': 'GPS daemon not enabled'
        }
    
    def register_gps_plugin(self, plugin: GPSPlugin):
        """Register a GPS plugin"""
        if self.gps_daemon:
            self.gps_daemon.register_plugin(plugin)
            return True
        return False
    
    def subscribe_gps(self, event: str, callback: Callable):
        """Subscribe to GPS events"""
        if self.gps_daemon:
            self.gps_daemon.subscribe(event, callback)
            return True
        return False
    
    # ============================================================
    # MAP ENGINE INTEGRATION
    # ============================================================
    
    def enable_map(self, renderer_type: str = "osm", api_key: str = None):
        """Enable map engine with specified renderer"""
        try:
            from .map_engine import MapEngine, OSMRenderer, GoogleRenderer
            
            if renderer_type == "osm":
                renderer = OSMRenderer()
            elif renderer_type == "google" and api_key:
                renderer = GoogleRenderer(api_key)
            else:
                renderer = OSMRenderer()  # Default to OSM
            
            self.map_engine = MapEngine(renderer)
            self.map_enabled = True
            return True
        except Exception as e:
            print(f"[GEO] Failed to enable map engine: {e}")
            return False
    
    def disable_map(self):
        """Disable map engine"""
        self.map_engine = None
        self.map_enabled = False
        return True
    
    def get_map_status(self) -> Dict[str, Any]:
        """Get map engine status"""
        if self.map_engine:
            return {
                'success': True,
                'enabled': self.map_enabled,
                'points': len(self.map_engine.points),
                'paths': len(self.map_engine.paths),
                'heat': len(self.map_engine.heat),
                'plugins': [p.name for p in self.map_engine.plugins]
            }
        return {
            'success': False,
            'message': 'Map engine not enabled'
        }
    
    def register_map_plugin(self, plugin):
        """Register a map plugin"""
        if self.map_engine:
            self.map_engine.register_plugin(plugin)
            return True
        return False
    
    def subscribe_map(self, event: str, callback: Callable):
        """Subscribe to map events"""
        if self.map_engine:
            self.map_engine.subscribe(event, callback)
            return True
        return False
    
    # ============================================================
    # FUSION ENGINE INTEGRATION
    # ============================================================
    
    def enable_fusion(self):
        """Enable fusion engine"""
        try:
            from .fusion_engine import FusionEngine
            
            self.fusion_engine = FusionEngine()
            self.fusion_enabled = True
            return True
        except Exception as e:
            print(f"[GEO] Failed to enable fusion engine: {e}")
            return False
    
    def disable_fusion(self):
        """Disable fusion engine"""
        self.fusion_engine = None
        self.fusion_enabled = False
        return True
    
    def get_fusion_status(self) -> Dict[str, Any]:
        """Get fusion engine status"""
        if self.fusion_engine:
            return {
                'success': True,
                'enabled': self.fusion_enabled,
                'plugins': [p.name for p in self.fusion_engine.plugins],
                'weights': {
                    'gps': self.fusion_engine.weight_gps,
                    'bts': self.fusion_engine.weight_bts,
                    'wifi': self.fusion_engine.weight_wifi
                }
            }
        return {
            'success': False,
            'message': 'Fusion engine not enabled'
        }
    
    def register_fusion_plugin(self, plugin):
        """Register a fusion plugin"""
        if self.fusion_engine:
            self.fusion_engine.register_plugin(plugin)
            return True
        return False
    
    def subscribe_fusion(self, event: str, callback: Callable):
        """Subscribe to fusion events"""
        if self.fusion_engine:
            self.fusion_engine.subscribe(event, callback)
            return True
        return False
    
    def update_fusion_gps(self, fix):
        """Update fusion engine with GPS data"""
        if self.fusion_engine:
            self.fusion_engine.update_gps(fix)
            return True
        return False
    
    def update_fusion_bts(self, loc):
        """Update fusion engine with BTS data"""
        if self.fusion_engine:
            self.fusion_engine.update_bts(loc)
            return True
        return False
    
    def update_fusion_wifi(self, loc):
        """Update fusion engine with WiFi data"""
        if self.fusion_engine:
            self.fusion_engine.update_wifi(loc)
            return True
        return False

    async def locate(self, query: str, provider_name: str = None) -> GeoLocation:
        """
        Locate a query using registered providers

        Args:
            query: IP address or location name
            provider_name: Specific provider to use (optional)

        Returns:
            GeoLocation object

        Raises:
            GeoEngineError: If all providers fail
        """
        self.stats['queries'] += 1

        # PLUGINS: before_query
        for plugin in self.plugins:
            try:
                cached = plugin.on_before_query(query)
                if cached:
                    self.stats['cache_hits'] += 1
                    self.stats['successes'] += 1
                    self.events.emit("cache_hit", {"query": query, "result": cached})
                    return cached
            except Exception as e:
                plugin.on_error(e)

        # Determine provider order
        if provider_name:
            providers_to_try = [provider_name] if provider_name in self.providers else []
        else:
            providers_to_try = sorted(
                self.providers.keys(),
                key=lambda x: self.providers[x].priority,
                reverse=True
            )

        if not providers_to_try:
            raise GeoEngineError("No providers available")

        # Try providers in order
        last_error = None
        for i, provider_name in enumerate(providers_to_try):
            provider = self.providers[provider_name]

            # Notify provider switch
            if i > 0 and self.config.get('enable_fallback'):
                for plugin in self.plugins:
                    try:
                        plugin.on_provider_switch(providers_to_try[i-1], provider_name)
                    except Exception as e:
                        plugin.on_error(e)

            try:
                # Check provider availability
                if not await provider.is_available():
                    continue

                # Execute query
                result = await provider.locate(query)
                result.provider = provider_name
                result.timestamp = datetime.now().isoformat()

                # Update stats
                self.stats['successes'] += 1
                self.stats['provider_usage'][provider_name] += 1

                # PLUGINS: after_query
                for plugin in self.plugins:
                    try:
                        plugin.on_after_query(result)
                    except Exception as e:
                        plugin.on_error(e)

                self.events.emit("location", result)
                return result

            except Exception as e:
                last_error = e
                for plugin in self.plugins:
                    plugin.on_error(e)

                # Try next provider if fallback enabled
                if not self.config.get('enable_fallback'):
                    break

        # All providers failed
        self.stats['failures'] += 1
        raise GeoEngineError(f"All providers failed. Last error: {last_error}")

    async def batch_locate(self, queries: List[str]) -> Dict[str, GeoLocation]:
        """
        Locate multiple queries in parallel

        Args:
            queries: List of IP addresses or location names

        Returns:
            Dictionary mapping query to GeoLocation
        """
        tasks = [self.locate(query) for query in queries]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        output = {}
        for query, result in zip(queries, results):
            if isinstance(result, Exception):
                output[query] = None
            else:
                output[query] = result

        return output

    async def reverse_geocode(self, lat: float, lon: float) -> GeoLocation:
        """
        Reverse geocode coordinates to location

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            GeoLocation object
        """
        query = f"{lat},{lon}"
        return await self.locate(query)
