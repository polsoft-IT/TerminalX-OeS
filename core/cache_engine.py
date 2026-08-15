"""
Cache Engine - Caching system for TerminalX
"""

import json
import os
import time
from typing import Any, Dict, Optional


class CacheEngine:
    """Cache engine for storing and retrieving data"""
    
    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or os.path.join(
            os.path.dirname(__file__), '..', 'cache'
        )
        self.cache: Dict[str, Dict] = {}
        os.makedirs(self.cache_dir, exist_ok=True)
        
    async def initialize(self):
        """Initialize cache engine"""
        await self._load_cache()
        
    async def _load_cache(self):
        """Load cache from disk"""
        cache_file = os.path.join(self.cache_dir, 'cache.json')
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r') as f:
                    self.cache = json.load(f)
            except Exception as e:
                print(f"Error loading cache: {e}")
                self.cache = {}
                
    async def _save_cache(self):
        """Save cache to disk"""
        cache_file = os.path.join(self.cache_dir, 'cache.json')
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")
            
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            entry = self.cache[key]
            
            # Check if expired
            if entry.get('ttl') and time.time() > entry['expires']:
                del self.cache[key]
                return None
                
            return entry['value']
        return None
        
    async def set(self, key: str, value: Any, ttl: int = None):
        """Set value in cache"""
        entry = {
            'value': value,
            'created': time.time(),
        }
        
        if ttl:
            entry['ttl'] = ttl
            entry['expires'] = time.time() + ttl
            
        self.cache[key] = entry
        await self._save_cache()
        
    async def delete(self, key: str):
        """Delete value from cache"""
        if key in self.cache:
            del self.cache[key]
            await self._save_cache()
            
    async def clear(self):
        """Clear all cache"""
        self.cache.clear()
        await self._save_cache()
        
    async def cleanup_expired(self):
        """Clean up expired entries"""
        current_time = time.time()
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.get('expires') and current_time > entry['expires']
        ]
        
        for key in expired_keys:
            del self.cache[key]
            
        if expired_keys:
            await self._save_cache()
