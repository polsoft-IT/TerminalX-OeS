"""
 ============================================================
  MODULE/PLUGIN NAME: Geo
  VERSION: 3.0.0
  MODULE CLASS: Geo
  DESCRIPTION:
       GeoEngine v3 — Advanced Geolocation Engine (Godmode Architecture)

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

from .geo_engine import GeoEngine, GeoLocation, GeoProvider, GeoPlugin, EventBus
from .providers import IPInfoProvider, GeoPyProvider, FreeGeoIPProvider, IPAPICOProvider
from .plugins import LoggerPlugin, CachePlugin, StatsPlugin
from .exceptions import GeoProviderError, GeoEngineError

__all__ = [
    'GeoEngine',
    'GeoLocation',
    'GeoProvider',
    'GeoPlugin',
    'EventBus',
    'IPInfoProvider',
    'GeoPyProvider',
    'FreeGeoIPProvider',
    'IPAPICOProvider',
    'LoggerPlugin',
    'CachePlugin',
    'StatsPlugin',
    'RateLimitPlugin',
    'ValidationPlugin',
    'NotificationPlugin',
    'GeoProviderError',
    'GeoEngineError',
    'GeoCacheError',
    'GeoConfigError',
]
