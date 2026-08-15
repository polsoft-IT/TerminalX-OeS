"""
 ============================================================
  MODULE/PLUGIN NAME: VersionModule
  VERSION: 1.0.0
  MODULE CLASS: VersionModule
  DESCRIPTION:
       Version management module with full command list, integrated with TerminalX logger and notification system

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
import json
import datetime
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from core import ANSI


# ============================================================
# Model wersji
# ============================================================

@dataclass
class VersionInfo:
    """
    Struktura przechowująca pełne informacje o wersji.
    Format wersji: v{major}.{minor}.{patch}.{modules:02d}.{plugins:02d}
    Można ją rozszerzać o kolejne pola (branch, commit, itd.).
    """
    name: str = "TerminalX"
    major: int = 2
    minor: int = 5
    patch: int = 0
    module_count: int = 0
    plugin_count: int = 0
    build: int = 102
    tag: str = "stable"
    api_level: int = 1
    engine_core: str = "hybrid-core"
    plugins_api: str = "v1"
    created_at: str = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    description: str = "TerminalX - Advanced Terminal Operating System"

    def semver(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def full_version(self) -> str:
        """Format: v{major}.{minor}.{patch}.{modules:02d}.{plugins:02d}"""
        base = f"v{self.major}.{self.minor}.{self.patch}.{self.module_count:02d}.{self.plugin_count:02d}"
        if self.tag:
            return f"{base}-{self.tag}"
        return base

    def short(self) -> str:
        return f"{self.name} {self.full_version()}"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ============================================================
# Manager wersji
# ============================================================

class VersionModule:
    """
    Manager wersji z pełną listą komend.
    Zintegrowany z systemem logowania i powiadomień TerminalX.
    """

    def __init__(self):
        self.info = VersionInfo()
        self.logger = None
        self.notification_callback = None
        self.enabled = True
        
    def set_logger(self, logger):
        """Set logger instance"""
        self.logger = logger
        
    def set_notification_callback(self, callback):
        """Set notification callback"""
        self.notification_callback = callback
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize version module"""
        config = config or {}
        self.enabled = config.get('enabled', True)
        
        # Load custom version info from config if provided
        if config.get('name'):
            self.info.name = config['name']
        if config.get('major'):
            self.info.major = config['major']
        if config.get('minor'):
            self.info.minor = config['minor']
        if config.get('patch'):
            self.info.patch = config['patch']
        if config.get('build'):
            self.info.build = config['build']
        if config.get('tag'):
            self.info.tag = config['tag']
            
        if self.logger:
            self.logger.info(f"VersionModule initialized: {self.info.full_version()}")
            
    # --- API wysokiego poziomu ---

    def get_semver(self) -> str:
        return self.info.semver()

    def get_full_version(self) -> str:
        return self.info.full_version()

    def get_info_dict(self) -> Dict[str, Any]:
        return self.info.to_dict()

    def set_build(self, build: int) -> None:
        self.info.build = build
        if self.logger:
            self.logger.info(f"Build number set to: {build}")

    def set_tag(self, tag: str) -> None:
        self.info.tag = tag
        if self.logger:
            self.logger.info(f"Tag set to: {tag}")

    def set_module_count(self, count: int) -> None:
        """Set module count and auto-increment patch if needed"""
        if count > 99:
            self.info.patch += 1
            self.info.module_count = count % 100
            if self.logger:
                self.logger.info(f"Module count exceeded 99, patch incremented to {self.info.patch}")
        else:
            self.info.module_count = count
        if self.logger:
            self.logger.info(f"Module count set to: {self.info.module_count}")

    def set_plugin_count(self, count: int) -> None:
        """Set plugin count and auto-increment patch if needed"""
        if count > 99:
            self.info.patch += 1
            self.info.plugin_count = count % 100
            if self.logger:
                self.logger.info(f"Plugin count exceeded 99, patch incremented to {self.info.patch}")
        else:
            self.info.plugin_count = count
        if self.logger:
            self.logger.info(f"Plugin count set to: {self.info.plugin_count}")

    def update_counts(self, module_count: int, plugin_count: int) -> None:
        """Update both module and plugin counts"""
        self.set_module_count(module_count)
        self.set_plugin_count(plugin_count)

    # --- Formatowane wyjścia ---

    def format_banner(self) -> str:
        """Display centered blue gradient banner"""
        banner_text = "2026 (c) polsoft.ITS (TM)  |  TerminalOS v2.5.0  |  Cross-platform  |  Sebastian Januchowski"
        try:
            return ANSI.blue_gradient_banner(banner_text)
        except UnicodeEncodeError:
            return ANSI.CYAN + banner_text + ANSI.RESET

    def format_human(self) -> str:
        info = self.info
        lines = [
            f"{ANSI.CYAN}{info.name}{ANSI.RESET}",
            f"  Version: {ANSI.GREEN}{info.full_version()}{ANSI.RESET}",
            f"  Semver:  {ANSI.YELLOW}{info.semver()}{ANSI.RESET}",
            f"  Modules: {ANSI.MAGENTA}{info.module_count:02d}{ANSI.RESET}",
            f"  Plugins: {ANSI.MAGENTA}{info.plugin_count:02d}{ANSI.RESET}",
            f"  Build:   {ANSI.YELLOW}{info.build}{ANSI.RESET}",
            f"  Tag:     {ANSI.MAGENTA}{info.tag}{ANSI.RESET}",
            f"  API:     core={info.api_level}, plugins={info.plugins_api}",
            f"  Engine:  {info.engine_core}",
            f"  Created: {info.created_at}",
            f"  Desc:    {info.description}",
        ]
        return "\n".join(lines)

    def format_short(self) -> str:
        return f"{ANSI.CYAN}{self.info.short()}{ANSI.RESET}"

    def format_json(self, pretty: bool = True) -> str:
        data = self.info.to_dict()
        if pretty:
            return json.dumps(data, indent=2, sort_keys=True)
        return json.dumps(data, separators=(",", ":"))

    # --- Komendy CLI (mapa) ---

    def get_commands(self) -> Dict[str, str]:
        """
        Pełna lista komend obsługiwanych przez moduł.
        Można ją wykorzystać np. w helpie głównego silnika.
        """
        return {
            "version": "Wyświetla pełną wersję (v{major}.{minor}.{patch}.{modules:02d}.{plugins:02d}).",
            "semver": "Wyświetla wersję semver (major.minor.patch).",
            "short": "Krótka forma: nazwa + pełna wersja.",
            "info": "Czytelne, kolorowe informacje o wersji.",
            "json": "Informacje o wersji w formacie JSON.",
            "json-compact": "JSON bez wcięć (kompaktowy).",
            "all": "Wyświetla wszystkie informacje (human + JSON).",
            "banner": "Wyświetla wysrodkowany niebieski banner z efektem gradient.",
            "set-build": "Ustawia numer build (wymaga wartości).",
            "set-tag": "Ustawia tag wersji (np. alpha/beta/rc/stable).",
            "set-modules": "Ustawia liczbę modułów (auto-increment patch jeśli >99).",
            "set-plugins": "Ustawia liczbę pluginów (auto-increment patch jeśli >99).",
            "update-counts": "Aktualizuje liczbę modułów i pluginów jednocześnie.",
            "commands": "Wyświetla listę dostępnych komend.",
        }
        
    async def enable(self):
        """Enable version module"""
        self.enabled = True
        if self.logger:
            self.logger.info("VersionModule enabled")
        
    async def disable(self):
        """Disable version module"""
        self.enabled = False
        if self.logger:
            self.logger.info("VersionModule disabled")
