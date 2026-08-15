"""
 ============================================================
  MODULE/PLUGIN NAME: GitHub
  VERSION: 1.0.0
  MODULE CLASS: GitHub
  DESCRIPTION:
       GitHub integration for TerminalX operations

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

import requests
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class GitHubRepo:
    """GitHub repository information"""
    name: str
    full_name: str
    description: str
    url: str
    stars: int
    forks: int
    language: str
    updated_at: str


@dataclass
class GitHubIssue:
    """GitHub issue information"""
    number: int
    title: str
    state: str
    url: str
    user: str
    created_at: str
    body: str


class GitHubClient:
    """GitHub API client"""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None, logger: Optional[CleanLogger] = None):
        """
        Initialize GitHub client
        
        Args:
            token: GitHub personal access token
            logger: Logger instance
        """
        self.token = token
        self.logger = logger or CleanLogger("GitHubClient", LogLevel.INFO)
        self.headers = {}
        if token:
            self.headers['Authorization'] = f'token {token}'
            
    def _request(self, endpoint: str, method: str = 'GET', data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make API request
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            data: Request data
            
        Returns:
            Response data or None
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                return None
                
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 204:
                return None
            else:
                self.logger.error(f"API request failed: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Request error: {e}")
            return None
            
    def get_user(self, username: str) -> Optional[Dict]:
        """
        Get user information
        
        Args:
            username: GitHub username
            
        Returns:
            User data or None
        """
        return self._request(f"/users/{username}")
        
    def get_repos(self, username: str, repo_type: str = 'all') -> List[GitHubRepo]:
        """
        Get user repositories
        
        Args:
            username: GitHub username
            repo_type: Repository type (all, owner, member)
            
        Returns:
            List of repositories
        """
        repos = []
        data = self._request(f"/users/{username}/repos?type={repo_type}")
        
        if data:
            for item in data:
                repos.append(GitHubRepo(
                    name=item['name'],
                    full_name=item['full_name'],
                    description=item.get('description', ''),
                    url=item['html_url'],
                    stars=item['stargazers_count'],
                    forks=item['forks_count'],
                    language=item.get('language', 'Unknown'),
                    updated_at=item['updated_at']
                ))
                
        return repos
        
    def get_repo(self, owner: str, repo: str) -> Optional[Dict]:
        """
        Get repository information
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Repository data or None
        """
        return self._request(f"/repos/{owner}/{repo}")
        
    def get_issues(self, owner: str, repo: str, state: str = 'open') -> List[GitHubIssue]:
        """
        Get repository issues
        
        Args:
            owner: Repository owner
            repo: Repository name
            state: Issue state (open, closed, all)
            
        Returns:
            List of issues
        """
        issues = []
        data = self._request(f"/repos/{owner}/{repo}/issues?state={state}")
        
        if data:
            for item in data:
                issues.append(GitHubIssue(
                    number=item['number'],
                    title=item['title'],
                    state=item['state'],
                    url=item['html_url'],
                    user=item['user']['login'],
                    created_at=item['created_at'],
                    body=item.get('body', '')
                ))
                
        return issues
        
    def create_issue(self, owner: str, repo: str, title: str, body: str = '') -> Optional[Dict]:
        """
        Create an issue
        
        Args:
            owner: Repository owner
            repo: Repository name
            title: Issue title
            body: Issue body
            
        Returns:
            Created issue data or None
        """
        return self._request(
            f"/repos/{owner}/{repo}/issues",
            method='POST',
            data={'title': title, 'body': body}
        )
        
    def create_repo(self, name: str, description: str = '', private: bool = False) -> Optional[Dict]:
        """
        Create a repository
        
        Args:
            name: Repository name
            description: Repository description
            private: Private repository
            
        Returns:
            Created repository data or None
        """
        return self._request(
            '/user/repos',
            method='POST',
            data={'name': name, 'description': description, 'private': private}
        )
        
    def fork_repo(self, owner: str, repo: str) -> Optional[Dict]:
        """
        Fork a repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Forked repository data or None
        """
        return self._request(
            f"/repos/{owner}/{repo}/forks",
            method='POST'
        )
        
    def search_repos(self, query: str, sort: str = 'stars', order: str = 'desc') -> List[GitHubRepo]:
        """
        Search repositories
        
        Args:
            query: Search query
            sort: Sort field (stars, forks, updated)
            order: Sort order (asc, desc)
            
        Returns:
            List of repositories
        """
        repos = []
        data = self._request(f"/search/repositories?q={query}&sort={sort}&order={order}")
        
        if data and 'items' in data:
            for item in data['items']:
                repos.append(GitHubRepo(
                    name=item['name'],
                    full_name=item['full_name'],
                    description=item.get('description', ''),
                    url=item['html_url'],
                    stars=item['stargazers_count'],
                    forks=item['forks_count'],
                    language=item.get('language', 'Unknown'),
                    updated_at=item['updated_at']
                ))
                
        return repos
        
    def get_commits(self, owner: str, repo: str, branch: str = 'main') -> List[Dict]:
        """
        Get repository commits
        
        Args:
            owner: Repository owner
            repo: Repository name
            branch: Branch name
            
        Returns:
            List of commits
        """
        data = self._request(f"/repos/{owner}/{repo}/commits?sha={branch}")
        return data if data else []
        
    def get_branches(self, owner: str, repo: str) -> List[Dict]:
        """
        Get repository branches
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            List of branches
        """
        data = self._request(f"/repos/{owner}/{repo}/branches")
        return data if data else []
        
    def get_readme(self, owner: str, repo: str) -> Optional[str]:
        """
        Get repository README
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            README content or None
        """
        data = self._request(f"/repos/{owner}/{repo}/readme")
        if data and 'content' in data:
            import base64
            return base64.b64decode(data['content']).decode()
        return None
        
    def get_stats(self) -> Dict[str, Any]:
        """
        Get client statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'authenticated': self.token is not None,
            'base_url': self.BASE_URL
        }


# Global GitHub client instance
github_client = GitHubClient()
