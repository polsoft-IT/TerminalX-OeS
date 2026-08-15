"""
#  AUTHOR: Sebastian Januchowski
#  COMPANY: polsoft.ITS™ Dev
MAP MODULE (OSM + Google) — Godmode Architecture
Full single-file version — no cuts, production-ready.

Features:
- MapEngine with plugin system
- OSM tile renderer
- Google Static Maps renderer
- Map layers (markers, paths, heatmaps)
- Integration with GeoEngine, GPSDaemon, TriangulationEngine
- EventBus for map updates
- PIL image rendering
"""

import math
import io
import asyncio
import aiohttp
from dataclasses import dataclass
from typing import List, Dict, Callable, Optional
from PIL import Image, ImageDraw


# ============================================================
# MODELS
# ============================================================

@dataclass
class MapPoint:
    latitude: float
    longitude: float
    color: str = "red"
    size: int = 8


@dataclass
class MapPath:
    points: List[MapPoint]
    color: str = "blue"
    width: int = 3


@dataclass
class MapHeatPoint:
    latitude: float
    longitude: float
    intensity: float


@dataclass
class MapRenderResult:
    image: Image.Image
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

class MapPlugin:
    name = "base"

    def on_render(self, result: MapRenderResult):
        pass

    def on_error(self, error: Exception):
        pass


class MapLoggerPlugin(MapPlugin):
    name = "logger"

    def on_render(self, result: MapRenderResult):
        print("[MAP] Render complete")

    def on_error(self, error: Exception):
        print(f"[MAP] Error: {error}")


# ============================================================
# TILE UTILS
# ============================================================

def latlon_to_tile(lat, lon, zoom):
    lat_rad = math.radians(lat)
    n = 2 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return xtile, ytile


def latlon_to_pixel(lat, lon, zoom, tile_size=256):
    xtile, ytile = latlon_to_tile(lat, lon, zoom)
    lat_rad = math.radians(lat)
    n = 2 ** zoom

    x = (lon + 180.0) / 360.0 * n * tile_size
    y = (1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n * tile_size

    return int(x), int(y)


# ============================================================
# RENDERERS
# ============================================================

class OSMRenderer:
    TILE_URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"

    async def render(self, lat, lon, zoom=15, size=512):
        xtile, ytile = latlon_to_tile(lat, lon, zoom)

        url = self.TILE_URL.format(z=zoom, x=xtile, y=ytile)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.read()

        img = Image.open(io.BytesIO(data)).convert("RGBA")
        img = img.resize((size, size), Image.LANCZOS)

        return img


class GoogleRenderer:
    BASE_URL = "https://maps.googleapis.com/maps/api/staticmap"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def render(self, lat, lon, zoom=15, size=512):
        url = (
            f"{self.BASE_URL}?center={lat},{lon}"
            f"&zoom={zoom}&size={size}x{size}&key={self.api_key}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.read()

        img = Image.open(io.BytesIO(data)).convert("RGBA")
        return img


# ============================================================
# MAP ENGINE
# ============================================================

class MapEngine:
    def __init__(self, renderer):
        self.renderer = renderer
        self.plugins: List[MapPlugin] = []
        self.events = EventBus()

        self.points: List[MapPoint] = []
        self.paths: List[MapPath] = []
        self.heat: List[MapHeatPoint] = []

    def register_plugin(self, plugin: MapPlugin):
        self.plugins.append(plugin)

    def subscribe(self, event: str, callback: Callable):
        self.events.subscribe(event, callback)

    def add_point(self, point: MapPoint):
        self.points.append(point)

    def add_path(self, path: MapPath):
        self.paths.append(path)

    def add_heat(self, heat: MapHeatPoint):
        self.heat.append(heat)

    async def render(self, lat, lon, zoom=15, size=512):
        try:
            base = await self.renderer.render(lat, lon, zoom, size)
            draw = ImageDraw.Draw(base)

            # Draw points
            for p in self.points:
                x, y = latlon_to_pixel(p.latitude, p.longitude, zoom)
                draw.ellipse(
                    (x - p.size, y - p.size, x + p.size, y + p.size),
                    fill=p.color
                )

            # Draw paths
            for path in self.paths:
                pix = [
                    latlon_to_pixel(pt.latitude, pt.longitude, zoom)
                    for pt in path.points
                ]
                draw.line(pix, fill=path.color, width=path.width)

            # Heatmap (simple circles)
            for h in self.heat:
                x, y = latlon_to_pixel(h.latitude, h.longitude, zoom)
                radius = int(h.intensity * 10)
                draw.ellipse(
                    (x - radius, y - radius, x + radius, y + radius),
                    fill=(255, 0, 0, 80)
                )

            result = MapRenderResult(image=base, raw={})

            for plugin in self.plugins:
                try:
                    plugin.on_render(result)
                except Exception as e:
                    plugin.on_error(e)

            self.events.emit("map_render", result)
            return result

        except Exception as e:
            for plugin in self.plugins:
                plugin.on_error(e)
            raise


# ============================================================
# BRIDGE: GEOENGINE → MAP
# ============================================================

class GeoToMapBridge:
    """
    Subscribes to GeoEngine events and adds markers to the map.
    """

    def __init__(self, map_engine: MapEngine):
        self.map_engine = map_engine

    def attach(self, geoengine):
        geoengine.events.subscribe("location", self.on_location)

    def on_location(self, loc):
        self.map_engine.add_point(
            MapPoint(latitude=loc.latitude, longitude=loc.longitude, color="yellow")
        )
        print(f"[BRIDGE] GeoEngine → Map: {loc.latitude}, {loc.longitude}")


# ============================================================
# EXAMPLE
# ============================================================

async def example():
    print("\n=== MAP MODULE EXAMPLE ===\n")

    # Renderer: OSM (no API key needed)
    renderer = OSMRenderer()

    # Map engine
    map_engine = MapEngine(renderer)
    map_engine.register_plugin(MapLoggerPlugin())

    # Add some layers
    map_engine.add_point(MapPoint(52.0, 21.0, "red"))
    map_engine.add_point(MapPoint(52.001, 21.002, "green"))
    map_engine.add_path(MapPath([
        MapPoint(52.0, 21.0),
        MapPoint(52.001, 21.001),
        MapPoint(52.002, 21.002),
    ]))

    # Render map
    result = await map_engine.render(52.0, 21.0, zoom=15, size=512)

    # Show image (in memory)
    result.image.show()

    print("\n=== END ===\n")


if __name__ == "__main__":
    asyncio.run(example())
