"""
 ============================================================
  MODULE/PLUGIN NAME: ManViewer
  VERSION: 2.0.0
  MODULE CLASS: ManViewer
  DESCRIPTION:
       Enhanced man page viewer v2 with color output support, improved rendering, and multiple format support

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
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum


class ViewerFormat(Enum):
    """Viewer output formats"""
    TEXT = "text"
    MARKDOWN = "markdown"
    HTML = "html"
    ANSI = "ansi"


class ManViewer:
    """Man page viewer"""
    
    def __init__(self):
        self.config: Dict[str, Any] = {}
        self.default_format = ViewerFormat.ANSI
        self.terminal_width = 80
        self.terminal_height = 24
        self.colors_enabled = True
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize viewer"""
        self.config = config or {}
        self.default_format = ViewerFormat(self.config.get('default_format', 'ansi'))
        self.terminal_width = self.config.get('terminal_width', 80)
        self.terminal_height = self.config.get('terminal_height', 24)
        self.colors_enabled = self.config.get('colors_enabled', True)
        
    async def render(self, page_data: Dict[str, Any], format: ViewerFormat = None, color: bool = True) -> str:
        """Render a man page for display"""
        format = format or self.default_format
        
        if format == ViewerFormat.TEXT:
            return await self.to_text(page_data)
        elif format == ViewerFormat.MARKDOWN:
            return await self.to_markdown(page_data)
        elif format == ViewerFormat.HTML:
            return await self.to_html(page_data)
        elif format == ViewerFormat.ANSI:
            return await self.to_ansi(page_data, color=color)
        else:
            return await self.to_text(page_data)
            
    async def to_text(self, page_data: Dict[str, Any]) -> str:
        """Convert man page to plain text"""
        lines = []
        
        # Header
        lines.append("=" * self.terminal_width)
        lines.append(f"{page_data.get('name', 'Unknown')}({page_data.get('section', 1)})")
        lines.append("=" * self.terminal_width)
        lines.append("")
        
        # Name section
        if page_data.get('name'):
            lines.append("NAME")
            lines.append("-" * 4)
            lines.append(page_data['name'])
            lines.append("")
        
        # Description
        if page_data.get('description'):
            lines.append("DESCRIPTION")
            lines.append("-" * 11)
            lines.append(self._wrap_text(page_data['description']))
            lines.append("")
            
        # Synopsis
        if page_data.get('synopsis'):
            lines.append("SYNOPSIS")
            lines.append("-" * 8)
            lines.append(page_data['synopsis'])
            lines.append("")
            
        # Options
        if page_data.get('options'):
            lines.append("OPTIONS")
            lines.append("-" * 7)
            for option in page_data['options']:
                lines.append(f"  {option}")
            lines.append("")
            
        # Examples
        if page_data.get('examples'):
            lines.append("EXAMPLES")
            lines.append("-" * 8)
            for example in page_data['examples']:
                lines.append(f"  {example}")
            lines.append("")
            
        # See Also
        if page_data.get('see_also'):
            lines.append("SEE ALSO")
            lines.append("-" * 8)
            lines.append(", ".join(page_data['see_also']))
            lines.append("")
            
        # Author
        if page_data.get('author'):
            lines.append("AUTHOR")
            lines.append("-" * 6)
            lines.append(page_data['author'])
            lines.append("")
            
        # Footer
        lines.append("=" * self.terminal_width)
        lines.append(f"TerminalX Man Pages - Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * self.terminal_width)
        
        return "\n".join(lines)
        
    async def to_markdown(self, page_data: Dict[str, Any]) -> str:
        """Convert man page to markdown"""
        lines = []
        
        # Header
        lines.append(f"# {page_data.get('name', 'Unknown')}({page_data.get('section', 1)})")
        lines.append("")
        
        # Name section
        if page_data.get('name'):
            lines.append("## Name")
            lines.append("")
            lines.append(page_data['name'])
            lines.append("")
        
        # Description
        if page_data.get('description'):
            lines.append("## Description")
            lines.append("")
            lines.append(page_data['description'])
            lines.append("")
            
        # Synopsis
        if page_data.get('synopsis'):
            lines.append("## Synopsis")
            lines.append("")
            lines.append("```")
            lines.append(page_data['synopsis'])
            lines.append("```")
            lines.append("")
            
        # Options
        if page_data.get('options'):
            lines.append("## Options")
            lines.append("")
            for option in page_data['options']:
                lines.append(f"- {option}")
            lines.append("")
            
        # Examples
        if page_data.get('examples'):
            lines.append("## Examples")
            lines.append("")
            for example in page_data['examples']:
                lines.append(f"```")
                lines.append(example)
                lines.append("```")
                lines.append("")
                
        # See Also
        if page_data.get('see_also'):
            lines.append("## See Also")
            lines.append("")
            lines.append(", ".join(page_data['see_also']))
            lines.append("")
            
        # Author
        if page_data.get('author'):
            lines.append("## Author")
            lines.append("")
            lines.append(page_data['author'])
            lines.append("")
            
        return "\n".join(lines)
        
    async def to_html(self, page_data: Dict[str, Any]) -> str:
        """Convert man page to HTML"""
        lines = []
        
        # HTML header
        lines.append("<!DOCTYPE html>")
        lines.append("<html>")
        lines.append("<head>")
        lines.append("<meta charset='UTF-8'>")
        lines.append("<title>{}({})</title>".format(page_data.get('name', 'Unknown'), page_data.get('section', 1)))
        lines.append("<style>")
        lines.append("body { font-family: monospace; max-width: 800px; margin: 0 auto; padding: 20px; }")
        lines.append("h1 { border-bottom: 2px solid #333; }")
        lines.append("h2 { border-bottom: 1px solid #ccc; margin-top: 30px; }")
        lines.append("code { background: #f4f4f4; padding: 2px 4px; border-radius: 3px; }")
        lines.append("pre { background: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto; }")
        lines.append("</style>")
        lines.append("</head>")
        lines.append("<body>")
        
        # Header
        lines.append("<h1>{}({})</h1>".format(page_data.get('name', 'Unknown'), page_data.get('section', 1)))
        lines.append("")
        
        # Name section
        if page_data.get('name'):
            lines.append("<h2>Name</h2>")
            lines.append("<p>{}</p>".format(page_data['name']))
            lines.append("")
        
        # Description
        if page_data.get('description'):
            lines.append("<h2>Description</h2>")
            lines.append("<p>{}</p>".format(page_data['description']))
            lines.append("")
            
        # Synopsis
        if page_data.get('synopsis'):
            lines.append("<h2>Synopsis</h2>")
            lines.append("<pre><code>{}</code></pre>".format(page_data['synopsis']))
            lines.append("")
            
        # Options
        if page_data.get('options'):
            lines.append("<h2>Options</h2>")
            lines.append("<ul>")
            for option in page_data['options']:
                lines.append("<li>{}</li>".format(option))
            lines.append("</ul>")
            lines.append("")
            
        # Examples
        if page_data.get('examples'):
            lines.append("<h2>Examples</h2>")
            for example in page_data['examples']:
                lines.append("<pre><code>{}</code></pre>".format(example))
                lines.append("")
                
        # See Also
        if page_data.get('see_also'):
            lines.append("<h2>See Also</h2>")
            lines.append("<p>{}</p>".format(", ".join(page_data['see_also'])))
            lines.append("")
            
        # Author
        if page_data.get('author'):
            lines.append("<h2>Author</h2>")
            lines.append("<p>{}</p>".format(page_data['author']))
            lines.append("")
            
        # Footer
        lines.append("<hr>")
        lines.append("<p><small>TerminalX Man Pages - Generated: {}</small></p>".format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        # HTML footer
        lines.append("</body>")
        lines.append("</html>")
        
        return "\n".join(lines)
        
    async def to_ansi(self, page_data: Dict[str, Any], color: bool = True) -> str:
        """Convert man page to ANSI colored text"""
        if not color or not self.colors_enabled:
            return await self.to_text(page_data)
            
        lines = []
        
        # ANSI color codes
        BOLD = "\033[1m"
        RESET = "\033[0m"
        BLUE = "\033[34m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"
        CYAN = "\033[36m"
        MAGENTA = "\033[35m"
        
        # Header
        lines.append(f"{BLUE}{BOLD}{'=' * self.terminal_width}{RESET}")
        lines.append(f"{CYAN}{BOLD}{page_data.get('name', 'Unknown')}({page_data.get('section', 1)}){RESET}")
        lines.append(f"{BLUE}{BOLD}{'=' * self.terminal_width}{RESET}")
        lines.append("")
        
        # Name section
        if page_data.get('name'):
            lines.append(f"{GREEN}{BOLD}NAME{RESET}")
            lines.append(f"{YELLOW}{'-' * 4}{RESET}")
            lines.append(f"{BOLD}{page_data['name']}{RESET}")
            lines.append("")
        
        # Description
        if page_data.get('description'):
            lines.append(f"{GREEN}{BOLD}DESCRIPTION{RESET}")
            lines.append(f"{YELLOW}{'-' * 11}{RESET}")
            lines.append(self._wrap_text(page_data['description']))
            lines.append("")
            
        # Synopsis
        if page_data.get('synopsis'):
            lines.append(f"{GREEN}{BOLD}SYNOPSIS{RESET}")
            lines.append(f"{YELLOW}{'-' * 8}{RESET}")
            lines.append(f"{CYAN}{page_data['synopsis']}{RESET}")
            lines.append("")
            
        # Options
        if page_data.get('options'):
            lines.append(f"{GREEN}{BOLD}OPTIONS{RESET}")
            lines.append(f"{YELLOW}{'-' * 7}{RESET}")
            for option in page_data['options']:
                lines.append(f"  {MAGENTA}{option}{RESET}")
            lines.append("")
            
        # Examples
        if page_data.get('examples'):
            lines.append(f"{GREEN}{BOLD}EXAMPLES{RESET}")
            lines.append(f"{YELLOW}{'-' * 8}{RESET}")
            for example in page_data['examples']:
                lines.append(f"  {CYAN}{example}{RESET}")
            lines.append("")
                
        # See Also
        if page_data.get('see_also'):
            lines.append(f"{GREEN}{BOLD}SEE ALSO{RESET}")
            lines.append(f"{YELLOW}{'-' * 8}{RESET}")
            lines.append(f"{CYAN}{', '.join(page_data['see_also'])}{RESET}")
            lines.append("")
            
        # Author
        if page_data.get('author'):
            lines.append(f"{GREEN}{BOLD}AUTHOR{RESET}")
            lines.append(f"{YELLOW}{'-' * 6}{RESET}")
            lines.append(f"{BOLD}{page_data['author']}{RESET}")
            lines.append("")
            
        # Footer
        lines.append(f"{BLUE}{'=' * self.terminal_width}{RESET}")
        lines.append(f"{YELLOW}TerminalX Man Pages v2 - Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
        lines.append(f"{BLUE}{'=' * self.terminal_width}{RESET}")
        
        return "\n".join(lines)
    
    def _wrap_text(self, text: str, width: int = None) -> str:
        """Wrap text to specified width"""
        width = width or (self.terminal_width - 4)
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= width:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
                
        if current_line:
            lines.append(" ".join(current_line))
            
        return "\n".join(lines)
        
    async def get_page_preview(self, page_data: Dict[str, Any], lines: int = 10) -> str:
        """Get a preview of the man page (first N lines)"""
        full_text = await self.to_text(page_data)
        preview_lines = full_text.split('\n')[:lines]
        return "\n".join(preview_lines)
        
    async def search_in_page(self, page_data: Dict[str, Any], query: str) -> List[int]:
        """Search for text in a man page, return line numbers"""
        text = await self.to_text(page_data)
        lines = text.split('\n')
        matches = []
        
        for i, line in enumerate(lines):
            if query.lower() in line.lower():
                matches.append(i + 1)  # 1-based line numbers
                
        return matches
