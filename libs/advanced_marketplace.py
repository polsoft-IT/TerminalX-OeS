"""
 ============================================================
  MODULE/PLUGIN NAME: AdvancedMarketplace
  VERSION: 1.0.0
  MODULE CLASS: AdvancedMarketplace
  DESCRIPTION:
       Advanced module and plugin store for TerminalX

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
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from libs.clean_logger import CleanLogger, LogLevel


class PackageStatus(Enum):
    """Package status"""
    AVAILABLE = "available"
    INSTALLED = "installed"
    OUTDATED = "outdated"
    INCOMPATIBLE = "incompatible"


@dataclass
class Package:
    """Package information"""
    name: str
    version: str
    description: str
    author: str
    downloads: int
    rating: float
    status: PackageStatus
    dependencies: List[str]
    size: int


@dataclass
class Review:
    """Package review"""
    author: str
    rating: int
    comment: str
    date: str


class AdvancedMarketplace:
    """Advanced marketplace for modules and plugins"""
    
    def __init__(self, api_url: str = "https://api.terminalx.marketplace", 
                 logger: Optional[CleanLogger] = None):
        """
        Initialize marketplace
        
        Args:
            api_url: Marketplace API URL
            logger: Logger instance
        """
        self.api_url = api_url
        self.logger = logger or CleanLogger("AdvancedMarketplace", LogLevel.INFO)
        self.installed_packages: Dict[str, Package] = {}
        self.cache: Dict[str, Any] = {}
        
    def search_packages(self, query: str, category: Optional[str] = None) -> List[Package]:
        """
        Search for packages
        
        Args:
            query: Search query
            category: Optional category filter
            
        Returns:
            List of packages
        """
        try:
            params = {'q': query}
            if category:
                params['category'] = category
                
            response = requests.get(f"{self.api_url}/search", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                packages = []
                
                for item in data.get('packages', []):
                    packages.append(Package(
                        name=item['name'],
                        version=item['version'],
                        description=item['description'],
                        author=item['author'],
                        downloads=item.get('downloads', 0),
                        rating=item.get('rating', 0.0),
                        status=PackageStatus.AVAILABLE,
                        dependencies=item.get('dependencies', []),
                        size=item.get('size', 0)
                    ))
                    
                return packages
                
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            
        return []
        
    def get_package(self, name: str) -> Optional[Package]:
        """
        Get package information
        
        Args:
            name: Package name
            
        Returns:
            Package or None
        """
        try:
            response = requests.get(f"{self.api_url}/package/{name}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                return Package(
                    name=data['name'],
                    version=data['version'],
                    description=data['description'],
                    author=data['author'],
                    downloads=data.get('downloads', 0),
                    rating=data.get('rating', 0.0),
                    status=PackageStatus.AVAILABLE,
                    dependencies=data.get('dependencies', []),
                    size=data.get('size', 0)
                )
                
        except Exception as e:
            self.logger.error(f"Failed to get package {name}: {e}")
            
        return None
        
    def install_package(self, name: str, version: Optional[str] = None) -> bool:
        """
        Install a package
        
        Args:
            name: Package name
            version: Specific version (None for latest)
            
        Returns:
            True if installed successfully
        """
        try:
            params = {}
            if version:
                params['version'] = version
                
            response = requests.post(
                f"{self.api_url}/install/{name}",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                package = Package(
                    name=data['name'],
                    version=data['version'],
                    description=data['description'],
                    author=data['author'],
                    downloads=data.get('downloads', 0),
                    rating=data.get('rating', 0.0),
                    status=PackageStatus.INSTALLED,
                    dependencies=data.get('dependencies', []),
                    size=data.get('size', 0)
                )
                
                self.installed_packages[name] = package
                self.logger.info(f"Installed package: {name}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to install {name}: {e}")
            
        return False
        
    def uninstall_package(self, name: str) -> bool:
        """
        Uninstall a package
        
        Args:
            name: Package name
            
        Returns:
            True if uninstalled successfully
        """
        if name not in self.installed_packages:
            self.logger.warning(f"Package {name} not installed")
            return False
            
        try:
            response = requests.delete(f"{self.api_url}/install/{name}", timeout=10)
            
            if response.status_code == 200:
                del self.installed_packages[name]
                self.logger.info(f"Uninstalled package: {name}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to uninstall {name}: {e}")
            
        return False
        
    def update_package(self, name: str) -> bool:
        """
        Update a package
        
        Args:
            name: Package name
            
        Returns:
            True if updated successfully
        """
        if name not in self.installed_packages:
            return False
            
        try:
            response = requests.put(f"{self.api_url}/install/{name}", timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                package = Package(
                    name=data['name'],
                    version=data['version'],
                    description=data['description'],
                    author=data['author'],
                    downloads=data().get('downloads', 0),
                    rating=data.get('rating', 0.0),
                    status=PackageStatus.INSTALLED,
                    dependencies=data.get('dependencies', []),
                    size=data.get('size', 0)
                )
                
                self.installed_packages[name] = package
                self.logger.info(f"Updated package: {name}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to update {name}: {e}")
            
        return False
        
    def get_reviews(self, package_name: str) -> List[Review]:
        """
        Get package reviews
        
        Args:
            package_name: Package name
            
        Returns:
            List of reviews
        """
        try:
            response = requests.get(f"{self.api_url}/reviews/{package_name}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                reviews = []
                
                for item in data.get('reviews', []):
                    reviews.append(Review(
                        author=item['author'],
                        rating=item['rating'],
                        comment=item['comment'],
                        date=item['date']
                    ))
                    
                return reviews
                
        except Exception as e:
            self.logger.error(f"Failed to get reviews for {package_name}: {e}")
            
        return []
        
    def add_review(self, package_name: str, rating: int, comment: str) -> bool:
        """
        Add a review
        
        Args:
            package_name: Package name
            rating: Rating (1-5)
            comment: Review comment
            
        Returns:
            True if added successfully
        """
        try:
            response = requests.post(
                f"{self.api_url}/reviews/{package_name}",
                json={'rating': rating, 'comment': comment},
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.info(f"Added review for {package_name}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to add review: {e}")
            
        return False
        
    def get_categories(self) -> List[str]:
        """
        Get available categories
        
        Returns:
            List of category names
        """
        try:
            response = requests.get(f"{self.api_url}/categories", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('categories', [])
                
        except Exception as e:
            self.logger.error(f"Failed to get categories: {e}")
            
        return []
        
    def get_trending(self, limit: int = 10) -> List[Package]:
        """
        Get trending packages
        
        Args:
            limit: Number of packages
            
        Returns:
            List of trending packages
        """
        try:
            response = requests.get(f"{self.api_url}/trending?limit={limit}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                packages = []
                
                for item in data.get('packages', []):
                    packages.append(Package(
                        name=item['name'],
                        version=item['version'],
                        description=item['description'],
                        author=item['author'],
                        downloads=item.get('downloads', 0),
                        rating=item.get('rating', 0.0),
                        status=PackageStatus.AVAILABLE,
                        dependencies=item.get('dependencies', []),
                        size=item.get('size', 0)
                    ))
                    
                return packages
                
        except Exception as e:
            self.logger.error(f"Failed to get trending: {e}")
            
        return []
        
    def get_installed(self) -> List[Package]:
        """
        Get installed packages
        
        Returns:
            List of installed packages
        """
        return list(self.installed_packages.values())
        
    def check_updates(self) -> List[Package]:
        """
        Check for package updates
        
        Returns:
            List of updatable packages
        """
        updatable = []
        
        for name, package in self.installed_packages.items():
            latest = self.get_package(name)
            
            if latest and latest.version != package.version:
                latest.status = PackageStatus.OUTDATED
                updatable.append(latest)
                
        return updatable
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get marketplace statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'installed_packages': len(self.installed_packages),
            'api_url': self.api_url,
            'cache_size': len(self.cache)
        }


# Global marketplace instance
advanced_marketplace = AdvancedMarketplace()
