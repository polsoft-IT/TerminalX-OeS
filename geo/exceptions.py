"""
GeoEngine Exceptions
"""


class GeoProviderError(Exception):
    """Exception raised when a geolocation provider fails"""
    pass


class GeoEngineError(Exception):
    """Exception raised when the geo engine fails"""
    pass


class GeoCacheError(Exception):
    """Exception raised when geo cache operations fail"""
    pass


class GeoConfigError(Exception):
    """Exception raised when geo configuration is invalid"""
    pass
