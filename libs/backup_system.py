"""
 ============================================================
  MODULE/PLUGIN NAME: BackupSystem
  VERSION: 1.0.0
  MODULE CLASS: BackupSystem
  DESCRIPTION:
       Data and configuration backup system for TerminalX

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
import shutil
import json
import gzip
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class Backup:
    """Backup information"""
    name: str
    path: str
    size: int
    created_at: str
    compressed: bool = False
    checksum: str = ""


@dataclass
class BackupSchedule:
    """Backup schedule"""
    name: str
    source: str
    destination: str
    frequency: str  # daily, weekly, monthly
    enabled: bool = True
    last_run: Optional[str] = None


class BackupSystem:
    """Backup system for data and configuration"""
    
    def __init__(self, backup_dir: Optional[Path] = None, logger: Optional[CleanLogger] = None):
        """
        Initialize backup system
        
        Args:
            backup_dir: Backup directory
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("BackupSystem", LogLevel.INFO)
        self.backup_dir = backup_dir or Path.home() / ".terminalx" / "backups"
        self.backups: Dict[str, Backup] = {}
        self.schedules: Dict[str, BackupSchedule] = {}
        
        self._init_backup_dir()
        
    def _init_backup_dir(self) -> None:
        """Initialize backup directory"""
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
    def create_backup(self, name: str, source: str, compress: bool = True) -> Optional[Backup]:
        """
        Create a backup
        
        Args:
            name: Backup name
            source: Source path
            compress: Compress backup
            
        Returns:
            Backup info or None
        """
        source_path = Path(source)
        
        if not source_path.exists():
            self.logger.error(f"Source path does not exist: {source}")
            return None
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{name}_{timestamp}"
            backup_path = self.backup_dir / backup_name
            
            if compress:
                backup_path = backup_path.with_suffix('.tar.gz')
                self._create_compressed_backup(source_path, backup_path)
            else:
                backup_path.mkdir(parents=True, exist_ok=True)
                if source_path.is_dir():
                    shutil.copytree(source_path, backup_path / source_path.name)
                else:
                    shutil.copy2(source_path, backup_path)
                    
            # Calculate size
            size = self._get_directory_size(backup_path)
            
            # Calculate checksum
            checksum = self._calculate_checksum(backup_path)
            
            backup = Backup(
                name=backup_name,
                path=str(backup_path),
                size=size,
                created_at=datetime.now().isoformat(),
                compressed=compress,
                checksum=checksum
            )
            
            self.backups[backup_name] = backup
            self.logger.info(f"Created backup: {backup_name}")
            return backup
            
        except Exception as e:
            self.logger.error(f"Backup creation failed: {e}")
            return None
            
    def _create_compressed_backup(self, source: Path, destination: Path) -> None:
        """
        Create compressed backup
        
        Args:
            source: Source path
            destination: Destination path
        """
        if source.is_dir():
            shutil.make_archive(str(destination.with_suffix('')), 'gztar', str(source))
        else:
            with open(destination, 'wb') as f_out:
                with open(source, 'rb') as f_in:
                    f_out.write(gzip.compress(f_in.read()))
                    
    def restore_backup(self, name: str, destination: str) -> bool:
        """
        Restore a backup
        
        Args:
            name: Backup name
            destination: Destination path
            
        Returns:
            True if restored successfully
        """
        backup = self.backups.get(name)
        if not backup:
            self.logger.error(f"Backup {name} not found")
            return False
            
        backup_path = Path(backup.path)
        
        if not backup_path.exists():
            self.logger.error(f"Backup file does not exist: {backup.path}")
            return False
            
        try:
            dest_path = Path(destination)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            if backup.compressed:
                if backup_path.suffix == '.gz':
                    shutil.unpack_archive(str(backup_path), str(dest_path.parent))
                else:
                    with open(backup_path, 'rb') as f_in:
                        with open(dest_path, 'wb') as f_out:
                            f_out.write(gzip.decompress(f_in.read()))
            else:
                if backup_path.is_dir():
                    shutil.copytree(backup_path, dest_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(backup_path, dest_path)
                    
            self.logger.info(f"Restored backup: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Backup restore failed: {e}")
            return False
            
    def delete_backup(self, name: str) -> bool:
        """
        Delete a backup
        
        Args:
            name: Backup name
            
        Returns:
            True if deleted successfully
        """
        backup = self.backups.get(name)
        if not backup:
            return False
            
        try:
            backup_path = Path(backup.path)
            
            if backup_path.is_dir():
                shutil.rmtree(backup_path)
            else:
                backup_path.unlink()
                
            del self.backups[name]
            self.logger.info(f"Deleted backup: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Backup deletion failed: {e}")
            return False
            
    def list_backups(self) -> List[Backup]:
        """
        List all backups
        
        Returns:
            List of backups
        """
        return list(self.backups.values())
        
    def get_backup(self, name: str) -> Optional[Backup]:
        """
        Get backup information
        
        Args:
            name: Backup name
            
        Returns:
            Backup or None
        """
        return self.backups.get(name)
        
    def create_schedule(self, name: str, source: str, destination: str, 
                       frequency: str = "daily") -> bool:
        """
        Create backup schedule
        
        Args:
            name: Schedule name
            source: Source path
            destination: Destination path
            frequency: Backup frequency
            
        Returns:
            True if created successfully
        """
        if name in self.schedules:
            self.logger.warning(f"Schedule {name} already exists")
            return False
            
        self.schedules[name] = BackupSchedule(
            name=name,
            source=source,
            destination=destination,
            frequency=frequency
        )
        
        self.logger.info(f"Created schedule: {name}")
        return True
        
    def delete_schedule(self, name: str) -> bool:
        """
        Delete backup schedule
        
        Args:
            name: Schedule name
            
        Returns:
            True if deleted successfully
        """
        if name in self.schedules:
            del self.schedules[name]
            self.logger.info(f"Deleted schedule: {name}")
            return True
        return False
        
    def run_schedule(self, name: str) -> bool:
        """
        Run a scheduled backup
        
        Args:
            name: Schedule name
            
        Returns:
            True if run successfully
        """
        schedule = self.schedules.get(name)
        if not schedule:
            return False
            
        if not schedule.enabled:
            self.logger.warning(f"Schedule {name} is disabled")
            return False
            
        backup = self.create_backup(name, schedule.source)
        
        if backup:
            schedule.last_run = datetime.now().isoformat()
            return True
            
        return False
        
    def list_schedules(self) -> List[BackupSchedule]:
        """
        List all schedules
        
        Returns:
            List of schedules
        """
        return list(self.schedules.values())
        
    def _get_directory_size(self, path: Path) -> int:
        """
        Get directory size
        
        Args:
            path: Directory path
            
        Returns:
            Size in bytes
        """
        total = 0
        
        if path.is_file():
            return path.stat().st_size
            
        for item in path.rglob('*'):
            if item.is_file():
                total += item.stat().st_size
                
        return total
        
    def _calculate_checksum(self, path: Path) -> str:
        """
        Calculate checksum for backup
        
        Args:
            path: Path to calculate
            
        Returns:
            Checksum string
        """
        import hashlib
        hash_obj = hashlib.md5()
        
        if path.is_file():
            with open(path, 'rb') as f:
                hash_obj.update(f.read())
        else:
            for item in sorted(path.rglob('*')):
                if item.is_file():
                    with open(item, 'rb') as f:
                        hash_obj.update(f.read())
                        
        return hash_obj.hexdigest()
        
    def verify_backup(self, name: str) -> bool:
        """
        Verify backup integrity
        
        Args:
            name: Backup name
            
        Returns:
            True if backup is valid
        """
        backup = self.backups.get(name)
        if not backup:
            return False
            
        backup_path = Path(backup.path)
        
        if not backup_path.exists():
            return False
            
        current_checksum = self._calculate_checksum(backup_path)
        return current_checksum == backup.checksum
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get backup system statistics
        
        Returns:
            Statistics dictionary
        """
        total_size = sum(b.size for b in self.backups.values())
        
        return {
            'total_backups': len(self.backups),
            'total_size': total_size,
            'schedules': len(self.schedules),
            'enabled_schedules': sum(1 for s in self.schedules.values() if s.enabled),
            'backup_dir': str(self.backup_dir)
        }


# Global backup system instance
backup_system = BackupSystem()
