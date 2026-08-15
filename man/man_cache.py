"""
 ============================================================
  MODULE/PLUGIN NAME: ManCache
  VERSION: 1.0.2
  MODULE CLASS: ManCache
  DESCRIPTION:
       Man page caching system - improves performance by caching parsed man pages (supports comprehensive command documentation)

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

import os
import json
import time
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from enum import Enum


class CachePolicy(Enum):
    """Cache eviction policies"""
    LRU = "lru"  # Least Recently Used
    FIFO = "fifo"  # First In First Out
    LFU = "lfu"  # Least Frequently Used


class ManCache:
    """Man page cache system"""
    
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.enabled = True
        self.cache_dir: str = ""
        self.memory_cache: Dict[str, Dict] = {}
        self.access_times: Dict[str, float] = {}
        self.access_counts: Dict[str, int] = {}
        self.max_memory_size = 100
        self.max_disk_size = 1000
        self.cache_ttl = 3600  # 1 hour default
        self.policy = CachePolicy.LRU
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'size': 0,
        }
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize cache"""
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        self.max_memory_size = self.config.get('max_memory_size', 100)
        self.max_disk_size = self.config.get('max_disk_size', 1000)
        self.cache_ttl = self.config.get('ttl', 3600)
        self.policy = CachePolicy(self.config.get('policy', 'lru'))
        
        # Set cache directory
        cache_dir = self.config.get('cache_dir')
        if cache_dir:
            self.cache_dir = cache_dir
        else:
            # Default to man/cache directory
            self.cache_dir = os.path.join(
                os.path.dirname(__file__), 'cache'
            )
            
        # Create cache directory if it doesn't exist
        if self.enabled:
            os.makedirs(self.cache_dir, exist_ok=True)
            
        # Load existing cache stats
        await self._load_stats()
        
    async def get(self, key: str) -> Optional[Dict]:
        """Get cached man page"""
        if not self.enabled:
            return None
            
        # Check memory cache first
        if key in self.memory_cache:
            cache_entry = self.memory_cache[key]
            
            # Check if expired
            if self._is_expired(cache_entry):
                await self._remove(key)
                self.stats['misses'] += 1
                return None
                
            # Update access tracking
            self.access_times[key] = time.time()
            self.access_counts[key] = self.access_counts.get(key, 0) + 1
            self.stats['hits'] += 1
            
            return cache_entry['data']
            
        # Check disk cache
        disk_entry = await self._load_from_disk(key)
        if disk_entry:
            # Check if expired
            if self._is_expired(disk_entry):
                await self._remove_from_disk(key)
                self.stats['misses'] += 1
                return None
                
            # Add to memory cache
            await self._add_to_memory(key, disk_entry)
            self.stats['hits'] += 1
            
            return disk_entry['data']
            
        self.stats['misses'] += 1
        return None
        
    async def set(self, key: str, data: Dict) -> bool:
        """Cache a man page"""
        if not self.enabled:
            return False
            
        cache_entry = {
            'data': data,
            'timestamp': time.time(),
            'size': len(json.dumps(data)),
        }
        
        # Add to memory cache
        await self._add_to_memory(key, cache_entry)
        
        # Add to disk cache
        await self._save_to_disk(key, cache_entry)
        
        self.stats['size'] = len(self.memory_cache)
        return True
        
    async def remove(self, key: str) -> bool:
        """Remove a man page from cache"""
        if not self.enabled:
            return False
            
        success = True
        
        # Remove from memory
        if key in self.memory_cache:
            del self.memory_cache[key]
            if key in self.access_times:
                del self.access_times[key]
            if key in self.access_counts:
                del self.access_counts[key]
        else:
            success = False
            
        # Remove from disk
        await self._remove_from_disk(key)
        
        self.stats['size'] = len(self.memory_cache)
        return success
        
    async def clear(self) -> bool:
        """Clear all cache"""
        if not self.enabled:
            return False
            
        # Clear memory cache
        self.memory_cache.clear()
        self.access_times.clear()
        self.access_counts.clear()
        
        # Clear disk cache
        if os.path.exists(self.cache_dir):
            for filename in os.listdir(self.cache_dir):
                filepath = os.path.join(self.cache_dir, filename)
                try:
                    os.remove(filepath)
                except Exception:
                    pass
                    
        # Reset stats
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'size': 0,
        }
        
        return True
        
    async def _add_to_memory(self, key: str, cache_entry: Dict):
        """Add entry to memory cache with eviction policy"""
        # Check if we need to evict
        while len(self.memory_cache) >= self.max_memory_size:
            await self._evict()
            
        self.memory_cache[key] = cache_entry
        self.access_times[key] = time.time()
        self.access_counts[key] = 1
        
    async def _evict(self):
        """Evict entry based on policy"""
        if not self.memory_cache:
            return
            
        if self.policy == CachePolicy.LRU:
            # Least Recently Used
            key_to_evict = min(self.access_times.keys(), 
                              key=lambda k: self.access_times[k])
        elif self.policy == CachePolicy.LFU:
            # Least Frequently Used
            key_to_evict = min(self.access_counts.keys(),
                              key=lambda k: self.access_counts[k])
        else:  # FIFO
            # First In First Out (approximate by access time)
            key_to_evict = min(self.access_times.keys(),
                              key=lambda k: self.access_times[k])
            
        await self._remove(key_to_evict)
        self.stats['evictions'] += 1
        
    async def _save_to_disk(self, key: str, cache_entry: Dict):
        """Save entry to disk cache"""
        try:
            # Create filename from key
            filename = self._hash_key(key) + '.json'
            filepath = os.path.join(self.cache_dir, filename)
            
            # Check disk cache size
            if await self._get_disk_size() >= self.max_disk_size:
                await self._evict_from_disk()
                
            # Save to disk
            with open(filepath, 'w') as f:
                json.dump(cache_entry, f)
                
        except Exception:
            pass  # Fail silently on disk cache errors
            
    async def _load_from_disk(self, key: str) -> Optional[Dict]:
        """Load entry from disk cache"""
        try:
            filename = self._hash_key(key) + '.json'
            filepath = os.path.join(self.cache_dir, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
                    
        except Exception:
            pass
            
        return None
        
    async def _remove_from_disk(self, key: str):
        """Remove entry from disk cache"""
        try:
            filename = self._hash_key(key) + '.json'
            filepath = os.path.join(self.cache_dir, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                
        except Exception:
            pass
            
    async def _evict_from_disk(self):
        """Evict oldest entry from disk cache"""
        try:
            files = []
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.cache_dir, filename)
                    files.append((filepath, os.path.getmtime(filepath)))
                    
            if files:
                # Sort by modification time and remove oldest
                files.sort(key=lambda x: x[1])
                oldest_file = files[0][0]
                os.remove(oldest_file)
                self.stats['evictions'] += 1
                
        except Exception:
            pass
            
    def _is_expired(self, cache_entry: Dict) -> bool:
        """Check if cache entry is expired"""
        age = time.time() - cache_entry['timestamp']
        return age > self.cache_ttl
        
    def _hash_key(self, key: str) -> str:
        """Create hash from key for filename"""
        return hashlib.md5(key.encode()).hexdigest()
        
    async def _get_disk_size(self) -> int:
        """Get current disk cache size"""
        try:
            if os.path.exists(self.cache_dir):
                return len([f for f in os.listdir(self.cache_dir) if f.endswith('.json')])
        except Exception:
            pass
        return 0
        
    async def _load_stats(self):
        """Load cache statistics from disk"""
        try:
            stats_file = os.path.join(self.cache_dir, 'stats.json')
            if os.path.exists(stats_file):
                with open(stats_file, 'r') as f:
                    saved_stats = json.load(f)
                    self.stats.update(saved_stats)
        except Exception:
            pass
            
    async def _save_stats(self):
        """Save cache statistics to disk"""
        try:
            stats_file = os.path.join(self.cache_dir, 'stats.json')
            with open(stats_file, 'w') as f:
                json.dump(self.stats, f)
        except Exception:
            pass
            
    async def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        # Save stats before returning
        await self._save_stats()
        
        hit_rate = 0
        total_requests = self.stats['hits'] + self.stats['misses']
        if total_requests > 0:
            hit_rate = (self.stats['hits'] / total_requests) * 100
            
        return {
            'enabled': self.enabled,
            'memory_size': len(self.memory_cache),
            'max_memory_size': self.max_memory_size,
            'disk_size': await self._get_disk_size(),
            'max_disk_size': self.max_disk_size,
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'evictions': self.stats['evictions'],
            'hit_rate': f"{hit_rate:.2f}%",
            'policy': self.policy.value,
            'ttl': self.cache_ttl,
        }
        
    async def cleanup_expired(self) -> int:
        """Clean up expired cache entries"""
        if not self.enabled:
            return 0
            
        cleaned = 0
        
        # Clean memory cache
        keys_to_remove = []
        for key, entry in self.memory_cache.items():
            if self._is_expired(entry):
                keys_to_remove.append(key)
                
        for key in keys_to_remove:
            await self._remove(key)
            cleaned += 1
            
        # Clean disk cache
        try:
            if os.path.exists(self.cache_dir):
                for filename in os.listdir(self.cache_dir):
                    if filename.endswith('.json'):
                        filepath = os.path.join(self.cache_dir, filename)
                        try:
                            with open(filepath, 'r') as f:
                                entry = json.load(f)
                                if self._is_expired(entry):
                                    os.remove(filepath)
                                    cleaned += 1
                        except Exception:
                            pass
        except Exception:
            pass
            
        return cleaned
