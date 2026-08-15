"""
 ============================================================
  MODULE/PLUGIN NAME: ClipboardManager
  VERSION: 1.0.0
  MODULE CLASS: ClipboardManager
  DESCRIPTION:
       Clipboard and clipboard history management for TerminalX

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

import platform
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class ClipboardEntry:
    """Clipboard entry"""
    content: str
    timestamp: str
    size: int
    content_type: str = "text"


class ClipboardManager:
    """Clipboard manager with history"""
    
    def __init__(self, max_history: int = 100, logger: Optional[CleanLogger] = None):
        """
        Initialize clipboard manager
        
        Args:
            max_history: Maximum history size
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("ClipboardManager", LogLevel.INFO)
        self.max_history = max_history
        self.history: List[ClipboardEntry] = []
        self.current_content: Optional[str] = None
        
    def get_content(self) -> Optional[str]:
        """
        Get current clipboard content
        
        Returns:
            Clipboard content or None
        """
        try:
            if platform.system() == 'Windows':
                import win32clipboard
                win32clipboard.OpenClipboard()
                try:
                    content = win32clipboard.GetClipboardData()
                    self.current_content = content
                    return content
                finally:
                    win32clipboard.CloseClipboard()
                    
            elif platform.system() == 'Darwin':
                import subprocess
                result = subprocess.run(['pbpaste'], capture_output=True, text=True)
                content = result.stdout
                self.current_content = content
                return content
                
            elif platform.system() == 'Linux':
                import subprocess
                result = subprocess.run(['xclip', '-o', '-selection', 'clipboard'], capture_output=True, text=True)
                content = result.stdout
                self.current_content = content
                return content
                
        except Exception as e:
            self.logger.error(f"Failed to get clipboard content: {e}")
            
        return None
        
    def set_content(self, content: str) -> bool:
        """
        Set clipboard content
        
        Args:
            content: Content to set
            
        Returns:
            True if set successfully
        """
        try:
            if platform.system() == 'Windows':
                import win32clipboard
                win32clipboard.OpenClipboard()
                try:
                    win32clipboard.EmptyClipboard()
                    win32clipboard.SetClipboardText(content)
                    self.current_content = content
                    return True
                finally:
                    win32clipboard.CloseClipboard()
                    
            elif platform.system() == 'Darwin':
                import subprocess
                subprocess.run(['pbcopy'], input=content, text=True, capture_output=True)
                self.current_content = content
                return True
                
            elif platform.system() == 'Linux':
                import subprocess
                subprocess.run(['xclip', '-selection', 'clipboard'], input=content, text=True, capture_output=True)
                self.current_content = content
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to set clipboard content: {e}")
            
        return False
        
    def save_to_history(self, content: Optional[str] = None) -> bool:
        """
        Save content to history
        
        Args:
            content: Content to save (None for current)
            
        Returns:
            True if saved successfully
        """
        if content is None:
            content = self.get_content()
            
        if not content:
            return False
            
        # Check if already in history
        for entry in self.history:
            if entry.content == content:
                return False
                
        entry = ClipboardEntry(
            content=content,
            timestamp=datetime.now().isoformat(),
            size=len(content)
        )
        
        self.history.insert(0, entry)
        
        # Trim history if needed
        if len(self.history) > self.max_history:
            self.history = self.history[:self.max_history]
            
        self.logger.info("Saved to clipboard history")
        return True
        
    def get_history(self, limit: Optional[int] = None) -> List[ClipboardEntry]:
        """
        Get clipboard history
        
        Args:
            limit: Maximum entries to return
            
        Returns:
            List of clipboard entries
        """
        if limit:
            return self.history[:limit]
        return self.history.copy()
        
    def restore_from_history(self, index: int) -> bool:
        """
        Restore content from history
        
        Args:
            index: History index
            
        Returns:
            True if restored successfully
        """
        if index < 0 or index >= len(self.history):
            return False
            
        entry = self.history[index]
        return self.set_content(entry.content)
        
    def clear_history(self) -> None:
        """Clear clipboard history"""
        self.history.clear()
        self.logger.info("Cleared clipboard history")
        
    def search_history(self, query: str) -> List[ClipboardEntry]:
        """
        Search clipboard history
        
        Args:
            query: Search query
            
        Returns:
            List of matching entries
        """
        query = query.lower()
        results = []
        
        for entry in self.history:
            if query in entry.content.lower():
                results.append(entry)
                
        return results
        
    def delete_from_history(self, index: int) -> bool:
        """
        Delete entry from history
        
        Args:
            index: History index
            
        Returns:
            True if deleted successfully
        """
        if index < 0 or index >= len(self.history):
            return False
            
        del self.history[index]
        self.logger.info(f"Deleted history entry at index {index}")
        return True
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get clipboard manager statistics
        
        Returns:
            Statistics dictionary
        """
        total_size = sum(entry.size for entry in self.history)
        
        return {
            'history_size': len(self.history),
            'max_history': self.max_history,
            'total_size': total_size,
            'has_content': self.current_content is not None,
            'current_size': len(self.current_content) if self.current_content else 0
        }


# Global clipboard manager instance
clipboard_manager = ClipboardManager()
