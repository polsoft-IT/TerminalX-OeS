"""
 ============================================================
  MODULE/PLUGIN NAME: FileManager
  VERSION: 1.0.0
  MODULE CLASS: FileManager
  DESCRIPTION:
       Advanced file management for TerminalX operations

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
import hashlib
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from libs.clean_logger import CleanLogger, LogLevel


class FileType(Enum):
    """File types"""
    FILE = "file"
    DIRECTORY = "directory"
    SYMLINK = "symlink"
    UNKNOWN = "unknown"


@dataclass
class FileInfo:
    """File information"""
    path: str
    name: str
    size: int
    file_type: FileType
    modified: float
    created: float
    permissions: str
    is_hidden: bool = False


class FileManager:
    """Advanced file management system"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize file manager
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("FileManager", LogLevel.INFO)
        self.watchers: Dict[str, Callable] = {}
        
    def get_info(self, path: str) -> Optional[FileInfo]:
        """
        Get file information
        
        Args:
            path: File path
            
        Returns:
            File info or None
        """
        try:
            path_obj = Path(path)
            stat = path_obj.stat()
            
            # Determine file type
            if path_obj.is_symlink():
                file_type = FileType.SYMLINK
            elif path_obj.is_dir():
                file_type = FileType.DIRECTORY
            elif path_obj.is_file():
                file_type = FileType.FILE
            else:
                file_type = FileType.UNKNOWN
                
            # Check if hidden
            is_hidden = path_obj.name.startswith('.')
            
            # Get permissions
            permissions = oct(stat.st_mode)[-3:]
            
            return FileInfo(
                path=str(path_obj.absolute()),
                name=path_obj.name,
                size=stat.st_size,
                file_type=file_type,
                modified=stat.st_mtime,
                created=stat.st_ctime,
                permissions=permissions,
                is_hidden=is_hidden
            )
        except Exception as e:
            self.logger.error(f"Failed to get file info: {e}")
            return None
            
    def list_directory(self, path: str = '.', include_hidden: bool = False, 
                      recursive: bool = False) -> List[FileInfo]:
        """
        List directory contents
        
        Args:
            path: Directory path
            include_hidden: Include hidden files
            recursive: Recursive listing
            
        Returns:
            List of file info
        """
        files = []
        
        try:
            path_obj = Path(path)
            
            if recursive:
                for item in path_obj.rglob('*'):
                    info = self.get_info(str(item))
                    if info:
                        if include_hidden or not info.is_hidden:
                            files.append(info)
            else:
                for item in path_obj.iterdir():
                    info = self.get_info(str(item))
                    if info:
                        if include_hidden or not info.is_hidden:
                            files.append(info)
                            
        except Exception as e:
            self.logger.error(f"Failed to list directory: {e}")
            
        return files
        
    def search(self, path: str, pattern: str, case_sensitive: bool = False) -> List[FileInfo]:
        """
        Search for files by pattern
        
        Args:
            path: Search path
            pattern: Search pattern
            case_sensitive: Case sensitive search
            
        Returns:
            List of matching files
        """
        results = []
        
        try:
            path_obj = Path(path)
            
            for item in path_obj.rglob('*'):
                if case_sensitive:
                    match = pattern in item.name
                else:
                    match = pattern.lower() in item.name.lower()
                    
                if match:
                    info = self.get_info(str(item))
                    if info:
                        results.append(info)
                        
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            
        return results
        
    def search_content(self, path: str, text: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """
        Search for text in files
        
        Args:
            path: Search path
            text: Text to search
            case_sensitive: Case sensitive search
            
        Returns:
            List of matches with file and line info
        """
        results = []
        
        try:
            path_obj = Path(path)
            
            for file_path in path_obj.rglob('*'):
                if file_path.is_file():
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            for line_num, line in enumerate(f, 1):
                                if case_sensitive:
                                    match = text in line
                                else:
                                    match = text.lower() in line.lower()
                                    
                                if match:
                                    results.append({
                                        'file': str(file_path),
                                        'line': line_num,
                                        'content': line.strip()
                                    })
                    except Exception:
                        pass
                        
        except Exception as e:
            self.logger.error(f"Content search failed: {e}")
            
        return results
        
    def copy(self, source: str, destination: str, preserve_metadata: bool = True) -> bool:
        """
        Copy file or directory
        
        Args:
            source: Source path
            destination: Destination path
            preserve_metadata: Preserve file metadata
            
        Returns:
            True if copied successfully
        """
        try:
            source_path = Path(source)
            dest_path = Path(destination)
            
            if preserve_metadata:
                if source_path.is_dir():
                    shutil.copytree(source, destination)
                else:
                    shutil.copy2(source, destination)
            else:
                if source_path.is_dir():
                    shutil.copytree(source, destination, copy_function=shutil.copy)
                else:
                    shutil.copy(source, destination)
                    
            self.logger.info(f"Copied {source} to {destination}")
            return True
        except Exception as e:
            self.logger.error(f"Copy failed: {e}")
            return False
            
    def move(self, source: str, destination: str) -> bool:
        """
        Move file or directory
        
        Args:
            source: Source path
            destination: Destination path
            
        Returns:
            True if moved successfully
        """
        try:
            shutil.move(source, destination)
            self.logger.info(f"Moved {source} to {destination}")
            return True
        except Exception as e:
            self.logger.error(f"Move failed: {e}")
            return False
            
    def delete(self, path: str, force: bool = False) -> bool:
        """
        Delete file or directory
        
        Args:
            path: Path to delete
            force: Force deletion
            
        Returns:
            True if deleted successfully
        """
        try:
            path_obj = Path(path)
            
            if path_obj.is_dir():
                if force:
                    shutil.rmtree(path)
                else:
                    shutil.rmdir(path)
            else:
                path_obj.unlink()
                
            self.logger.info(f"Deleted {path}")
            return True
        except Exception as e:
            self.logger.error(f"Delete failed: {e}")
            return False
            
    def create_directory(self, path: str, parents: bool = True) -> bool:
        """
        Create directory
        
        Args:
            path: Directory path
            parents: Create parent directories
            
        Returns:
            True if created successfully
        """
        try:
            Path(path).mkdir(parents=parents, exist_ok=True)
            self.logger.info(f"Created directory: {path}")
            return True
        except Exception as e:
            self.logger.error(f"Directory creation failed: {e}")
            return False
            
    def create_file(self, path: str, content: str = '') -> bool:
        """
        Create file
        
        Args:
            path: File path
            content: Initial content
            
        Returns:
            True if created successfully
        """
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            self.logger.info(f"Created file: {path}")
            return True
        except Exception as e:
            self.logger.error(f"File creation failed: {e}")
            return False
            
    def get_size(self, path: str) -> int:
        """
        Get size of file or directory
        
        Args:
            path: Path
            
        Returns:
            Size in bytes
        """
        try:
            path_obj = Path(path)
            
            if path_obj.is_file():
                return path_obj.stat().st_size
            elif path_obj.is_dir():
                total = 0
                for item in path_obj.rglob('*'):
                    if item.is_file():
                        total += item.stat().st_size
                return total
        except Exception as e:
            self.logger.error(f"Size calculation failed: {e}")
            
        return 0
        
    def get_disk_usage(self, path: str = '.') -> Dict[str, int]:
        """
        Get disk usage
        
        Args:
            path: Path to check
            
        Returns:
            Dictionary with total, used, free
        """
        try:
            usage = shutil.disk_usage(path)
            return {
                'total': usage.total,
                'used': usage.used,
                'free': usage.free
            }
        except Exception as e:
            self.logger.error(f"Disk usage check failed: {e}")
            return {'total': 0, 'used': 0, 'free': 0}
            
    def watch(self, path: str, callback: Callable) -> bool:
        """
        Watch directory for changes
        
        Args:
            path: Path to watch
            callback: Callback function for changes
            
        Returns:
            True if watching started
        """
        self.watchers[path] = callback
        self.logger.info(f"Watching: {path}")
        return True
        
    def unwatch(self, path: str) -> bool:
        """
        Stop watching directory
        
        Args:
            path: Path to unwatch
            
        Returns:
            True if unwatched successfully
        """
        if path in self.watchers:
            del self.watchers[path]
            self.logger.info(f"Stopped watching: {path}")
            return True
        return False
        
    def get_stats(self) -> Dict[str, Any]:
        """
        Get file manager statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'watchers': len(self.watchers)
        }


# Global file manager instance
file_manager = FileManager()
