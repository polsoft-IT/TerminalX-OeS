"""
 ============================================================
  MODULE/PLUGIN NAME: GitIntegration
  VERSION: 1.0.0
  MODULE CLASS: GitIntegration
  DESCRIPTION:
       Git support for TerminalX operations

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

import subprocess
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from libs.clean_logger import CleanLogger, LogLevel


class GitStatus(Enum):
    """Git status"""
    CLEAN = "clean"
    MODIFIED = "modified"
    ADDED = "added"
    DELETED = "deleted"
    UNTRACKED = "untracked"
    CONFLICT = "conflict"


@dataclass
class GitCommit:
    """Git commit information"""
    hash: str
    author: str
    date: str
    message: str


@dataclass
class GitBranch:
    """Git branch information"""
    name: str
    is_current: bool


@dataclass
class GitFileStatus:
    """Git file status"""
    path: str
    status: GitStatus


class GitManager:
    """Git integration manager"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize Git manager
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("GitManager", LogLevel.INFO)
        
    def _run_git(self, args: List[str], cwd: Optional[str] = None) -> Tuple[bool, str]:
        """
        Run git command
        
        Args:
            args: Git arguments
            cwd: Working directory
            
        Returns:
            Tuple of (success, output)
        """
        try:
            result = subprocess.run(
                ['git'] + args,
                capture_output=True,
                text=True,
                cwd=cwd
            )
            
            if result.returncode == 0:
                return True, result.stdout.strip()
            else:
                return False, result.stderr.strip()
                
        except FileNotFoundError:
            return False, "Git not found"
        except Exception as e:
            return False, str(e)
            
    def is_repo(self, path: str = '.') -> bool:
        """
        Check if directory is a git repository
        
        Args:
            path: Directory path
            
        Returns:
            True if git repository
        """
        success, _ = self._run_git(['rev-parse', '--git-dir'], cwd=path)
        return success
        
    def init(self, path: str = '.') -> bool:
        """
        Initialize git repository
        
        Args:
            path: Directory path
            
        Returns:
            True if initialized successfully
        """
        success, output = self._run_git(['init'], cwd=path)
        if success:
            self.logger.info(f"Initialized git repository in {path}")
        else:
            self.logger.error(f"Failed to initialize: {output}")
        return success
        
    def clone(self, url: str, destination: str) -> bool:
        """
        Clone repository
        
        Args:
            url: Repository URL
            destination: Destination path
            
        Returns:
            True if cloned successfully
        """
        success, output = self._run_git(['clone', url, destination])
        if success:
            self.logger.info(f"Cloned {url} to {destination}")
        else:
            self.logger.error(f"Clone failed: {output}")
        return success
        
    def status(self, path: str = '.') -> List[GitFileStatus]:
        """
        Get git status
        
        Args:
            path: Repository path
            
        Returns:
            List of file statuses
        """
        statuses = []
        success, output = self._run_git(['status', '--porcelain'], cwd=path)
        
        if success:
            for line in output.split('\n'):
                if line:
                    status_code = line[:2]
                    file_path = line[3:]
                    
                    if status_code == 'M ':
                        status = GitStatus.MODIFIED
                    elif status_code == 'M':
                        status = GitStatus.MODIFIED
                    elif status_code == 'A ':
                        status = GitStatus.ADDED
                    elif status_code == 'D ':
                        status = GitStatus.DELETED
                    elif status_code == '??':
                        status = GitStatus.UNTRACKED
                    elif 'U' in status_code:
                        status = GitStatus.CONFLICT
                    else:
                        status = GitStatus.CLEAN
                        
                    statuses.append(GitFileStatus(path=file_path, status=status))
                    
        return statuses
        
    def add(self, files: List[str], path: str = '.') -> bool:
        """
        Add files to staging
        
        Args:
            files: List of files to add
            path: Repository path
            
        Returns:
            True if added successfully
        """
        success, output = self._run_git(['add'] + files, cwd=path)
        if success:
            self.logger.info(f"Added files: {files}")
        else:
            self.logger.error(f"Add failed: {output}")
        return success
        
    def commit(self, message: str, path: str = '.') -> bool:
        """
        Commit changes
        
        Args:
            message: Commit message
            path: Repository path
            
        Returns:
            True if committed successfully
        """
        success, output = self._run_git(['commit', '-m', message], cwd=path)
        if success:
            self.logger.info(f"Committed: {message}")
        else:
            self.logger.error(f"Commit failed: {output}")
        return success
        
    def push(self, remote: str = 'origin', branch: str = 'main', path: str = '.') -> bool:
        """
        Push changes
        
        Args:
            remote: Remote name
            branch: Branch name
            path: Repository path
            
        Returns:
            True if pushed successfully
        """
        success, output = self._run_git(['push', remote, branch], cwd=path)
        if success:
            self.logger.info(f"Pushed to {remote}/{branch}")
        else:
            self.logger.error(f"Push failed: {output}")
        return success
        
    def pull(self, remote: str = 'origin', branch: str = 'main', path: str = '.') -> bool:
        """
        Pull changes
        
        Args:
            remote: Remote name
            branch: Branch name
            path: Repository path
            
        Returns:
            True if pulled successfully
        """
        success, output = self._run_git(['pull', remote, branch], cwd=path)
        if success:
            self.logger.info(f"Pulled from {remote}/{branch}")
        else:
            self.logger.error(f"Pull failed: {output}")
        return success
        
    def branch(self, name: Optional[str] = None, path: str = '.') -> List[GitBranch]:
        """
        List or create branches
        
        Args:
            name: Branch name (None to list)
            path: Repository path
            
        Returns:
            List of branches
        """
        if name:
            success, output = self._run_git(['branch', name], cwd=path)
            if success:
                self.logger.info(f"Created branch: {name}")
            return []
            
        branches = []
        success, output = self._run_git(['branch', '-a'], cwd=path)
        
        if success:
            current = self.get_current_branch(path)
            for line in output.split('\n'):
                if line.strip():
                    branch_name = line.strip().replace('* ', '').replace('remotes/', '')
                    is_current = branch_name == current
                    branches.append(GitBranch(name=branch_name, is_current=is_current))
                    
        return branches
        
    def get_current_branch(self, path: str = '.') -> str:
        """
        Get current branch name
        
        Args:
            path: Repository path
            
        Returns:
            Branch name
        """
        success, output = self._run_git(['branch', '--show-current'], cwd=path)
        return output if success else 'HEAD'
        
    def checkout(self, branch: str, path: str = '.') -> bool:
        """
        Checkout branch
        
        Args:
            branch: Branch name
            path: Repository path
            
        Returns:
            True if checked out successfully
        """
        success, output = self._run_git(['checkout', branch], cwd=path)
        if success:
            self.logger.info(f"Checked out: {branch}")
        else:
            self.logger.error(f"Checkout failed: {output}")
        return success
        
    def log(self, path: str = '.', limit: int = 10) -> List[GitCommit]:
        """
        Get commit log
        
        Args:
            path: Repository path
            limit: Number of commits
            
        Returns:
            List of commits
        """
        commits = []
        success, output = self._run_git(['log', '-n', str(limit), '--pretty=format:%H|%an|%ai|%s'], cwd=path)
        
        if success:
            for line in output.split('\n'):
                if line:
                    parts = line.split('|', 3)
                    if len(parts) == 4:
                        commits.append(GitCommit(
                            hash=parts[0],
                            author=parts[1],
                            date=parts[2],
                            message=parts[3]
                        ))
                        
        return commits
        
    def diff(self, path: str = '.', file: Optional[str] = None) -> str:
        """
        Get diff
        
        Args:
            path: Repository path
            file: Specific file (None for all)
            
        Returns:
            Diff output
        """
        args = ['diff']
        if file:
            args.append(file)
            
        success, output = self._run_git(args, cwd=path)
        return output if success else ""
        
    def merge(self, branch: str, path: str = '.') -> bool:
        """
        Merge branch
        
        Args:
            branch: Branch to merge
            path: Repository path
            
        Returns:
            True if merged successfully
        """
        success, output = self._run_git(['merge', branch], cwd=path)
        if success:
            self.logger.info(f"Merged branch: {branch}")
        else:
            self.logger.error(f"Merge failed: {output}")
        return success
        
    def remote_add(self, name: str, url: str, path: str = '.') -> bool:
        """
        Add remote
        
        Args:
            name: Remote name
            url: Remote URL
            path: Repository path
            
        Returns:
            True if added successfully
        """
        success, output = self._run_git(['remote', 'add', name, url], cwd=path)
        if success:
            self.logger.info(f"Added remote: {name}")
        else:
            self.logger.error(f"Remote add failed: {output}")
        return success
        
    def get_remotes(self, path: str = '.') -> Dict[str, str]:
        """
        Get remotes
        
        Args:
            path: Repository path
            
        Returns:
            Dictionary of remote name -> URL
        """
        remotes = {}
        success, output = self._run_git(['remote', '-v'], cwd=path)
        
        if success:
            for line in output.split('\n'):
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        name = parts[0]
                        url = parts[1]
                        remotes[name] = url
                        
        return remotes
        
    def stash(self, message: str = '', path: str = '.') -> bool:
        """
        Stash changes
        
        Args:
            message: Stash message
            path: Repository path
            
        Returns:
            True if stashed successfully
        """
        args = ['stash']
        if_message = ['push', '-m', message] if message else ['push']
        args.extend(if_message)
        
        success, output = self._run_git(args, cwd=path)
        if success:
            self.logger.info("Stashed changes")
        else:
            self.logger.error(f"Stash failed: {output}")
        return success
        
    def stash_pop(self, path: str = '.') -> bool:
        """
        Pop stashed changes
        
        Args:
            path: Repository path
            
        Returns:
            True if popped successfully
        """
        success, output = self._run_git(['stash', 'pop'], cwd=path)
        if success:
            self.logger.info("Popped stash")
        else:
            self.logger.error(f"Stash pop failed: {output}")
        return success
        
    def get_stats(self, path: str = '.') -> Dict[str, any]:
        """
        Get repository statistics
        
        Args:
            path: Repository path
            
        Returns:
            Statistics dictionary
        """
        if not self.is_repo(path):
            return {'is_repo': False}
            
        return {
            'is_repo': True,
            'current_branch': self.get_current_branch(path),
            'remotes': len(self.get_remotes(path)),
            'branches': len(self.branch(path=path)),
            'status': len(self.status(path))
        }


# Global git manager instance
git_manager = GitManager()
