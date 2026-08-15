"""
GeoEngine Plugins
"""

from typing import Optional, Dict
from datetime import datetime, timedelta

from .geo_engine import GeoPlugin, GeoLocation
from .exceptions import GeoCacheError


class LoggerPlugin(GeoPlugin):
    """Logger plugin for geo engine - logs all queries and results"""
    name = "logger"

    def __init__(self, verbose: bool = True):
        self.verbose = verbose

    def on_before_query(self, query: str) -> Optional[GeoLocation]:
        """Called before query"""
        if self.verbose:
            print(f"[GEOENGINE] Query: {query}")
        return None

    def on_after_query(self, result: GeoLocation):
        """Called after successful query"""
        if self.verbose:
            print(f"[GEOENGINE] Result: {result}")

    def on_error(self, error: Exception):
        """Called on error"""
        print(f"[GEOENGINE] Error: {error}")

    def on_provider_switch(self, from_provider: str, to_provider: str):
        """Called when switching providers"""
        if self.verbose:
            print(f"[GEOENGINE] Switching provider: {from_provider} -> {to_provider}")


class CachePlugin(GeoPlugin):
    """Cache plugin for geo engine - caches query results"""
    name = "cache"

    def __init__(self, ttl_seconds: int = 3600):
        self.cache: Dict[str, tuple] = {}  # {query: (result, timestamp)}
        self.ttl = ttl_seconds

    def on_before_query(self, query: str) -> Optional[GeoLocation]:
        """Check cache before query"""
        if query in self.cache:
            result, timestamp = self.cache[query]
            age = datetime.now() - timestamp

            if age < timedelta(seconds=self.ttl):
                print(f"[GEOENGINE] Cache hit for: {query}")
                return result
            else:
                # Expired
                del self.cache[query]

        return None

    def on_after_query(self, result: GeoLocation):
        """Cache result after successful query"""
        # Cache by coordinates and by query
        if result.latitude and result.longitude:
            coord_key = f"{result.latitude},{result.longitude}"
            self.cache[coord_key] = (result, datetime.now())

    def clear_cache(self):
        """Clear all cached results"""
        self.cache.clear()

    def get_cache_size(self) -> int:
        """Get number of cached entries"""
        return len(self.cache)


class StatsPlugin(GeoPlugin):
    """Statistics plugin for geo engine - tracks usage statistics"""
    name = "stats"

    def __init__(self):
        self.queries = []
        self.errors = []
        self.provider_switches = []

    def on_after_query(self, result: GeoLocation):
        """Track successful queries"""
        self.queries.append({
            'query': 'unknown',
            'result': str(result),
            'provider': result.provider,
            'timestamp': datetime.now().isoformat()
        })

    def on_error(self, error: Exception):
        """Track errors"""
        self.errors.append({
            'error': str(error),
            'timestamp': datetime.now().isoformat()
        })

    def on_provider_switch(self, from_provider: str, to_provider: str):
        """Track provider switches"""
        self.provider_switches.append({
            'from': from_provider,
            'to': to_provider,
            'timestamp': datetime.now().isoformat()
        })

    def get_stats(self) -> Dict:
        """Get statistics"""
        return {
            'total_queries': len(self.queries),
            'total_errors': len(self.errors),
            'total_switches': len(self.provider_switches),
            'recent_queries': self.queries[-10:] if self.queries else [],
            'recent_errors': self.errors[-10:] if self.errors else [],
        }

    def reset_stats(self):
        """Reset statistics"""
        self.queries.clear()
        self.errors.clear()
        self.provider_switches.clear()


class RateLimitPlugin(GeoPlugin):
    """Rate limit plugin - prevents too many queries"""
    name = "rate_limit"

    def __init__(self, max_queries: int = 100, window_seconds: int = 60):
        self.max_queries = max_queries
        self.window = timedelta(seconds=window_seconds)
        self.queries = []

    def on_before_query(self, query: str) -> Optional[GeoLocation]:
        """Check rate limit before query"""
        now = datetime.now()

        # Remove old queries outside window
        self.queries = [t for t in self.queries if now - t < self.window]

        # Check limit
        if len(self.queries) >= self.max_queries:
            from .exceptions import GeoEngineError
            raise GeoEngineError(f"Rate limit exceeded: {self.max_queries} queries per {self.window.total_seconds()}s")

        self.queries.append(now)
        return None


class ValidationPlugin(GeoPlugin):
    """Validation plugin - validates query format"""
    name = "validation"

    def on_before_query(self, query: str) -> Optional[GeoLocation]:
        """Validate query format"""
        if not query or not query.strip():
            from .exceptions import GeoEngineError
            raise GeoEngineError("Query cannot be empty")

        # Basic IP validation
        if self._is_ip_address(query):
            if not self._validate_ip(query):
                from .exceptions import GeoEngineError
                raise GeoEngineError(f"Invalid IP address: {query}")

        return None

    def _is_ip_address(self, query: str) -> bool:
        """Check if query looks like an IP address"""
        parts = query.split('.')
        return len(parts) == 4 and all(p.isdigit() for p in parts)

    def _validate_ip(self, ip: str) -> bool:
        """Validate IPv4 address"""
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            try:
                num = int(part)
                if num < 0 or num > 255:
                    return False
            except ValueError:
                return False
        return True


class NotificationPlugin(GeoPlugin):
    """Notification plugin - sends notifications on events"""
    name = "notification"

    def __init__(self, callback=None):
        self.callback = callback

    def on_after_query(self, result: GeoLocation):
        """Send notification on successful query"""
        if self.callback:
            self.callback("location_found", result)

    def on_error(self, error: Exception):
        """Send notification on error"""
        if self.callback:
            self.callback("error", str(error))
