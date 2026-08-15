"""
 ============================================================
  MODULE/PLUGIN NAME: ManEngine
  VERSION: 2.0.0
  MODULE CLASS: ManEngine
  DESCRIPTION:
       Enhanced man pages engine v2 with relevance scoring, usage statistics, category organization, cross-references, quick reference, and advanced search capabilities

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

import asyncio
import os
import json
import glob
import re
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
from .man_parser import ManParser
from .man_viewer import ManViewer
from .man_cache import ManCache


class ManSection(Enum):
    """Man page sections"""
    GENERAL = 1
    SYSTEM_CALLS = 2
    LIBRARY_FUNCTIONS = 3
    SPECIAL_FILES = 4
    FILE_FORMATS = 5
    GAMES = 6
    MISC = 7
    SYS_ADMIN = 8
    KERNEL = 9


class ManEngine:
    """Main man pages engine"""
    
    def __init__(self):
        self.enabled = False
        self.config: Dict[str, Any] = {}
        self.parser = ManParser()
        self.viewer = ManViewer()
        self.cache = ManCache()
        self.man_pages: Dict[str, Dict] = {}
        self.index: Dict[str, List[str]] = {}
        self.notification_callback = None
        
        # Multi-source integration
        self.meta_entries: Dict[str, str] = {}  # META files: name -> description
        self.pkg_entries: Dict[str, Dict] = {}  # PKG database: name -> {description, version, tags}
        self.info_entries: Dict[str, str] = {}  # INFO pages: name -> description
        
        # Source priority (highest to lowest)
        self.source_priority = ['meta', 'pkg', 'man', 'info']
        
        # Statistics
        self.source_stats = {
            'meta': {'count': 0, 'load_time': 0},
            'pkg': {'count': 0, 'load_time': 0},
            'man': {'count': 0, 'load_time': 0},
            'info': {'count': 0, 'load_time': 0}
        }
        
        # Search history
        self.search_history: List[Dict[str, Any]] = []
        self.max_history_size = 100
        
        # Usage statistics
        self.usage_stats = {
            'page_views': {},
            'search_queries': {},
            'most_viewed': [],
            'most_searched': []
        }
        
        # Cross-references
        self.cross_references: Dict[str, List[str]] = {}
        
        # Categories
        self.categories: Dict[str, List[str]] = {
            'godmode': ['kernel', 'proc', 'advshield', 'modman', 'plugin', 'geo', 'sysopt', 'event'],
            'standard': ['ai', 'gui', 'network', 'shield', 'cloud', 'modules', 'metadata', 'build', 'task', 'version', 'report'],
            'library': ['emoji', 'unicode', 'figlet', 'ansi', 'anim', 'widgets'],
            'network': ['wifi', 'lan', 'ethernet', 'bluetooth'],
            'filesystem': ['fs'],
            'system': ['sys', 'auth', 'archive', 'display', 'dev', 'python', 'engine'],
            'documentation': ['man', 'help']
        }
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize man engine"""
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        
        # Initialize components
        await self.cache.initialize(self.config.get('cache', {}))
        await self.parser.initialize(self.config.get('parser', {}))
        await self.viewer.initialize(self.config.get('viewer', {}))
        
        # Clear cache to ensure fresh page loading
        await self.cache.clear()
        
        # Load sources in priority order
        await self.load_meta_files()
        await self.load_pkg_database()
        
        # Load built-in man pages
        await self._load_builtin_pages()
        
        # Load INFO pages (lowest priority)
        await self.load_info_pages()
        
        # Load external man pages if configured
        if self.config.get('load_external', False):
            await self._load_external_pages()
            
        # Build index
        self._build_index()
        
    def set_notification_callback(self, callback):
        """Set callback for notifications"""
        self.notification_callback = callback
        
    async def _load_builtin_pages(self):
        """Load built-in man pages"""
        builtin_dir = os.path.join(
            os.path.dirname(__file__), 'pages'
        )
        
        if os.path.exists(builtin_dir):
            for section in range(1, 10):
                section_dir = os.path.join(builtin_dir, f'man{section}')
                if os.path.exists(section_dir):
                    for filename in os.listdir(section_dir):
                        if filename.endswith('.md') or filename.endswith('.man'):
                            filepath = os.path.join(section_dir, filename)
                            await self._load_page(filepath, section)
                            
    async def _load_external_pages(self, man_path: str = None):
        """Load external man pages from system"""
        man_path = man_path or self.config.get('man_path', '/usr/share/man')
        
        if os.path.exists(man_path):
            for section in range(1, 10):
                section_dir = os.path.join(man_path, f'man{section}')
                if os.path.exists(section_dir):
                    for filename in os.listdir(section_dir):
                        if filename.endswith('.gz') or filename.endswith('.md'):
                            filepath = os.path.join(section_dir, filename)
                            await self._load_page(filepath, section)
                            
    async def _load_page(self, filepath: str, section: int):
        """Load a single man page"""
        try:
            # Always parse fresh to ensure aliases are extracted
            page_data = await self.parser.parse_file(filepath, section)
            
            # Store in man pages - use the parsed name as key only
            page_name = page_data.get('name', os.path.basename(filepath))
            self.man_pages[page_name] = page_data
            
        except Exception as e:
            if self.notification_callback:
                await self.notification_callback(
                    f"Error loading man page: {filepath}",
                    str(e),
                    'warning',
                    'low'
                )
                
    def _build_index(self):
        """Build search index"""
        self.index = {}
        for name, page in self.man_pages.items():
            # Index by name
            if name not in self.index:
                self.index[name] = []
            self.index[name].append(name)
            
            # Index by alias
            alias = page.get('alias')
            if alias:
                if alias not in self.index:
                    self.index[alias] = []
                self.index[alias].append(name)
            
            # Index by keywords
            keywords = page.get('keywords', [])
            for keyword in keywords:
                if keyword not in self.index:
                    self.index[keyword] = []
                self.index[keyword].append(name)
            
            # Index by section
            section = page.get('section', 1)
            section_key = f"section{section}"
            if section_key not in self.index:
                self.index[section_key] = []
            self.index[section_key].append(name)
            
    async def get_page(self, name: str, section: int = None) -> Optional[Dict]:
        """Get a man page by name or alias"""
        # Try exact match first
        if name in self.man_pages:
            page = self.man_pages[name]
            if section is None or page.get('section') == section:
                return page
                
        # Try alias lookup
        for page_name, page in self.man_pages.items():
            if page.get('alias') == name:
                if section is None or page.get('section') == section:
                    return page
                
        # Try section-specific lookup
        if section:
            key = f"{name}.{section}"
            if key in self.man_pages:
                return self.man_pages[key]
                
        return None
        
    async def search(self, query: str) -> List[str]:
        """Search for man pages with relevance scoring"""
        query = query.lower()
        scored_results = []
        
        # Search in page names, aliases, and descriptions with scoring
        for name, page in self.man_pages.items():
            score = 0
            
            # Exact name match - highest score
            if query == name.lower():
                score += 100
            # Exact alias match - same high score
            elif query == page.get('alias', '').lower():
                score += 100
            # Name contains query
            elif query in name.lower():
                score += 50
            # Alias contains query
            elif query in page.get('alias', '').lower():
                score += 50
            # Description contains query
            elif query in page.get('description', '').lower():
                score += 30
            # Keywords match
            elif any(query in keyword.lower() for keyword in page.get('keywords', [])):
                score += 20
            # Partial name match
            elif name.lower().startswith(query):
                score += 15
            # Partial alias match
            elif page.get('alias', '').lower().startswith(query):
                score += 15
            # Fuzzy match (contains parts of query)
            elif any(part in name.lower() for part in query.split() if len(part) > 2):
                score += 10
                
            if score > 0:
                scored_results.append((name, score))
                
        # Sort by score (descending) then by name
        scored_results.sort(key=lambda x: (-x[1], x[0]))
        
        # Track search statistics
        self.usage_stats['search_queries'][query] = self.usage_stats['search_queries'].get(query, 0) + 1
        
        # Add to search history
        self.search_history.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'search',
            'query': query,
            'results_count': len(scored_results)
        })
        if len(self.search_history) > self.max_history_size:
            self.search_history.pop(0)
        
        # Return just names, sorted by relevance
        return [name for name, score in scored_results]
        
    async def list_pages(self, section: int = None) -> List[str]:
        """List all available man pages"""
        if section:
            pages = [page.get('name', key) for key, page in self.man_pages.items() 
                   if page.get('section') == section]
        else:
            # Return just the names from page data, not keys
            pages = [page.get('name', key) for key, page in self.man_pages.items()]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_pages = []
        for page in pages:
            if page not in seen:
                seen.add(page)
                unique_pages.append(page)
        
        return unique_pages
        
    async def display_page(self, name: str, section: int = None, color: bool = True) -> str:
        """Display a man page with optional color support"""
        page = await self.get_page(name, section)
        if not page:
            return f"No manual entry for {name}"
        
        # Track page view statistics
        self.usage_stats['page_views'][name] = self.usage_stats['page_views'].get(name, 0) + 1
        
        # Add to search history
        self.search_history.append({
            'timestamp': datetime.now().isoformat(),
            'type': 'view',
            'query': name,
            'results_count': 1
        })
        if len(self.search_history) > self.max_history_size:
            self.search_history.pop(0)
            
        return await self.viewer.render(page, color=color)
        
    async def add_page(self, name: str, content: str, section: int = 1, 
                      keywords: List[str] = None) -> bool:
        """Add a custom man page"""
        try:
            page_data = await self.parser.parse_content(content, section)
            page_data['name'] = name
            page_data['keywords'] = keywords or []
            page_data['section'] = section
            page_data['custom'] = True
            page_data['created'] = datetime.now().isoformat()
            
            self.man_pages[name] = page_data
            self._build_index()
            
            return True
        except Exception as e:
            if self.notification_callback:
                await self.notification_callback(
                    f"Error adding man page: {name}",
                    str(e),
                    'error',
                    'high'
                )
            return False
            
    async def remove_page(self, name: str) -> bool:
        """Remove a custom man page"""
        if name in self.man_pages:
            page = self.man_pages[name]
            if page.get('custom', False):
                del self.man_pages[name]
                self._build_index()
                return True
        return False
        
    async def update_page(self, name: str, content: str = None, 
                        keywords: List[str] = None) -> bool:
        """Update an existing man page"""
        if name not in self.man_pages:
            return False
            
        page = self.man_pages[name]
        if not page.get('custom', False):
            return False
            
        if content:
            section = page.get('section', 1)
            page_data = await self.parser.parse_content(content, section)
            page.update(page_data)
            
        if keywords:
            page['keywords'] = keywords
            
        page['updated'] = datetime.now().isoformat()
        self._build_index()
        
        return True
        
    async def export_page(self, name: str, format: str = 'md') -> Optional[str]:
        """Export a man page to specified format"""
        page = await self.get_page(name)
        if not page:
            return None
            
        if format == 'md':
            return await self.viewer.to_markdown(page)
        elif format == 'html':
            return await self.viewer.to_html(page)
        elif format == 'txt':
            return await self.viewer.to_text(page)
        else:
            return None
            
    async def get_stats(self) -> Dict[str, Any]:
        """Get man engine statistics"""
        source_stats = await self.get_source_stats()
        return {
            'enabled': self.enabled,
            'total_pages': len(self.man_pages),
            'custom_pages': sum(1 for p in self.man_pages.values() if p.get('custom', False)),
            'builtin_pages': sum(1 for p in self.man_pages.values() if not p.get('custom', False)),
            'cache_stats': await self.cache.get_stats(),
            'index_size': len(self.index),
            'sources': source_stats
        }
        
    async def enable(self):
        """Enable man engine"""
        self.enabled = True
        
    async def disable(self):
        """Disable man engine"""
        self.enabled = False
        
    async def refresh(self):
        """Refresh man pages from sources"""
        self.man_pages.clear()
        await self._load_builtin_pages()
        if self.config.get('load_external', False):
            await self._load_external_pages()
        self._build_index()
        
    # ============================================================
    # MULTI-SOURCE INTEGRATION
    # ============================================================
    
    async def load_meta_files(self, pattern: str = "**/*.meta"):
        """Load META files with highest priority"""
        import time
        start_time = time.time()
        
        try:
            # Search for META files recursively
            base_dir = os.path.dirname(os.path.dirname(__file__))  # TerminalX root
            meta_files = glob.glob(os.path.join(base_dir, pattern), recursive=True)
            
            for mf in meta_files:
                try:
                    name = None
                    desc = None
                    with open(mf, "r", encoding="utf-8") as f:
                        for line in f:
                            if line.startswith("name="):
                                name = line.split("=", 1)[1].strip()
                            elif line.startswith("desc="):
                                desc = line.split("=", 1)[1].strip()
                    
                    if name and desc:
                        self.meta_entries[name] = desc
                        
                        # Also add to man_pages if not exists
                        if name not in self.man_pages:
                            self.man_pages[name] = {
                                'name': name,
                                'description': desc,
                                'section': 1,
                                'custom': True,
                                'source': 'meta',
                                'created': datetime.now().isoformat()
                            }
                            
                except Exception as e:
                    if self.notification_callback:
                        await self.notification_callback(
                            f"Error loading META file: {mf}",
                            str(e),
                            'warning',
                            'low'
                        )
            
            load_time = time.time() - start_time
            self.source_stats['meta'] = {'count': len(self.meta_entries), 'load_time': load_time}
            
            if self.notification_callback:
                await self.notification_callback(
                    f"Loaded {len(self.meta_entries)} META entries",
                    f"Load time: {load_time:.3f}s",
                    'info',
                    'low'
                )
                
        except Exception as e:
            if self.notification_callback:
                await self.notification_callback(
                    "Error loading META files",
                    str(e),
                    'error',
                    'high'
                )
    
    async def load_pkg_database(self, path: str = "pkgdb/*.json"):
        """Load PKG manager database"""
        import time
        start_time = time.time()
        
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))  # TerminalX root
            pkg_files = glob.glob(os.path.join(base_dir, path))
            
            for pf in pkg_files:
                try:
                    with open(pf, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    # Handle both single package and array of packages
                    packages = data if isinstance(data, list) else [data]
                    
                    for pkg in packages:
                        name = pkg.get("name")
                        desc = pkg.get("description")
                        version = pkg.get("version", "unknown")
                        tags = pkg.get("tags", [])
                        
                        if name and desc:
                            self.pkg_entries[name] = {
                                'description': desc,
                                'version': version,
                                'tags': tags
                            }
                            
                            # Add to man_pages if not exists (lower priority than META)
                            if name not in self.man_pages and name not in self.meta_entries:
                                self.man_pages[name] = {
                                    'name': name,
                                    'description': desc,
                                    'section': 1,
                                    'custom': True,
                                    'source': 'pkg',
                                    'version': version,
                                    'tags': tags,
                                    'created': datetime.now().isoformat()
                                }
                                
                except Exception as e:
                    if self.notification_callback:
                        await self.notification_callback(
                            f"Error loading PKG file: {pf}",
                            str(e),
                            'warning',
                            'low'
                        )
            
            load_time = time.time() - start_time
            self.source_stats['pkg'] = {'count': len(self.pkg_entries), 'load_time': load_time}
            
            if self.notification_callback:
                await self.notification_callback(
                    f"Loaded {len(self.pkg_entries)} PKG entries",
                    f"Load time: {load_time:.3f}s",
                    'info',
                    'low'
                )
                
        except Exception as e:
            if self.notification_callback:
                await self.notification_callback(
                    "Error loading PKG database",
                    str(e),
                    'error',
                    'high'
                )
    
    async def load_info_pages(self, path: str = "info/*.info"):
        """Load INFO pages"""
        import time
        start_time = time.time()
        
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))  # TerminalX root
            info_files = glob.glob(os.path.join(base_dir, path))
            
            for inf in info_files:
                try:
                    with open(inf, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    name = data.get("node")
                    title = data.get("title", "")
                    content = data.get("content", "")
                    
                    if not name:
                        continue
                    
                    # Extract first sentence as description
                    first_sentence = content.split(".")[0].strip()
                    desc = f"{title} — {first_sentence}"
                    
                    self.info_entries[name] = desc
                    
                    # Add to man_pages if not exists (lowest priority)
                    if name not in self.man_pages and name not in self.meta_entries and name not in self.pkg_entries:
                        self.man_pages[name] = {
                            'name': name,
                            'description': desc,
                            'section': 1,
                            'custom': True,
                            'source': 'info',
                            'title': title,
                            'created': datetime.now().isoformat()
                        }
                        
                except Exception as e:
                    if self.notification_callback:
                        await self.notification_callback(
                            f"Error loading INFO file: {inf}",
                            str(e),
                            'warning',
                            'low'
                        )
            
            load_time = time.time() - start_time
            self.source_stats['info'] = {'count': len(self.info_entries), 'load_time': load_time}
            
            if self.notification_callback:
                await self.notification_callback(
                    f"Loaded {len(self.info_entries)} INFO entries",
                    f"Load time: {load_time:.3f}s",
                    'info',
                    'low'
                )
                
        except Exception as e:
            if self.notification_callback:
                await self.notification_callback(
                    "Error loading INFO pages",
                    str(e),
                    'error',
                    'high'
                )
    
    # ============================================================
    # WHATIS FUNCTIONALITY
    # ============================================================
    
    async def whatis(self, name: str) -> Optional[str]:
        """Get short description for a module (like whatis command)"""
        # Check sources in priority order
        if name in self.meta_entries:
            return f"[META] {self.meta_entries[name]}"
        
        if name in self.pkg_entries:
            return f"[PKG] {self.pkg_entries[name]['description']}"
        
        if name in self.man_pages:
            page = self.man_pages[name]
            source = page.get('source', 'MAN')
            return f"[{source}] {page.get('description', '')}"
        
        if name in self.info_entries:
            return f"[INFO] {self.info_entries[name]}"
        
        return None
    
    async def whatis_batch(self, names: List[str]) -> Dict[str, str]:
        """Get descriptions for multiple modules at once"""
        results = {}
        for name in names:
            desc = await self.whatis(name)
            if desc:
                results[name] = desc
        return results
    
    async def whatis_all(self) -> Dict[str, str]:
        """Get all available whatis entries"""
        results = {}
        
        # Add all sources with priority indicators
        for name, desc in self.meta_entries.items():
            results[name] = f"[META] {desc}"
        
        for name, pkg_data in self.pkg_entries.items():
            if name not in results:
                results[name] = f"[PKG] {pkg_data['description']}"
        
        for name, page in self.man_pages.items():
            if name not in results:
                source = page.get('source', 'MAN')
                results[name] = f"[{source}] {page.get('description', '')}"
        
        for name, desc in self.info_entries.items():
            if name not in results:
                results[name] = f"[INFO] {desc}"
        
        return results
    
    # ============================================================
    # ADVANCED SEARCH
    # ============================================================
    
    async def search_wildcard(self, pattern: str) -> Dict[str, str]:
        """Search using wildcard patterns (e.g., 'net*', '*wifi*')"""
        try:
            # Convert wildcard to regex
            regex_pattern = pattern.replace("*", ".*")
            regex = re.compile(regex_pattern, re.IGNORECASE)
            
            results = {}
            
            # Search in all sources with priority
            for name, desc in self.meta_entries.items():
                if regex.match(name):
                    results[name] = f"[META] {desc}"
            
            for name, pkg_data in self.pkg_entries.items():
                if name not in results and regex.match(name):
                    results[name] = f"[PKG] {pkg_data['description']}"
            
            for name, page in self.man_pages.items():
                if name not in results and regex.match(name):
                    results[name] = f"[MAN] {page.get('description', '')}"
            
            for name, desc in self.info_entries.items():
                if name not in results and regex.match(name):
                    results[name] = f"[INFO] {desc}"
            
            return results
            
        except Exception as e:
            if self.notification_callback:
                await self.notification_callback(
                    f"Error in wildcard search: {pattern}",
                    str(e),
                    'error',
                    'medium'
                )
            return {}
    
    async def search_fuzzy(self, query: str, threshold: float = 0.6) -> Dict[str, float]:
        """Fuzzy search with approximate matching and similarity scores"""
        import difflib
        
        query = query.lower()
        results = {}
        
        # Search in all page names
        for name in self.man_pages.keys():
            # Sequence matcher for similarity
            similarity = difflib.SequenceMatcher(None, query, name.lower()).ratio()
            
            if similarity >= threshold:
                results[name] = similarity
        
        # Sort by similarity (descending)
        results = dict(sorted(results.items(), key=lambda x: x[1], reverse=True))
        
        return results
    
    async def search_regex(self, pattern: str) -> Dict[str, str]:
        """Search using full regex patterns"""
        try:
            regex = re.compile(pattern, re.IGNORECASE)
            results = {}
            
            # Search in all sources with priority
            for name, desc in self.meta_entries.items():
                if regex.search(name) or regex.search(desc):
                    results[name] = f"[META] {desc}"
            
            for name, pkg_data in self.pkg_entries.items():
                if name not in results and (regex.search(name) or regex.search(pkg_data['description'])):
                    results[name] = f"[PKG] {pkg_data['description']}"
            
            for name, page in self.man_pages.items():
                if name not in results and (regex.search(name) or regex.search(page.get('description', ''))):
                    results[name] = f"[MAN] {page.get('description', '')}"
            
            for name, desc in self.info_entries.items():
                if name not in results and (regex.search(name) or regex.search(desc)):
                    results[name] = f"[INFO] {desc}"
            
            return results
            
        except Exception as e:
            if self.notification_callback:
                await self.notification_callback(
                    f"Error in regex search: {pattern}",
                    str(e),
                    'error',
                    'medium'
                )
            return {}
    
    async def search_by_source(self, pattern: str, source: str) -> Dict[str, str]:
        """Search only in specific source (meta, pkg, man, info)"""
        pattern_lower = pattern.lower()
        results = {}
        
        if source == 'meta':
            for name, desc in self.meta_entries.items():
                if pattern_lower in name.lower() or pattern_lower in desc.lower():
                    results[name] = f"[META] {desc}"
        
        elif source == 'pkg':
            for name, pkg_data in self.pkg_entries.items():
                if pattern_lower in name.lower() or pattern_lower in pkg_data['description'].lower():
                    results[name] = f"[PKG] {pkg_data['description']}"
        
        elif source == 'man':
            for name, page in self.man_pages.items():
                if pattern_lower in name.lower() or pattern_lower in page.get('description', '').lower():
                    results[name] = f"[MAN] {page.get('description', '')}"
        
        elif source == 'info':
            for name, desc in self.info_entries.items():
                if pattern_lower in name.lower() or pattern_lower in desc.lower():
                    results[name] = f"[INFO] {desc}"
        
        return results
    
    async def search_by_tag(self, tag: str) -> Dict[str, str]:
        """Search modules by tag (from PKG database)"""
        results = {}
        tag_lower = tag.lower()
        
        for name, pkg_data in self.pkg_entries.items():
            tags = pkg_data.get('tags', [])
            if any(tag_lower in t.lower() for t in tags):
                results[name] = f"[PKG] {pkg_data['description']}"
        
        return results
    
    async def search_by_section(self, section: int) -> Dict[str, str]:
        """Search modules by man section"""
        results = {}
        
        for name, page in self.man_pages.items():
            if page.get('section') == section:
                source = page.get('source', 'MAN')
                results[name] = f"[{source}] {page.get('description', '')}"
        
        return results
    
    async def search_advanced(self, query: str, options: Dict[str, Any] = None) -> Dict[str, str]:
        """Advanced search with multiple filters
        
        Options:
        - source: filter by source (meta, pkg, man, info)
        - section: filter by section number
        - tag: filter by tag
        - exact: exact match only
        - case_sensitive: case sensitive search
        """
        options = options or {}
        results = {}
        
        # Apply filters
        source_filter = options.get('source')
        section_filter = options.get('section')
        tag_filter = options.get('tag')
        exact_match = options.get('exact', False)
        case_sensitive = options.get('case_sensitive', False)
        
        search_query = query if case_sensitive else query.lower()
        
        # Search in meta
        if not source_filter or source_filter == 'meta':
            for name, desc in self.meta_entries.items():
                if section_filter:  # META doesn't have sections
                    continue
                
                match_name = name if case_sensitive else name.lower()
                match_desc = desc if case_sensitive else desc.lower()
                
                if exact_match:
                    if match_name == search_query:
                        results[name] = f"[META] {desc}"
                else:
                    if search_query in match_name or search_query in match_desc:
                        results[name] = f"[META] {desc}"
        
        # Search in pkg
        if not source_filter or source_filter == 'pkg':
            for name, pkg_data in self.pkg_entries.items():
                if tag_filter:
                    tags = pkg_data.get('tags', [])
                    if not any(tag_filter.lower() in t.lower() for t in tags):
                        continue
                
                match_name = name if case_sensitive else name.lower()
                match_desc = pkg_data['description'] if case_sensitive else pkg_data['description'].lower()
                
                if exact_match:
                    if match_name == search_query:
                        results[name] = f"[PKG] {pkg_data['description']}"
                else:
                    if search_query in match_name or search_query in match_desc:
                        results[name] = f"[PKG] {pkg_data['description']}"
        
        # Search in man
        if not source_filter or source_filter == 'man':
            for name, page in self.man_pages.items():
                if section_filter and page.get('section') != section_filter:
                    continue
                
                match_name = name if case_sensitive else name.lower()
                match_desc = page.get('description', '') if case_sensitive else page.get('description', '').lower()
                
                if exact_match:
                    if match_name == search_query:
                        source = page.get('source', 'MAN')
                        results[name] = f"[{source}] {page.get('description', '')}"
                else:
                    if search_query in match_name or search_query in match_desc:
                        source = page.get('source', 'MAN')
                        results[name] = f"[{source}] {page.get('description', '')}"
        
        # Search in info
        if not source_filter or source_filter == 'info':
            for name, desc in self.info_entries.items():
                if section_filter:  # INFO doesn't have sections
                    continue
                
                match_name = name if case_sensitive else name.lower()
                match_desc = desc if case_sensitive else desc.lower()
                
                if exact_match:
                    if match_name == search_query:
                        results[name] = f"[INFO] {desc}"
                else:
                    if search_query in match_name or search_query in match_desc:
                        results[name] = f"[INFO] {desc}"
        
        return results
    
    # ============================================================
    # CACHE MANAGEMENT
    # ============================================================
    
    async def rebuild_cache(self):
        """Rebuild entire cache from all sources"""
        self.man_pages.clear()
        self.meta_entries.clear()
        self.pkg_entries.clear()
        self.info_entries.clear()
        
        # Clear existing cache
        await self.cache.clear()
        
        # Load sources in priority order
        await self.load_meta_files()
        await self.load_pkg_database()
        await self._load_builtin_pages()
        await self.load_info_pages()
        
        # Rebuild index
        self._build_index()
        
        # Update man stats
        self.source_stats['man'] = {
            'count': len(self.man_pages),
            'load_time': 0  # Loaded from builtin
        }
        
        if self.notification_callback:
            await self.notification_callback(
                "Cache rebuilt successfully",
                f"Total entries: {len(self.man_pages)}",
                'info',
                'medium'
            )
    
    # ============================================================
    # STATISTICS
    # ============================================================
    
    async def get_source_stats(self) -> Dict[str, Any]:
        """Get statistics for all data sources"""
        return {
            'sources': self.source_stats,
            'total_entries': len(self.man_pages),
            'meta_count': len(self.meta_entries),
            'pkg_count': len(self.pkg_entries),
            'info_count': len(self.info_entries),
            'man_count': len(self.man_pages) - len(self.meta_entries) - len(self.pkg_entries) - len(self.info_entries),
            'source_priority': self.source_priority
        }
    
    async def get_detailed_stats(self) -> Dict[str, Any]:
        """Get detailed statistics including cache performance"""
        cache_stats = await self.cache.get_stats()
        source_stats = await self.get_source_stats()
        
        return {
            'cache': cache_stats,
            'sources': source_stats,
            'index': {
                'size': len(self.index),
                'entries': list(self.index.keys())[:10]  # First 10 index keys
            },
            'total_pages': len(self.man_pages),
            'custom_pages': sum(1 for p in self.man_pages.values() if p.get('custom', False)),
            'builtin_pages': sum(1 for p in self.man_pages.values() if not p.get('custom', False))
        }
    
    # ============================================================
    # IMPORT/EXPORT
    # ============================================================
    
    async def export_database(self, filepath: str, format: str = 'json') -> bool:
        """Export entire database to file"""
        try:
            data = {
                'meta': self.meta_entries,
                'pkg': self.pkg_entries,
                'info': self.info_entries,
                'man': {name: page for name, page in self.man_pages.items() if page.get('custom', False)},
                'export_date': datetime.now().isoformat(),
                'version': '1.1.0'
            }
            
            if format == 'json':
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            elif format == 'txt':
                with open(filepath, 'w', encoding='utf-8') as f:
                    for name, desc in self.meta_entries.items():
                        f.write(f"[META] {name} - {desc}\n")
                    for name, pkg_data in self.pkg_entries.items():
                        f.write(f"[PKG] {name} - {pkg_data['description']}\n")
                    for name, desc in self.info_entries.items():
                        f.write(f"[INFO] {name} - {desc}\n")
            else:
                return False
            
            return True
        except Exception as e:
            if self.notification_callback:
                await self.notification_callback(
                    f"Error exporting database: {filepath}",
                    str(e),
                    'error',
                    'high'
                )
            return False
    
    async def import_database(self, filepath: str, merge: bool = True) -> bool:
        """Import database from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not merge:
                self.meta_entries.clear()
                self.pkg_entries.clear()
                self.info_entries.clear()
                self.man_pages.clear()
            
            # Import meta entries
            for name, desc in data.get('meta', {}).items():
                if merge or name not in self.meta_entries:
                    self.meta_entries[name] = desc
            
            # Import pkg entries
            for name, pkg_data in data.get('pkg', {}).items():
                if merge or name not in self.pkg_entries:
                    self.pkg_entries[name] = pkg_data
            
            # Import info entries
            for name, desc in data.get('info', {}).items():
                if merge or name not in self.info_entries:
                    self.info_entries[name] = desc
            
            # Import custom man pages
            for name, page in data.get('man', {}).items():
                if merge or name not in self.man_pages:
                    self.man_pages[name] = page
            
            # Rebuild index
            self._build_index()
            
            if self.notification_callback:
                await self.notification_callback(
                    f"Database imported from {filepath}",
                    f"Merge mode: {merge}",
                    'info',
                    'medium'
                )
            
            return True
        except Exception as e:
            if self.notification_callback:
                await self.notification_callback(
                    f"Error importing database: {filepath}",
                    str(e),
                    'error',
                    'high'
                )
            return False
    
    # ============================================================
    # VALIDATION
    # ============================================================
    
    async def validate_entries(self) -> Dict[str, List[str]]:
        """Validate all entries and return issues"""
        issues = {
            'missing_descriptions': [],
            'empty_names': [],
            'duplicates': [],
            'invalid_chars': []
        }
        
        all_names = []
        
        # Check meta entries
        for name, desc in self.meta_entries.items():
            all_names.append(name)
            if not name or not name.strip():
                issues['empty_names'].append(f"META: {name}")
            if not desc or not desc.strip():
                issues['missing_descriptions'].append(f"META: {name}")
            if re.search(r'[<>:"|?*]', name):
                issues['invalid_chars'].append(f"META: {name}")
        
        # Check pkg entries
        for name, pkg_data in self.pkg_entries.items():
            all_names.append(name)
            if not name or not name.strip():
                issues['empty_names'].append(f"PKG: {name}")
            if not pkg_data.get('description') or not pkg_data['description'].strip():
                issues['missing_descriptions'].append(f"PKG: {name}")
            if re.search(r'[<>:"|?*]', name):
                issues['invalid_chars'].append(f"PKG: {name}")
        
        # Check info entries
        for name, desc in self.info_entries.items():
            all_names.append(name)
            if not name or not name.strip():
                issues['empty_names'].append(f"INFO: {name}")
            if not desc or not desc.strip():
                issues['missing_descriptions'].append(f"INFO: {name}")
            if re.search(r'[<>:"|?*]', name):
                issues['invalid_chars'].append(f"INFO: {name}")
        
        # Check for duplicates
        seen = set()
        for name in all_names:
            if name in seen:
                issues['duplicates'].append(name)
            seen.add(name)
        
        return issues
    
    # ============================================================
    # CATEGORY ORGANIZATION
    # ============================================================
    
    async def list_categories(self) -> Dict[str, List[str]]:
        """List all categories and their pages"""
        return self.categories
    
    async def get_category_pages(self, category: str) -> List[str]:
        """Get pages in a specific category"""
        return self.categories.get(category, [])
    
    async def add_to_category(self, category: str, page_name: str) -> bool:
        """Add a page to a category"""
        if category not in self.categories:
            self.categories[category] = []
        if page_name not in self.categories[category]:
            self.categories[category].append(page_name)
            return True
        return False
    
    # ============================================================
    # CROSS-REFERENCES
    # ============================================================
    
    async def add_cross_reference(self, page_name: str, reference: str) -> bool:
        """Add a cross-reference to a page"""
        if page_name not in self.cross_references:
            self.cross_references[page_name] = []
        if reference not in self.cross_references[page_name]:
            self.cross_references[page_name].append(reference)
            return True
        return False
    
    async def get_cross_references(self, page_name: str) -> List[str]:
        """Get cross-references for a page"""
        return self.cross_references.get(page_name, [])
    
    async def build_cross_references(self):
        """Automatically build cross-references from SEE ALSO sections"""
        for name, page in self.man_pages.items():
            see_also = page.get('see_also', [])
            for ref in see_also:
                # Extract page name from reference (e.g., "man(1)" -> "man")
                ref_name = ref.split('(')[0].strip() if '(' in ref else ref.strip()
                await self.add_cross_reference(name, ref_name)
    
    # ============================================================
    # USAGE STATISTICS
    # ============================================================
    
    async def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        # Calculate most viewed and most searched
        sorted_views = sorted(self.usage_stats['page_views'].items(), key=lambda x: x[1], reverse=True)
        sorted_searches = sorted(self.usage_stats['search_queries'].items(), key=lambda x: x[1], reverse=True)
        
        self.usage_stats['most_viewed'] = sorted_views[:10]
        self.usage_stats['most_searched'] = sorted_searches[:10]
        
        return self.usage_stats
    
    async def reset_usage_stats(self):
        """Reset usage statistics"""
        self.usage_stats = {
            'page_views': {},
            'search_queries': {},
            'most_viewed': [],
            'most_searched': []
        }
    
    async def get_search_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get search history"""
        return self.search_history[-limit:]
    
    async def clear_search_history(self):
        """Clear search history"""
        self.search_history = []
    
    # ============================================================
    # QUICK REFERENCE
    # ============================================================
    
    async def get_quick_reference(self, page_name: str) -> Optional[str]:
        """Get quick reference summary for a page"""
        page = await self.get_page(page_name)
        if not page:
            return None
        
        # Build quick reference from key sections
        sections = []
        
        # Name and description
        name = page.get('name', '')
        description = page.get('description', '')
        if name and description:
            sections.append(f"**{name}**: {description}")
        
        # Synopsis (first few lines)
        synopsis = page.get('synopsis', '')
        if synopsis:
            # Handle both string and list
            if isinstance(synopsis, list):
                synopsis_text = '\n'.join(str(s) for s in synopsis[:5])
            else:
                synopsis_text = synopsis
            lines = synopsis_text.split('\n')[:5]  # First 5 lines
            sections.append("Synopsis:\n" + '\n'.join(lines))
        
        # Key options (first few)
        options = page.get('options', '')
        if options:
            # Handle both string and list
            if isinstance(options, list):
                options_text = '\n'.join(str(o) for o in options[:5])
            else:
                options_text = options
            lines = options_text.split('\n')[:5]  # First 5 options
            sections.append("Key Options:\n" + '\n'.join(lines))
        
        return '\n\n'.join(sections) if sections else None

    # ============================================================
    # HISTORY
    # ============================================================
    
    def _add_to_history(self, query: str, search_type: str, results_count: int):
        """Add search to history"""
        entry = {
            'query': query,
            'type': search_type,
            'results_count': results_count,
            'timestamp': datetime.now().isoformat()
        }
        
        self.search_history.append(entry)
        
        # Keep history size limited
        if len(self.search_history) > self.max_history_size:
            self.search_history.pop(0)
    
    async def get_search_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent search history"""
        return self.search_history[-limit:]
    
    async def clear_search_history(self):
        """Clear search history"""
        self.search_history.clear()
