"""
GeoEngine Providers
"""

import asyncio
import aiohttp
from typing import Optional

try:
    from geopy.geocoders import Nominatim
    GEOPY_AVAILABLE = True
except ImportError:
    GEOPY_AVAILABLE = False

from .geo_engine import GeoProvider, GeoLocation
from .exceptions import GeoProviderError


class IPInfoProvider(GeoProvider):
    """IPInfo.io provider for IP geolocation"""
    name = "ipinfo"
    priority = 90

    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.base_url = "https://ipinfo.io"

    async def is_available(self) -> bool:
        """Check if provider is available"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/json", timeout=5) as resp:
                    return resp.status == 200
        except Exception:
            return False

    async def locate(self, query: str) -> GeoLocation:
        """Locate an IP address"""
        url = f"{self.base_url}/{query}/json"
        if self.token:
            url += f"?token={self.token}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=self._get_timeout()) as resp:
                    if resp.status != 200:
                        raise GeoProviderError(f"IPInfo error: HTTP {resp.status}")

                    data = await resp.json()

                    # Parse location
                    lat, lon = None, None
                    if "loc" in data:
                        lat, lon = map(float, data["loc"].split(","))

                    return GeoLocation(
                        latitude=lat or 0.0,
                        longitude=lon or 0.0,
                        city=data.get("city"),
                        region=data.get("region"),
                        country=data.get("country"),
                        postal_code=data.get("postal"),
                        timezone=data.get("timezone"),
                        isp=data.get("org"),
                        org=data.get("org"),
                        raw=data,
                        provider=self.name
                    )

        except aiohttp.ClientError as e:
            raise GeoProviderError(f"IPInfo network error: {e}")
        except Exception as e:
            raise GeoProviderError(f"IPInfo error: {e}")

    def _get_timeout(self) -> int:
        """Get timeout for requests"""
        return 10


class GeoPyProvider(GeoProvider):
    """GeoPy provider using Nominatim (OpenStreetMap)"""
    name = "geopy"
    priority = 80

    def __init__(self, user_agent: str = "geoengine_v3"):
        if not GEOPY_AVAILABLE:
            raise GeoProviderError("geopy package not installed")
        self.geolocator = Nominatim(user_agent=user_agent)
        self.user_agent = user_agent

    async def is_available(self) -> bool:
        """Check if provider is available"""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, lambda: self.geolocator.geocode("test"))
            return True
        except Exception:
            return False

    async def locate(self, query: str) -> GeoLocation:
        """Locate an address or place name"""
        try:
            loop = asyncio.get_event_loop()
            location = await loop.run_in_executor(
                None,
                lambda: self.geolocator.geocode(query, timeout=10)
            )

            if not location:
                raise GeoProviderError(f"Location not found: {query}")

            # Extract address components
            address = location.raw.get('address', {})
            city = address.get('city') or address.get('town') or address.get('village')
            region = address.get('state') or address.get('county')
            country = address.get('country')
            postal_code = address.get('postcode')

            return GeoLocation(
                latitude=location.latitude,
                longitude=location.longitude,
                city=city,
                region=region,
                country=country,
                postal_code=postal_code,
                raw=location.raw,
                provider=self.name
            )

        except Exception as e:
            raise GeoProviderError(f"GeoPy error: {e}")


class FreeGeoIPProvider(GeoProvider):
    """FreeGeoIP.app provider (free, no token required)"""
    name = "freegeoip"
    priority = 70

    def __init__(self):
        self.base_url = "https://freegeoip.app/json"

    async def is_available(self) -> bool:
        """Check if provider is available"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/8.8.8.8", timeout=5) as resp:
                    return resp.status == 200
        except Exception:
            return False

    async def locate(self, query: str) -> GeoLocation:
        """Locate an IP address"""
        url = f"{self.base_url}/{query}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status != 200:
                        raise GeoProviderError(f"FreeGeoIP error: HTTP {resp.status}")

                    data = await resp.json()

                    return GeoLocation(
                        latitude=data.get("latitude", 0.0),
                        longitude=data.get("longitude", 0.0),
                        city=data.get("city"),
                        region=data.get("region_name"),
                        country=data.get("country_name"),
                        country_code=data.get("country_code"),
                        timezone=data.get("time_zone"),
                        raw=data,
                        provider=self.name
                    )

        except aiohttp.ClientError as e:
            raise GeoProviderError(f"FreeGeoIP network error: {e}")
        except Exception as e:
            raise GeoProviderError(f"FreeGeoIP error: {e}")


class IPAPICOProvider(GeoProvider):
    """IP-API.com provider (free, no token required)"""
    name = "ipapi"
    priority = 75

    def __init__(self):
        self.base_url = "http://ip-api.com/json"

    async def is_available(self) -> bool:
        """Check if provider is available"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/8.8.8.8", timeout=5) as resp:
                    return resp.status == 200
        except Exception:
            return False

    async def locate(self, query: str) -> GeoLocation:
        """Locate an IP address"""
        url = f"{self.base_url}/{query}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status != 200:
                        raise GeoProviderError(f"IP-API error: HTTP {resp.status}")

                    data = await resp.json()

                    if data.get("status") == "fail":
                        raise GeoProviderError(f"IP-API error: {data.get('message')}")

                    return GeoLocation(
                        latitude=data.get("lat", 0.0),
                        longitude=data.get("lon", 0.0),
                        city=data.get("city"),
                        region=data.get("regionName"),
                        country=data.get("country"),
                        country_code=data.get("countryCode"),
                        postal_code=data.get("zip"),
                        timezone=data.get("timezone"),
                        isp=data.get("isp"),
                        org=data.get("org"),
                        raw=data,
                        provider=self.name
                    )

        except aiohttp.ClientError as e:
            raise GeoProviderError(f"IP-API network error: {e}")
        except Exception as e:
            raise GeoProviderError(f"IP-API error: {e}")
