"""
 ============================================================
  MODULE/PLUGIN NAME: ManParser
  VERSION: 1.0.5
  MODULE CLASS: ManParser
  DESCRIPTION:
       Man page parser - parses man pages from various formats (markdown, man, etc.) (handles comprehensive command documentation)

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
import re
import gzip
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum


class ManFormat(Enum):
    """Man page formats"""
    MARKDOWN = "md"
    TRADITIONAL = "man"
    HTML = "html"
    TEXT = "txt"


class ManParser:
    """Man page parser"""
    
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.default_format = ManFormat.MARKDOWN
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize parser"""
        self.config = config or {}
        self.default_format = ManFormat(self.config.get('default_format', 'md'))
        
    async def parse_file(self, filepath: str, section: int = 1) -> Dict[str, Any]:
        """Parse a man page file"""
        # Determine format from extension
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.gz':
            # Decompress and parse
            content = await self._read_gzip(filepath)
            # Remove .gz extension for format detection
            base_ext = os.path.splitext(os.path.basename(filepath))[0].lower()
            if base_ext.endswith('.md'):
                format_type = ManFormat.MARKDOWN
            elif base_ext.endswith('.man'):
                format_type = ManFormat.TRADITIONAL
            else:
                format_type = self.default_format
        elif ext == '.md':
            content = await self._read_file(filepath)
            format_type = ManFormat.MARKDOWN
        elif ext == '.man':
            content = await self._read_file(filepath)
            format_type = ManFormat.TRADITIONAL
        elif ext == '.html':
            content = await self._read_file(filepath)
            format_type = ManFormat.HTML
        else:
            content = await self._read_file(filepath)
            format_type = self.default_format
            
        return await self.parse_content(content, section, format_type)
        
    async def parse_content(self, content: str, section: int = 1, 
                          format_type: ManFormat = None) -> Dict[str, Any]:
        """Parse man page content"""
        format_type = format_type or self.default_format
        
        if format_type == ManFormat.MARKDOWN:
            return await self._parse_markdown(content, section)
        elif format_type == ManFormat.TRADITIONAL:
            return await self._parse_traditional(content, section)
        elif format_type == ManFormat.HTML:
            return await self._parse_html(content, section)
        else:
            return await self._parse_text(content, section)
            
    async def _read_file(self, filepath: str) -> str:
        """Read file content"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(filepath, 'r', encoding='latin-1') as f:
                return f.read()
                
    async def _read_gzip(self, filepath: str) -> str:
        """Read gzip compressed file"""
        try:
            with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with gzip.open(filepath, 'rt', encoding='latin-1') as f:
                return f.read()
                
    async def _parse_markdown(self, content: str, section: int) -> Dict[str, Any]:
        """Parse markdown format man page"""
        import re
        lines = content.split('\n')
        page = {
            'section': section,
            'format': 'markdown',
            'title': '',
            'name': '',
            'alias': '',
            'description': '',
            'synopsis': '',
            'options': [],
            'examples': [],
            'see_also': [],
            'author': '',
            'keywords': [],
            'content': content,
            'parsed': datetime.now().isoformat()
        }
        
        current_section = None
        buffer = []
        
        for line in lines:
            # Headers
            if line.startswith('# '):
                page['title'] = line[2:].strip()
                current_section = 'title'
            elif line.startswith('## '):
                current_section = line[3:].strip().lower()
                buffer = []
            elif line.startswith('### '):
                current_section = line[4:].strip().lower()
                buffer = []
            # Parse based on current section
            elif current_section == 'name':
                if line.strip():
                    # Extract command name and alias
                    name_text = line.strip()
                    if ' - ' in name_text:
                        name_part = name_text.split(' - ')[0].strip()
                        # Extract alias from brackets like [ver]
                        alias_match = re.search(r'\[(.*?)\]', name_part)
                        if alias_match:
                            page['alias'] = alias_match.group(1)
                            # Remove alias brackets from name
                            name_part = re.sub(r'\s*\[.*?\]\s*$', '', name_part)
                        page['name'] = name_part
                    else:
                        # Extract alias even if no description
                        alias_match = re.search(r'\[(.*?)\]', name_text)
                        if alias_match:
                            page['alias'] = alias_match.group(1)
                            # Remove alias brackets from name
                            name_text = re.sub(r'\s*\[.*?\]\s*$', '', name_text)
                        page['name'] = name_text
            elif current_section == 'description':
                if line.strip():
                    page['description'] += line.strip() + ' '
            elif current_section == 'synopsis':
                if line.strip():
                    page['synopsis'] += line.strip() + '\n'
            elif current_section == 'options':
                if line.strip().startswith('-') or line.strip().startswith('--'):
                    if buffer:
                        page['options'].append(' '.join(buffer))
                        buffer = []
                    buffer.append(line.strip())
                elif buffer:
                    buffer.append(line.strip())
            elif current_section == 'examples':
                if line.strip().startswith('```'):
                    continue
                if line.strip():
                    page['examples'].append(line.strip())
            elif current_section == 'see also':
                if line.strip():
                    page['see_also'].extend([s.strip() for s in line.split(',')])
            elif current_section == 'author':
                if line.strip():
                    page['author'] = line.strip()
                    
        # Clean up
        page['description'] = page['description'].strip()
        page['synopsis'] = page['synopsis'].strip()
        
        # Ensure name is set (fallback to title if not set)
        if not page['name'] and page['title']:
            # Try to extract name from title
            if '(' in page['title'] and ')' in page['title']:
                name_part = page['title'].split('(')[0].strip()
                page['name'] = name_part
            elif ' - ' in page['title']:
                page['name'] = page['title'].split(' - ')[0].strip()
            else:
                page['name'] = page['title']
        
        # Extract keywords from description
        words = re.findall(r'\b\w+\b', page['description'].lower())
        page['keywords'] = list(set(words[:10]))  # Top 10 words
        
        return page
        
    async def _parse_traditional(self, content: str, section: int) -> Dict[str, Any]:
        """Parse traditional man page format"""
        lines = content.split('\n')
        page = {
            'section': section,
            'format': 'traditional',
            'title': '',
            'name': '',
            'description': '',
            'synopsis': '',
            'options': [],
            'examples': [],
            'see_also': [],
            'author': '',
            'keywords': [],
            'content': content,
            'parsed': datetime.now().isoformat()
        }
        
        current_section = None
        buffer = []
        
        for line in lines:
            # Section headers (traditional format uses .SH or uppercase)
            if line.startswith('.SH ') or line.startswith('.Sh '):
                current_section = line.split()[1].strip().lower()
                buffer = []
            elif line.startswith('.TH '):
                # Title header
                parts = line.split()
                if len(parts) >= 2:
                    page['name'] = parts[1]
                if len(parts) >= 3:
                    page['section'] = int(parts[2].strip('"'))
            elif line.isupper() and line.strip():
                current_section = line.strip().lower()
                buffer = []
            # Content
            elif current_section == 'name':
                if line.strip() and not line.startswith('.'):
                    page['name'] = line.strip().split('-')[0].strip()
            elif current_section == 'description':
                if line.strip() and not line.startswith('.'):
                    page['description'] += line.strip() + ' '
            elif current_section == 'synopsis':
                if line.strip() and not line.startswith('.'):
                    page['synopsis'] += line.strip() + '\n'
            elif current_section == 'options':
                if line.strip() and not line.startswith('.'):
                    if line.strip().startswith('.TP') or line.strip().startswith('.PP'):
                        if buffer:
                            page['options'].append(' '.join(buffer))
                            buffer = []
                    else:
                        buffer.append(line.strip())
            elif current_section == 'examples':
                if line.strip() and not line.startswith('.'):
                    page['examples'].append(line.strip())
            elif current_section == 'see also':
                if line.strip() and not line.startswith('.'):
                    page['see_also'].extend([s.strip() for s in line.split(',')])
            elif current_section == 'author':
                if line.strip() and not line.startswith('.'):
                    page['author'] = line.strip()
                    
        # Clean up
        page['description'] = page['description'].strip()
        page['synopsis'] = page['synopsis'].strip()
        
        # Extract keywords
        words = re.findall(r'\b\w+\b', page['description'].lower())
        page['keywords'] = list(set(words[:10]))
        
        return page
        
    async def _parse_html(self, content: str, section: int) -> Dict[str, Any]:
        """Parse HTML format man page"""
        # Simple HTML parsing - extract text content
        import re
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '\n', content)
        text = re.sub(r'\n+', '\n', text)
        
        return await self._parse_text(text, section)
        
    async def _parse_text(self, content: str, section: int) -> Dict[str, Any]:
        """Parse plain text format man page"""
        lines = content.split('\n')
        page = {
            'section': section,
            'format': 'text',
            'title': '',
            'name': '',
            'description': '',
            'synopsis': '',
            'options': [],
            'examples': [],
            'see_also': [],
            'author': '',
            'keywords': [],
            'content': content,
            'parsed': datetime.now().isoformat()
        }
        
        current_section = None
        buffer = []
        
        for line in lines:
            # Section headers (look for common patterns)
            if line.strip().upper() == line.strip() and len(line.strip()) > 3:
                current_section = line.strip().lower()
                buffer = []
            # Content
            elif current_section == 'name':
                if line.strip():
                    page['name'] = line.strip().split('-')[0].strip()
            elif current_section == 'description':
                if line.strip():
                    page['description'] += line.strip() + ' '
            elif current_section == 'synopsis':
                if line.strip():
                    page['synopsis'] += line.strip() + '\n'
            elif current_section == 'options':
                if line.strip():
                    if line.strip().startswith('-') or line.strip().startswith('--'):
                        if buffer:
                            page['options'].append(' '.join(buffer))
                            buffer = []
                        buffer.append(line.strip())
                    elif buffer:
                        buffer.append(line.strip())
            elif current_section == 'examples':
                if line.strip():
                    page['examples'].append(line.strip())
            elif current_section == 'see also':
                if line.strip():
                    page['see_also'].extend([s.strip() for s in line.split(',')])
            elif current_section == 'author':
                if line.strip():
                    page['author'] = line.strip()
                    
        # Clean up
        page['description'] = page['description'].strip()
        page['synopsis'] = page['synopsis'].strip()
        
        # Extract keywords
        words = re.findall(r'\b\w+\b', page['description'].lower())
        page['keywords'] = list(set(words[:10]))
        
        return page
        
    async def validate_page(self, page_data: Dict[str, Any]) -> bool:
        """Validate man page data structure"""
        required_fields = ['name', 'description', 'section']
        return all(field in page_data for field in required_fields)
