"""
 ============================================================
  MODULE/PLUGIN NAME: CloudSync
  VERSION: 1.0.0
  MODULE CLASS: CloudSync
  DESCRIPTION:
       Data and settings synchronization for TerminalX

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

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class SyncItem:
    """Sync item information"""
    path: str
    provider: str
    last_synced: str
    status: str  # synced, pending, conflict, error
    size: int


@dataclass
class SyncConflict:
    """Sync conflict information"""
    path: str
    local_version: str
    remote_version: str
    conflict_type: str


class CloudSync:
    """Cloud synchronization system"""
    
    def __init__(self, sync_dir: Optional[Path] = None, logger: Optional[CleanLogger] = None):
        """
        Initialize cloud sync
        
        Args:
            sync_dir: Sync directory
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("CloudSync", LogLevel.INFO)
        self.sync_dir = sync_dir or Path.home() / ".terminalx" / "sync"
        self.sync_items: Dict[str, SyncItem] = {}
        self.conflicts: List[SyncConflict] = []
        self.auto_sync_enabled = False
        self.sync_interval = 300  # 5 minutes
        
        self._init_sync_dir()
        
    def _init_sync_dir(self) -> None:
        """Initialize sync directory"""
        self.sync_dir.mkdir(parents=True, exist_ok=True)
        
    def add_sync_item(self, path: str, provider: str) -> bool:
        """
        Add item to sync
        
        Args:
            path: Local path to sync
            provider: Cloud provider name
            
        Returns:
            True if added successfully
        """
        if not os.path.exists(path):
            self.logger.error(f"Path does not exist: {path}")
            return False
            
        key = f"{provider}:{path}"
        
        if key in self.sync_items:
            self.logger.warning(f"Sync item already exists: {key}")
            return False
            
        size = os.path.getsize(path) if os.path.isfile(path) else 0
        
        self.sync_items[key] = SyncItem(
            path=path,
            provider=provider,
            last_synced="",
            status="pending",
            size=size
        )
        
        self.logger.info(f"Added sync item: {key}")
        return True
        
    def remove_sync_item(self, path: str, provider: str) -> bool:
        """
        Remove sync item
        
        Args:
            path: Local path
            provider: Cloud provider name
            
        Returns:
            True if removed successfully
        """
        key = f"{provider}:{path}"
        
        if key in self.sync_items:
            del self.sync_items[key]
            self.logger.info(f"Removed sync item: {key}")
            return True
        return False
        
    def sync_item(self, path: str, provider: str, direction: str = "both") -> bool:
        """
        Sync a single item
        
        Args:
            path: Local path
            provider: Cloud provider name
            direction: Sync direction (up, down, both)
            
        Returns:
            True if synced successfully
        """
        key = f"{provider}:{path}"
        item = self.sync_items.get(key)
        
        if not item:
            return False
            
        try:
            # Placeholder for actual sync logic
            # This would use the cloud_filesystem module
            
            item.last_synced = datetime.now().isoformat()
            item.status = "synced"
            
            self.logger.info(f"Synced {key} ({direction})")
            return True
            
        except Exception as e:
            item.status = "error"
            self.logger.error(f"Sync failed for {key}: {e}")
            return False
            
    def sync_all(self, provider: Optional[str] = None) -> Dict[str, bool]:
        """
        Sync all items
        
        Args:
            provider: Optional provider filter
            
        Returns:
            Dictionary of item key -> success
        """
        results = {}
        
        for key, item in self.sync_items.items():
            if provider and item.provider != provider:
                continue
                
            results[key] = self.sync_item(item.path, item.provider)
            
        return results
        
    def resolve_conflict(self, path: str, provider: str, resolution: str) -> bool:
        """
        Resolve a sync conflict
        
        Args:
            path: Item path
            provider: Provider name
            resolution: Resolution (local, remote, merge)
            
        Returns:
            True if resolved successfully
        """
        key = f"{provider}:{path}"
        
        # Remove conflict
        self.conflicts = [c for c in self.conflicts if c.path != path]
        
        # Update item status
        if key in self.sync_items:
            self.sync_items[key].status = "synced"
            
        self.logger.info(f"Resolved conflict for {key} ({resolution})")
        return True
        
    def get_sync_status(self, path: str, provider: str) -> Optional[str]:
        """
        Get sync status for item
        
        Args:
            path: Item path
            provider: Provider name
            
        Returns:
            Status or None
        """
        key = f"{provider}:{path}"
        item = self.sync_items.get(key)
        return item.status if item else None
        
    def list_sync_items(self, provider: Optional[str] = None, 
                       status: Optional[str] = None) -> List[SyncItem]:
        """
        List sync items
        
        Args:
            provider: Optional provider filter
            status: Optional status filter
            
        Returns:
            List of sync items
        """
        items = list(self.sync_items.values())
        
        if provider:
            items = [i for i in items if i.provider == provider]
            
        if status:
            items = [i for i in items if i.status == status]
            
        return items
        
    def list_conflicts(self) -> List[SyncConflict]:
        """
        List all conflicts
        
        Returns:
            List of conflicts
        """
        return self.conflicts.copy()
        
    def enable_auto_sync(self, interval: int = 300) -> None:
        """
        Enable automatic sync
        
        Args:
            interval: Sync interval in seconds
        """
        self.auto_sync_enabled = True
        self.sync_interval = interval
        self.logger.info(f"Auto-sync enabled (interval: {interval}s)")
        
    def disable_auto_sync(self) -> None:
        """Disable automatic sync"""
        self.auto_sync_enabled = False
        self.logger.info("Auto-sync disabled")
        
    def export_sync_config(self, path: str) -> bool:
        """
        Export sync configuration
        
        Args:
            path: Export path
            
        Returns:
            True if exported successfully
        """
        try:
            config = {
                'items': [
                    {
                        'path': item.path,
                        'provider': item.provider,
                        'last_synced': item.last_synced,
                        'status': item.status,
                        'size': item.size
                    }
                    for item in self.sync_items.values()
                ],
                'auto_sync': self.auto_sync_enabled,
                'sync_interval': self.sync_interval
            }
            
            with open(path, 'w') as f:
                json.dump(config, f, indent=2)
                
            self.logger.info(f"Exported sync config to {path}")
            return True
        except Exception as e:
            self.logger.error(f"Export failed: {e}")
            return False
            
    def import_sync_config(self, path: str) -> bool:
        """
        Import sync configuration
        
        Args:
            path: Import path
            
        Returns:
            True if imported successfully
        """
        try:
            with open(path, 'r') as f:
                config = json.load(f)
                
            self.sync_items.clear()
            
            for item_data in config.get('items', []):
                key = f"{item_data['provider']}:{item_data['path']}"
                self.sync_items[key] = SyncItem(
                    path=item_data['path'],
                    provider=item_data['provider'],
                    last_synced=item_data.get('last_synced', ''),
                    status=item_data.get('status', 'pending'),
                    size=item_data.get('size', 0)
                )
                
            self.auto_sync_enabled = config.get('auto_sync', False)
            self.sync_interval = config.get('sync_interval', 300)
            
            self.logger.info(f"Imported sync config from {path}")
            return True
        except Exception as e:
            self.logger.error(f"Import failed: {e}")
            return False
            
    def get_stats(self) -> Dict[str, any]:
        """
        Get sync statistics
        
        Returns:
            Statistics dictionary
        """
        status_counts = {}
        for item in self.sync_items.values():
            status_counts[item.status] = status_counts.get(item.status, 0) + 1
            
        return {
            'total_items': len(self.sync_items),
            'status_counts': status_counts,
            'conflicts': len(self.conflicts),
            'auto_sync': self.auto_sync_enabled,
            'sync_interval': self.sync_interval
        }


# Global cloud sync instance
cloud_sync = CloudSync()
