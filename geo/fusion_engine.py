"""
#  AUTHOR: Sebastian Januchowski
#  COMPANY: polsoft.ITS™ Dev
FUSIONENGINE v1 — Unified GPS + BTS + WiFi + Map Engine
Godmode Architecture — Full single-file version, no cuts.

Features:
- Fusion of GPS, BTS triangulation, WiFi positioning
- Confidence scoring + weighted fusion
- Integration with GeoEngine + MapEngine
- EventBus for unified location events
- Plugins (logger, recorder)
- Async architecture
"""

import asyncio
import time
from dataclasses import dataclass
from typing import Optional, Dict, List, Callable


# ============================================================
# MODELS
# ============================================================

@dataclass
class FusionLocation:
    latitude: float
    longitude: float
    accuracy: float
    confidence: float
    timestamp: float
    raw: Dict


# ============================================================
# EVENT BUS
# ============================================================

class EventBus:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event: str, callback: Callable):
        self._listeners.setdefault(event, []).append(callback)

    def emit(self, event: str, data):
        for cb in self._listeners.get(event, []):
            cb(data)


# ============================================================
# PLUGINS
# ============================================================

class FusionPlugin:
    name = "base"

    def on_fusion(self, loc: FusionLocation):
        pass

    def on_error(self, error: Exception):
        pass


class FusionLoggerPlugin(FusionPlugin):
    name = "logger"

    def on_fusion(self, loc: FusionLocation):
        print(f"[FUSION] {loc.latitude}, {loc.longitude} (±{loc.accuracy}m, conf={loc.confidence})")

    def on_error(self, error: Exception):
        print(f"[FUSION] Error: {error}")


class FusionRecordPlugin(FusionPlugin):
    name = "record"

    def __init__(self):
        self.history: List[FusionLocation] = []

    def on_fusion(self, loc: FusionLocation):
        self.history.append(loc)


# ============================================================
# FUSION ENGINE CORE
# ============================================================

class FusionEngine:
    def __init__(self):
        self.plugins: List[FusionPlugin] = []
        self.events = EventBus()

        # incoming data
        self.gps_fix = None
        self.bts_loc = None
        self.wifi_loc = None

        # weights
        self.weight_gps = 1.0
        self.weight_bts = 0.7
        self.weight_wifi = 0.9

    def register_plugin(self, plugin: FusionPlugin):
        self.plugins.append(plugin)

    def subscribe(self, event: str, callback: Callable):
        self.events.subscribe(event, callback)

    # ------------------------------------------------------------
    # INPUTS FROM OTHER MODULES
    # ------------------------------------------------------------

    def update_gps(self, fix):
        self.gps_fix = fix
        self._try_fuse()

    def update_bts(self, loc):
        self.bts_loc = loc
        self._try_fuse()

    def update_wifi(self, loc):
        self.wifi_loc = loc
        self._try_fuse()

    # ------------------------------------------------------------
    # FUSION LOGIC
    # ------------------------------------------------------------

    def _try_fuse(self):
        sources = []

        if self.gps_fix:
            sources.append(("gps", self.gps_fix.latitude, self.gps_fix.longitude, self.gps_fix.accuracy, self.weight_gps))

        if self.bts_loc:
            sources.append(("bts", self.bts_loc.latitude, self.bts_loc.longitude, self.bts_loc.accuracy, self.weight_bts))

        if self.wifi_loc:
            sources.append(("wifi", self.wifi_loc.latitude, self.wifi_loc.longitude, self.wifi_loc.accuracy, self.weight_wifi))

        if len(sources) == 0:
            return

        # Weighted fusion
        total_weight = sum(w for _, _, _, _, w in sources)

        fused_lat = sum(lat * w for _, lat, _, _, w in sources) / total_weight
        fused_lon = sum(lon * w for _, _, lon, _, w in sources) / total_weight

        # Accuracy = weighted average
        fused_acc = sum(acc * w for _, _, _, acc, w in sources) / total_weight

        # Confidence = number of sources + inverse accuracy
        confidence = len(sources) + (1 / (fused_acc + 1))

        loc = FusionLocation(
            latitude=fused_lat,
            longitude=fused_lon,
            accuracy=fused_acc,
            confidence=confidence,
            timestamp=time.time(),
            raw={"sources": sources}
        )

        self._emit(loc)

    # ------------------------------------------------------------
    # Emit to plugins + event bus
    # ------------------------------------------------------------

    def _emit(self, loc: FusionLocation):
        for plugin in self.plugins:
            try:
                plugin.on_fusion(loc)
            except Exception as e:
                plugin.on_error(e)

        self.events.emit("fusion_location", loc)


# ============================================================
# BRIDGE: FUSION → GEOENGINE
# ============================================================

class FusionToGeoBridge(FusionPlugin):
    def __init__(self, geoengine):
        self.geoengine = geoengine

    def on_fusion(self, loc: FusionLocation):
        geo = GeoLocation(
            latitude=loc.latitude,
            longitude=loc.longitude,
            raw={"fusion": True, "accuracy": loc.accuracy, "confidence": loc.confidence}
        )
        self.geoengine.events.emit("location", geo)
        print(f"[BRIDGE] Fusion → GeoEngine: {geo.latitude}, {geo.longitude}")


# ============================================================
# BRIDGE: FUSION → MAPENGINE
# ============================================================

class FusionToMapBridge(FusionPlugin):
    def __init__(self, map_engine):
        self.map_engine = map_engine

    def on_fusion(self, loc: FusionLocation):
        self.map_engine.add_point(
            MapPoint(latitude=loc.latitude, longitude=loc.longitude, color="yellow")
        )
        print(f"[BRIDGE] Fusion → Map: {loc.latitude}, {loc.longitude}")


# ============================================================
# MOCK MODELS FOR EXAMPLE
# ============================================================

@dataclass
class GeoLocation:
    latitude: float
    longitude: float
    raw: Dict


@dataclass
class GPSFix:
    latitude: float
    longitude: float
    accuracy: float
    timestamp: float


@dataclass
class TriangulatedLocation:
    latitude: float
    longitude: float
    accuracy: float
    timestamp: float


@dataclass
class WiFiLocation:
    latitude: float
    longitude: float
    accuracy: float
    timestamp: float


# ============================================================
# EXAMPLE
# ============================================================

async def example():
    print("\n=== FUSIONENGINE EXAMPLE ===\n")

    # Mock GeoEngine
    class GeoEngineMock:
        def __init__(self):
            self.events = EventBus()

    geo = GeoEngineMock()

    # Mock MapEngine
    class MapEngineMock:
        def __init__(self):
            self.points = []

        def add_point(self, p):
            self.points.append(p)

    map_engine = MapEngineMock()

    # FusionEngine
    fusion = FusionEngine()
    fusion.register_plugin(FusionLoggerPlugin())
    fusion.register_plugin(FusionRecordPlugin())
    fusion.register_plugin(FusionToGeoBridge(geo))
    fusion.register_plugin(FusionToMapBridge(map_engine))

    # GeoEngine subscriber
    def on_geo(loc):
        print(f"[GEOENGINE EVENT] {loc.latitude}, {loc.longitude}")

    geo.events.subscribe("location", on_geo)

    # Simulate incoming data
    fusion.update_gps(GPSFix(52.0, 21.0, 5, time.time()))
    fusion.update_bts(TriangulatedLocation(52.001, 21.002, 50, time.time()))
    fusion.update_wifi(WiFiLocation(51.999, 21.001, 20, time.time()))

    print("\n=== END ===\n")


if __name__ == "__main__":
    asyncio.run(example())
