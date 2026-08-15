"""
 ============================================================
  MODULE/PLUGIN NAME: ReportEngine
  VERSION: 1.0.0
  MODULE CLASS: ReportEngine
  DESCRIPTION:
       Advanced report engine with plugin system, integrated with TerminalX logger, notifications, and ANSI colors

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
import sys
import json
import abc
import time
import uuid
import types
import inspect
import logging
import importlib
from dataclasses import dataclass, field
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Callable,
    Iterable,
    Protocol,
    runtime_checkable,
)
from core import ANSI


# ============================================================
# LOGGING
# ============================================================

class ReportLogger:
    """Report logger integrated with TerminalX"""
    
    def __init__(self, logger=None):
        self.logger = logger or self._create_default_logger()
        
    def _create_default_logger(self):
        """Create default logger if none provided"""
        import logging
        logger = logging.getLogger("report_engine")
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            fmt = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
            handler.setFormatter(logging.Formatter(fmt))
            logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
        
    def info(self, msg: str):
        if self.logger:
            self.logger.info(msg)
            
    def debug(self, msg: str):
        if self.logger:
            self.logger.debug(msg)
            
    def warning(self, msg: str):
        if self.logger:
            self.logger.warning(msg)
            
    def error(self, msg: str):
        if self.logger:
            self.logger.error(msg)


# ============================================================
# TERMINAL INTEGRATION INTERFACES (ABSTRAKCJE)
# ============================================================

@runtime_checkable
class TerminalIO(Protocol):
    """Abstrakcyjny interfejs I/O terminala."""

    def write(self, text: str, *, style: Optional[str] = None) -> None:
        ...

    def writeln(self, text: str = "", *, style: Optional[str] = None) -> None:
        ...

    def flush(self) -> None:
        ...


@runtime_checkable
class TerminalTheme(Protocol):
    """Abstrakcyjny interfejs motywu terminala (kolory, style)."""

    def style_for_level(self, level: str) -> str:
        ...

    def style_for_section(self, section: str) -> str:
        ...


@runtime_checkable
class TerminalSession(Protocol):
    """Abstrakcyjny interfejs sesji terminala."""

    io: TerminalIO
    theme: TerminalTheme

    def get_env(self) -> Dict[str, str]:
        ...

    def get_capabilities(self) -> Dict[str, Any]:
        ...


# ============================================================
# PODSTAWOWE STRUKTURY DANYCH RAPORTU
# ============================================================

@dataclass
class ReportSection:
    """Pojedyncza sekcja raportu."""

    id: str
    title: str
    content: str
    level: int = 1
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Report:
    """Model raportu w pamięci."""

    id: str
    title: str
    created_at: float
    sections: List[ReportSection] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)

    def add_section(
        self,
        title: str,
        content: str,
        *,
        level: int = 1,
        meta: Optional[Dict[str, Any]] = None,
    ) -> ReportSection:
        section = ReportSection(
            id=str(uuid.uuid4()),
            title=title,
            content=content,
            level=level,
            meta=meta or {},
        )
        self.sections.append(section)
        return section


# ============================================================
# SYSTEM PLUGINÓW
# ============================================================

class PluginError(Exception):
    pass


class PluginContext:
    """Kontekst przekazywany do pluginów."""

    def __init__(
        self,
        engine: "ReportEngine",
        report: Optional[Report] = None,
        terminal_session: Optional[TerminalSession] = None,
    ) -> None:
        self.engine = engine
        self.report = report
        self.terminal_session = terminal_session

    def log(self, msg: str, level: int = logging.INFO) -> None:
        if self.engine.logger:
            self.engine.logger.info(f"[plugin] {msg}")


class ReportPlugin(abc.ABC):
    """Bazowa klasa pluginu raportowego."""

    name: str = "base"
    version: str = "0.0.0"
    description: str = ""
    priority: int = 100  # niższa wartość = wyższy priorytet

    def __init__(self) -> None:
        self.enabled: bool = True

    @abc.abstractmethod
    def plugin_type(self) -> str:
        """Zwraca typ pluginu (np. 'template', 'output', 'filter', 'postprocess')."""
        raise NotImplementedError

    def on_register(self, ctx: PluginContext) -> None:
        """Wywoływane po zarejestrowaniu pluginu."""
        pass

    def on_unregister(self, ctx: PluginContext) -> None:
        """Wywoływane po wyrejestrowaniu pluginu."""
        pass


class TemplatePlugin(ReportPlugin):
    """Plugin generujący szablony raportów."""

    def plugin_type(self) -> str:
        return "template"

    @abc.abstractmethod
    def generate(
        self,
        ctx: PluginContext,
        template_name: str,
        data: Dict[str, Any],
    ) -> Report:
        """Generuje raport na podstawie nazwy szablonu i danych."""
        raise NotImplementedError


class OutputPlugin(ReportPlugin):
    """Plugin odpowiedzialny za zapis/serializację raportu do różnych formatów."""

    def plugin_type(self) -> str:
        return "output"

    @abc.abstractmethod
    def supported_formats(self) -> Iterable[str]:
        """Zwraca listę obsługiwanych formatów (np. ['txt', 'md', 'html', 'json'])."""
        raise NotImplementedError

    @abc.abstractmethod
    def render(
        self,
        ctx: PluginContext,
        report: Report,
        fmt: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        """Renderuje raport do danego formatu i zwraca bajty."""
        raise NotImplementedError


class FilterPlugin(ReportPlugin):
    """Plugin filtrujący lub modyfikujący raport przed renderowaniem."""

    def plugin_type(self) -> str:
        return "filter"

    @abc.abstractmethod
    def apply(
        self,
        ctx: PluginContext,
        report: Report,
    ) -> Report:
        """Zwraca zmodyfikowany raport."""
        raise NotImplementedError


class PostProcessPlugin(ReportPlugin):
    """Plugin post‑processing (np. wysyłka, archiwizacja, logowanie)."""

    def plugin_type(self) -> str:
        return "postprocess"

    @abc.abstractmethod
    def run(
        self,
        ctx: PluginContext,
        report: Report,
        output_bytes: bytes,
        fmt: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Wykonuje akcję po wygenerowaniu raportu."""
        raise NotImplementedError


# ============================================================
# REJESTR PLUGINÓW
# ============================================================

class PluginRegistry:
    """Rejestr pluginów raportowych."""

    def __init__(self) -> None:
        self._plugins: Dict[str, List[ReportPlugin]] = {}

    def register(self, plugin: ReportPlugin, ctx: PluginContext) -> None:
        ptype = plugin.plugin_type()
        self._plugins.setdefault(ptype, [])
        self._plugins[ptype].append(plugin)
        self._plugins[ptype].sort(key=lambda p: p.priority)
        plugin.on_register(ctx)
        if ctx.engine.logger:
            ctx.engine.logger.debug(f"Zarejestrowano plugin '{plugin.name}' typu '{ptype}'")

    def unregister(self, plugin: ReportPlugin, ctx: PluginContext) -> None:
        ptype = plugin.plugin_type()
        if ptype in self._plugins and plugin in self._plugins[ptype]:
            self._plugins[ptype].remove(plugin)
            plugin.on_unregister(ctx)
            if ctx.engine.logger:
                ctx.engine.logger.debug(f"Wyrejestrowano plugin '{plugin.name}' typu '{ptype}'")

    def get_plugins(self, ptype: str) -> List[ReportPlugin]:
        return list(self._plugins.get(ptype, []))

    def get_template_plugins(self) -> List[TemplatePlugin]:
        return [p for p in self.get_plugins("template") if isinstance(p, TemplatePlugin)]

    def get_output_plugins(self) -> List[OutputPlugin]:
        return [p for p in self.get_plugins("output") if isinstance(p, OutputPlugin)]

    def get_filter_plugins(self) -> List[FilterPlugin]:
        return [p for p in self.get_plugins("filter") if isinstance(p, FilterPlugin)]

    def get_postprocess_plugins(self) -> List[PostProcessPlugin]:
        return [p for p in self.get_plugins("postprocess") if isinstance(p, PostProcessPlugin)]


# ============================================================
# KONFIGURACJA SILNIKA
# ============================================================

@dataclass
class ReportEngineConfig:
    """Konfiguracja silnika raportów."""

    plugin_paths: List[str] = field(default_factory=list)
    default_format: str = "txt"
    allow_unknown_format: bool = False
    terminal_integration_enabled: bool = True
    metadata_defaults: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def from_json(path: str) -> "ReportEngineConfig":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return ReportEngineConfig(
            plugin_paths=data.get("plugin_paths", []),
            default_format=data.get("default_format", "txt"),
            allow_unknown_format=data.get("allow_unknown_format", False),
            terminal_integration_enabled=data.get("terminal_integration_enabled", True),
            metadata_defaults=data.get("metadata_defaults", {}),
        )


# ============================================================
# GŁÓWNY SILNIK RAPORTÓW
# ============================================================

class ReportEngine:
    """Silnik raportów z obsługą pluginów i integracją z terminalem."""

    def __init__(
        self,
        config: Optional[ReportEngineConfig] = None,
        terminal_session: Optional[TerminalSession] = None,
    ) -> None:
        self.config = config or ReportEngineConfig()
        self.registry = PluginRegistry()
        self.terminal_session = terminal_session
        self.logger = None
        self.notification_callback = None
        self.enabled = True
        self._ctx = PluginContext(engine=self, report=None, terminal_session=terminal_session)

        if self.config.plugin_paths:
            self._auto_load_plugins(self.config.plugin_paths)
            
    def set_logger(self, logger):
        """Set logger instance"""
        self.logger = ReportLogger(logger)
        
    def set_notification_callback(self, callback):
        """Set notification callback"""
        self.notification_callback = callback
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize report engine"""
        config = config or {}
        self.enabled = config.get('enabled', True)
        
        # Update config from dict
        if config.get('plugin_paths'):
            self.config.plugin_paths = config['plugin_paths']
        if config.get('default_format'):
            self.config.default_format = config['default_format']
        if config.get('terminal_integration_enabled') is not None:
            self.config.terminal_integration_enabled = config['terminal_integration_enabled']
            
        if self.config.plugin_paths:
            self._auto_load_plugins(self.config.plugin_paths)
            
        if self.logger:
            self.logger.info("ReportEngine initialized")

    # ------------------------------------------------------------------ #
    # ŁADOWANIE PLUGINÓW
    # ------------------------------------------------------------------ #

    def _auto_load_plugins(self, paths: List[str]) -> None:
        """Automatyczne ładowanie pluginów z podanych ścieżek (foldery lub moduły)."""
        for path in paths:
            try:
                if os.path.isdir(path):
                    self._load_plugins_from_directory(path)
                else:
                    self._load_plugins_from_module(path)
            except Exception as exc:
                if self.logger:
                    self.logger.error(f"Nie udało się załadować pluginów z '{path}': {exc}")

    def _load_plugins_from_directory(self, directory: str) -> None:
        """Ładowanie pluginów z katalogu (pliki *.py)."""
        sys.path.insert(0, directory)
        for fname in os.listdir(directory):
            if not fname.endswith(".py"):
                continue
            mod_name = os.path.splitext(fname)[0]
            self._load_plugins_from_module(mod_name)
        sys.path.pop(0)

    def _load_plugins_from_module(self, module_name: str) -> None:
        """Ładowanie pluginów z modułu."""
        if self.logger:
            self.logger.debug(f"Ładowanie pluginów z modułu '{module_name}'")
        module = importlib.import_module(module_name)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, ReportPlugin) and obj is not ReportPlugin:
                plugin_instance = obj()
                self.registry.register(plugin_instance, self._ctx)

    # ------------------------------------------------------------------ #
    # TWORZENIE RAPORTÓW
    # ------------------------------------------------------------------ #

    def create_report(
        self,
        title: str,
        *,
        meta: Optional[Dict[str, Any]] = None,
    ) -> Report:
        """Tworzy pusty raport."""
        report = Report(
            id=str(uuid.uuid4()),
            title=title,
            created_at=time.time(),
            meta={**self.config.metadata_defaults, **(meta or {})},
        )
        if self.logger:
            self.logger.debug(f"Utworzono raport '{report.id}' o tytule '{title}'")
        return report

    def from_template(
        self,
        template_name: str,
        data: Dict[str, Any],
        *,
        meta: Optional[Dict[str, Any]] = None,
    ) -> Report:
        """Tworzy raport na podstawie szablonu (plugin TemplatePlugin)."""
        for plugin in self.registry.get_template_plugins():
            if not plugin.enabled:
                continue
            ctx = PluginContext(engine=self, report=None, terminal_session=self.terminal_session)
            try:
                report = plugin.generate(ctx, template_name, data)
                if meta:
                    report.meta.update(meta)
                if self.logger:
                    self.logger.info(
                        f"Raport wygenerowany przez plugin szablonu '{plugin.name}' "
                        f"z template='{template_name}'"
                    )
                return report
            except Exception as exc:
                if self.logger:
                    self.logger.error(f"Plugin szablonu '{plugin.name}' zgłosił błąd: {exc}")
        raise PluginError(f"Brak pluginu szablonu obsługującego template='{template_name}'")

    # ------------------------------------------------------------------ #
    # FILTROWANIE / MODYFIKACJA RAPORTU
    # ------------------------------------------------------------------ #

    def apply_filters(self, report: Report) -> Report:
        """Przepuszcza raport przez wszystkie pluginy filtrujące."""
        for plugin in self.registry.get_filter_plugins():
            if not plugin.enabled:
                continue
            ctx = PluginContext(engine=self, report=report, terminal_session=self.terminal_session)
            try:
                report = plugin.apply(ctx, report)
                if self.logger:
                    self.logger.debug(f"Zastosowano filtr '{plugin.name}'")
            except Exception as exc:
                if self.logger:
                    self.logger.error(f"Plugin filtra '{plugin.name}' zgłosił błąd: {exc}")
        return report

    # ------------------------------------------------------------------ #
    # RENDEROWANIE / ZAPIS
    # ------------------------------------------------------------------ #

    def _find_output_plugin_for_format(self, fmt: str) -> Optional[OutputPlugin]:
        for plugin in self.registry.get_output_plugins():
            if not plugin.enabled:
                continue
            if fmt in plugin.supported_formats():
                return plugin
        return None

    def render(
        self,
        report: Report,
        fmt: Optional[str] = None,
        *,
        options: Optional[Dict[str, Any]] = None,
        apply_filters: bool = True,
        run_postprocess: bool = True,
    ) -> bytes:
        """Renderuje raport do danego formatu."""
        fmt = fmt or self.config.default_format
        if self.logger:
            self.logger.debug(f"Renderowanie raportu '{report.id}' do formatu '{fmt}'")

        if apply_filters:
            report = self.apply_filters(report)

        plugin = self._find_output_plugin_for_format(fmt)
        if not plugin:
            msg = f"Brak pluginu output dla formatu '{fmt}'"
            if not self.config.allow_unknown_format:
                raise PluginError(msg)
            if self.logger:
                self.logger.warning(msg + " – użycie fallbacku TXT.")
            fmt = "txt"
            plugin = self._find_output_plugin_for_format(fmt)
            if not plugin:
                raise PluginError("Brak pluginu output dla fallbacku 'txt'")

        ctx = PluginContext(engine=self, report=report, terminal_session=self.terminal_session)
        output_bytes = plugin.render(ctx, report, fmt, options or {})

        if run_postprocess:
            for pp in self.registry.get_postprocess_plugins():
                if not pp.enabled:
                    continue
                try:
                    pp.run(ctx, report, output_bytes, fmt, options or {})
                except Exception as exc:
                    if self.logger:
                        self.logger.error(f"Plugin postprocess '{pp.name}' zgłosił błąd: {exc}")

        return output_bytes

    def save_to_file(
        self,
        report: Report,
        path: str,
        fmt: Optional[str] = None,
        *,
        options: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Renderuje raport i zapisuje do pliku."""
        fmt = fmt or self.config.default_format
        output_bytes = self.render(report, fmt, options=options)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "wb") as f:
            f.write(output_bytes)
        if self.logger:
            self.logger.info(f"Zapisano raport '{report.id}' do pliku '{path}' (fmt={fmt})")
            
        # Send notification
        if self.notification_callback:
            self.notification_callback(
                f"Report saved: {report.title}",
                f"Report saved to {path} in {fmt} format",
                'info',
                'low'
            )
            
        return path

    # ------------------------------------------------------------------ #
    # INTEGRACJA Z TERMINALEM
    # ------------------------------------------------------------------ #

    def display_in_terminal(
        self,
        report: Report,
        *,
        fmt: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Wyświetla raport w terminalu z użyciem motywu i I/O terminala."""
        if not self.config.terminal_integration_enabled or self.terminal_session is None:
            if self.logger:
                self.logger.warning("Integracja z terminalem jest wyłączona lub brak sesji terminala.")
            return

        fmt = fmt or "txt"
        output_bytes = self.render(
            report,
            fmt=fmt,
            options=options,
            apply_filters=True,
            run_postprocess=False,  # postprocess może być osobno
        )
        text = output_bytes.decode(options.get("encoding", "utf-8") if options else "utf-8")

        io = self.terminal_session.io
        theme = self.terminal_session.theme

        # Wyświetlanie z kolorami ANSI
        print(f"{ANSI.CYAN}== {report.title} =={ANSI.RESET}")
        print(f"{ANSI.YELLOW}ID: {report.id}{ANSI.RESET}")
        print(f"{ANSI.YELLOW}Created: {time.ctime(report.created_at)}{ANSI.RESET}")
        print()

        # Jeśli format jest prosty (txt/md), można wypisać sekcje bezpośrednio.
        for sec in report.sections:
            prefix = "#" * sec.level
            print(f"{ANSI.GREEN}{prefix} {sec.title}{ANSI.RESET}")
            print(sec.content)
            print()

    # ------------------------------------------------------------------ #
    # API WYSOKIEGO POZIOMU
    # ------------------------------------------------------------------ #
    
    def get_commands(self) -> Dict[str, str]:
        """Get available commands"""
        return {
            "create": "Create a new report",
            "template": "Generate report from template",
            "render": "Render report to specific format",
            "save": "Save report to file",
            "display": "Display report in terminal",
            "plugins": "List available plugins",
            "formats": "List supported output formats",
        }
    
    async def enable(self):
        """Enable report engine"""
        self.enabled = True
        if self.logger:
            self.logger.info("ReportEngine enabled")
        
    async def disable(self):
        """Disable report engine"""
        self.enabled = False
        if self.logger:
            self.logger.info("ReportEngine disabled")


# ============================================================
# PRZYKŁADOWE WBUdOWANE PLUGINY (BASIC)
# ============================================================

class BasicTextOutputPlugin(OutputPlugin):
    """Podstawowy plugin output dla formatów 'txt' i 'md'."""

    name = "basic_text_output"
    version = "2.5.0"
    description = "Podstawowy renderer tekstowy (txt/md)."
    priority = 10

    def supported_formats(self) -> Iterable[str]:
        return ["txt", "md"]

    def render(
        self,
        ctx: PluginContext,
        report: Report,
        fmt: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        options = options or {}
        encoding = options.get("encoding", "utf-8")
        lines: List[str] = []

        if fmt == "md":
            lines.append(f"# {report.title}")
            lines.append(f"_ID: {report.id}_")
            lines.append(f"_Created: {time.ctime(report.created_at)}_")
            lines.append("")
            for sec in report.sections:
                prefix = "#" * sec.level
                lines.append(f"{prefix} {sec.title}")
                lines.append(sec.content)
                lines.append("")
        else:  # txt
            lines.append(f"{report.title}")
            lines.append(f"ID: {report.id}")
            lines.append(f"Created: {time.ctime(report.created_at)}")
            lines.append("")
            for sec in report.sections:
                lines.append(sec.title.upper())
                lines.append(sec.content)
                lines.append("")

        text = "\n".join(lines)
        return text.encode(encoding)


class JsonOutputPlugin(OutputPlugin):
    """Plugin output dla formatu JSON."""

    name = "json_output"
    version = "2.5.0"
    description = "Renderer JSON dla raportów."
    priority = 20

    def supported_formats(self) -> Iterable[str]:
        return ["json"]

    def render(
        self,
        ctx: PluginContext,
        report: Report,
        fmt: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        options = options or {}
        encoding = options.get("encoding", "utf-8")

        payload = {
            "id": report.id,
            "title": report.title,
            "created_at": report.created_at,
            "meta": report.meta,
            "sections": [
                {
                    "id": s.id,
                    "title": s.title,
                    "content": s.content,
                    "level": s.level,
                    "meta": s.meta,
                }
                for s in report.sections
            ],
        }
        text = json.dumps(payload, ensure_ascii=False, indent=2)
        return text.encode(encoding)


class UppercaseFilterPlugin(FilterPlugin):
    """Przykładowy filtr – zamiana treści sekcji na wielkie litery."""

    name = "uppercase_filter"
    version = "2.5.0"
    description = "Przykładowy filtr: zamiana content na UPPERCASE."
    priority = 50

    def apply(
        self,
        ctx: PluginContext,
        report: Report,
    ) -> Report:
        for sec in report.sections:
            sec.content = sec.content.upper()
        return report


class LoggingPostProcessPlugin(PostProcessPlugin):
    """Przykładowy plugin postprocess – logowanie informacji o wygenerowanym raporcie."""

    name = "logging_postprocess"
    version = "2.5.0"
    description = "Loguje informacje o wygenerowanym raporcie."
    priority = 100

    def run(
        self,
        ctx: PluginContext,
        report: Report,
        output_bytes: bytes,
        fmt: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        if ctx.engine.logger:
            ctx.engine.logger.info(
                f"[postprocess] Raport '{report.id}' wygenerowany w formacie '{fmt}', "
                f"rozmiar={len(output_bytes)} bajtów"
            )


class SimpleTemplatePlugin(TemplatePlugin):
    """Prosty plugin szablonów – generuje raport na podstawie prostego layoutu."""

    name = "simple_template"
    version = "2.5.0"
    description = "Prosty szablon raportu (nagłówek + sekcje z danych)."
    priority = 10

    def generate(
        self,
        ctx: PluginContext,
        template_name: str,
        data: Dict[str, Any],
    ) -> Report:
        title = data.get("title", f"Raport: {template_name}")
        report = ctx.engine.create_report(title, meta=data.get("meta", {}))

        # Przykładowa logika – można rozbudować o różne template_name.
        sections_data = data.get("sections", [])
        if not sections_data:
            report.add_section("Informacje", "Brak danych sekcji.", level=1)
        else:
            for idx, sec in enumerate(sections_data, start=1):
                report.add_section(
                    sec.get("title", f"Sekcja {idx}"),
                    sec.get("content", ""),
                    level=sec.get("level", 2),
                    meta=sec.get("meta", {}),
                )

        return report


# ============================================================
# FUNKCJA FABRYKUJĄCA – GOTOWY SILNIK Z WBUdOWANYMI PLUGINAMI
# ============================================================

def create_default_engine(
    *,
    config: Optional[ReportEngineConfig] = None,
    terminal_session: Optional[TerminalSession] = None,
) -> ReportEngine:
    """Tworzy silnik z domyślnymi pluginami wbudowanymi."""
    engine = ReportEngine(config=config, terminal_session=terminal_session)
    ctx = PluginContext(engine=engine, report=None, terminal_session=terminal_session)

    # Wbudowane pluginy
    engine.registry.register(SimpleTemplatePlugin(), ctx)
    engine.registry.register(BasicTextOutputPlugin(), ctx)
    engine.registry.register(JsonOutputPlugin(), ctx)
    engine.registry.register(UppercaseFilterPlugin(), ctx)
    engine.registry.register(LoggingPostProcessPlugin(), ctx)

    return engine
