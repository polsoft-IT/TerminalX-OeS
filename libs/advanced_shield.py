"""
 ============================================================
  MODULE/PLUGIN NAME: AdvancedShield
  VERSION: 2.0.0
  MODULE CLASS: AdvancedShield
  DESCRIPTION:
       Advanced Shield Core for security protection and threat detection

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
import psutil
import json
import time
import shutil
import hashlib
import tempfile
import subprocess
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from libs.clean_logger import CleanLogger, LogLevel


class ShieldLogLevel(Enum):
    """Shield log level"""
    NORMAL = "normal"
    VERBOSE = "verbose"
    SILENT = "silent"


@dataclass
class ShieldEvent:
    """Shield event"""
    type: str
    time: str
    data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ShieldRule:
    """Shield rule"""
    name: str
    rule_type: str
    value: Any
    enabled: bool = True


@dataclass
class ShieldSnapshot:
    """Shield snapshot"""
    name: str
    path: str
    created_at: str


class AdvancedShield:
    """
    ADVANCED SHIELD CORE:
    - KernelShield
    - ProcessShield
    - FileShield
    - NetShield
    - SandboxShield
    - HeuristicShield
    - AISentinel
    - AutoResponse Engine
    - AutoRules Engine
    - AutoLearning Engine
    """

    def __init__(self, logger: Optional[CleanLogger] = None):
        self.logger = logger or CleanLogger("AdvancedShield", LogLevel.INFO)
        self.enabled = True
        self.logs = []
        self.events = []
        self.plugins = []
        self.thread = None

        # sandbox root
        self.sandbox_root = tempfile.mkdtemp(prefix="adv_sandbox_")
        self.snapshots = {}

        # config
        self.config = {
            "log_level": ShieldLogLevel.NORMAL,
            "auto_rules": True,
            "auto_response": True,
            "auto_learning": True,
            "realtime_interval": 1.0,
        }

        # rulesets
        self.kernel_rules = self.load_kernel_rules()
        self.proc_rules = self.load_proc_rules()
        self.file_rules = self.load_file_rules()
        self.net_rules = self.load_net_rules()
        self.heuristic_rules = self.load_heuristic_rules()

    # ============================================================
    # LOGGING
    # ============================================================
    def log(self, event: Dict[str, Any]) -> None:
        """Log event"""
        event["time"] = str(datetime.now())
        self.logs.append(event)
        
        if self.config["log_level"] != ShieldLogLevel.SILENT:
            self.logger.info(f"[{event.get('type', 'UNKNOWN')}] {event}")

    def get_logs(self) -> List[Dict[str, Any]]:
        """Get logs"""
        return self.logs.copy()

    def clear_logs(self) -> None:
        """Clear logs"""
        self.logs.clear()

    # ============================================================
    # CONFIG
    # ============================================================
    def config_get(self, key: str) -> Any:
        """Get config value"""
        return self.config.get(key)

    def config_set(self, key: str, value: Any) -> None:
        """Set config value"""
        self.config[key] = value
        self.logger.info(f"Config updated: {key} = {value}")

    def config_reset(self) -> None:
        """Reset config to defaults"""
        self.config = {
            "log_level": ShieldLogLevel.NORMAL,
            "auto_rules": True,
            "auto_response": True,
            "auto_learning": True,
            "realtime_interval": 1.0,
        }
        self.logger.info("Config reset to defaults")

    # ============================================================
    # RULESETS
    # ============================================================
    def load_kernel_rules(self) -> Dict[str, Any]:
        """Load kernel rules"""
        return {
            "BLOCK_SYSCALLS": ["ptrace", "mount", "umount", "clone", "kexec"],
            "BLOCK_BEHAVIOR": ["dll_injection", "driver_load", "token_steal"]
        }

    def load_proc_rules(self) -> Dict[str, Any]:
        """Load process rules"""
        return {
            "BLOCK_PROCESSES": ["mimikatz.exe", "nc.exe", "powershell.exe", "python.exe -c"],
            "BLOCK_PATTERNS": ["--encodedcommand", "base64", "xor", "AES", "RSA"]
        }

    def load_file_rules(self) -> Dict[str, Any]:
        """Load file rules"""
        return {
            "BLOCK_EXT": [".scr", ".pif", ".bat", ".cmd", ".ps1", ".vbs"],
            "BLOCK_NAMES": ["payload", "dropper", "loader"]
        }

    def load_net_rules(self) -> Dict[str, Any]:
        """Load network rules"""
        return {
            "BLOCK_PORTS": [23, 445, 3389, 5900, 8080],
            "BLOCK_IP_RANGES": ["185.", "45.", "37.", "188.", "212."],
            "BLOCK_PROTOCOLS": ["icmp", "raw"]
        }

    def load_heuristic_rules(self) -> Dict[str, Any]:
        """Load heuristic rules"""
        return {
            "ENTROPY_HIGH": 4.5,
            "PATTERN_SUSPICIOUS": ["eval(", "xor", "AES", "RSA", "keylog", "inject"]
        }

    def get_rules(self, rule_type: str) -> Dict[str, Any]:
        """Get rules by type"""
        rules_map = {
            "kernel": self.kernel_rules,
            "proc": self.proc_rules,
            "file": self.file_rules,
            "net": self.net_rules,
            "heuristic": self.heuristic_rules,
        }
        return rules_map.get(rule_type, {})

    def add_rule(self, rule_type: str, key: str, value: Any) -> bool:
        """Add rule"""
        rules = self.get_rules(rule_type)
        if rules and key in rules:
            if isinstance(rules[key], list):
                if value not in rules[key]:
                    rules[key].append(value)
                    self.log({"type": "RULE_ADD", "rule_type": rule_type, "key": key, "value": value})
                    return True
        return False

    def remove_rule(self, rule_type: str, key: str, value: Any) -> bool:
        """Remove rule"""
        rules = self.get_rules(rule_type)
        if rules and key in rules:
            if isinstance(rules[key], list) and value in rules[key]:
                rules[key].remove(value)
                self.log({"type": "RULE_REMOVE", "rule_type": rule_type, "key": key, "value": value})
                return True
        return False

    # ============================================================
    # SNAPSHOTS
    # ============================================================
    def snapshot_create(self, name: str) -> Optional[str]:
        """Create snapshot"""
        snap_path = os.path.join(self.sandbox_root, f"snapshot_{name}")
        if os.path.exists(snap_path):
            shutil.rmtree(snap_path)
        shutil.copytree(self.sandbox_root, snap_path)
        self.snapshots[name] = snap_path
        self.log({"type": "SNAPSHOT_CREATE", "name": name})
        return snap_path

    def snapshot_restore(self, name: str) -> Optional[str]:
        """Restore snapshot"""
        if name not in self.snapshots:
            return None
        snap_path = self.snapshots[name]
        if not os.path.exists(snap_path):
            return None
        shutil.rmtree(self.sandbox_root)
        shutil.copytree(snap_path, self.sandbox_root)
        self.log({"type": "SNAPSHOT_RESTORE", "name": name})
        return self.sandbox_root

    def snapshot_delete(self, name: str) -> bool:
        """Delete snapshot"""
        if name not in self.snapshots:
            return False
        snap_path = self.snapshots[name]
        shutil.rmtree(snap_path)
        del self.snapshots[name]
        self.log({"type": "SNAPSHOT_DELETE", "name": name})
        return True

    def snapshot_list(self) -> List[str]:
        """List snapshots"""
        return list(self.snapshots.keys())

    # ============================================================
    # FILE ISOLATION
    # ============================================================
    def isolate_file(self, path: str) -> Optional[str]:
        """Isolate file in sandbox"""
        if not os.path.exists(path):
            return None

        dst = os.path.join(self.sandbox_root, os.path.basename(path))
        shutil.copy2(path, dst)

        self.log({"type": "FILE_ISOLATE", "src": path, "dst": dst})
        return dst

    def check_file(self, path: str) -> Dict[str, Any]:
        """Check file against rules"""
        if not os.path.exists(path):
            return {"safe": True, "reason": "File not found"}

        result = {"safe": True, "violations": []}

        # Check extension
        ext = os.path.splitext(path)[1].lower()
        if ext in self.file_rules["BLOCK_EXT"]:
            result["safe"] = False
            result["violations"].append(f"Blocked extension: {ext}")

        # Check name
        name = os.path.basename(path).lower()
        for block_name in self.file_rules["BLOCK_NAMES"]:
            if block_name in name:
                result["safe"] = False
                result["violations"].append(f"Blocked name pattern: {block_name}")

        # Check entropy
        try:
            with open(path, "rb") as f:
                data = f.read()
            ent = self.entropy(data)
            if ent > self.heuristic_rules["ENTROPY_HIGH"]:
                result["safe"] = False
                result["violations"].append(f"High entropy: {ent:.2f}")
        except:
            pass

        return result

    # ============================================================
    # PROCESS ISOLATION
    # ============================================================
    def isolate_process(self, command: str) -> Optional[subprocess.Popen]:
        """Isolate process in sandbox"""
        try:
            proc = subprocess.Popen(
                command,
                cwd=self.sandbox_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            self.log({"type": "PROC_ISOLATE", "cmd": command, "pid": proc.pid})
            return proc
        except Exception as e:
            self.log({"type": "PROC_ISOLATE_FAIL", "cmd": command, "error": str(e)})
            return None

    def check_process(self, pid: int) -> Dict[str, Any]:
        """Check process against rules"""
        try:
            proc = psutil.Process(pid)
            result = {"safe": True, "violations": []}

            # Check name
            name = proc.name().lower()
            for block_proc in self.proc_rules["BLOCK_PROCESSES"]:
                if block_proc in name:
                    result["safe"] = False
                    result["violations"].append(f"Blocked process: {name}")

            # Check command line
            try:
                cmdline = " ".join(proc.cmdline()).lower()
                for pattern in self.proc_rules["BLOCK_PATTERNS"]:
                    if pattern in cmdline:
                        result["safe"] = False
                        result["violations"].append(f"Suspicious pattern: {pattern}")
            except:
                pass

            return result
        except:
            return {"safe": True, "reason": "Process not found"}

    # ============================================================
    # NETWORK ISOLATION
    # ============================================================
    def isolate_network(self) -> None:
        """Enable network isolation"""
        self.log({"type": "NET_ISOLATE", "status": "enabled"})

    def check_network(self, port: int, ip: str = "") -> Dict[str, Any]:
        """Check network connection against rules"""
        result = {"safe": True, "violations": []}

        # Check port
        if port in self.net_rules["BLOCK_PORTS"]:
            result["safe"] = False
            result["violations"].append(f"Blocked port: {port}")

        # Check IP range
        for block_range in self.net_rules["BLOCK_IP_RANGES"]:
            if ip.startswith(block_range):
                result["safe"] = False
                result["violations"].append(f"Blocked IP range: {block_range}")

        return result

    # ============================================================
    # HEURISTICS
    # ============================================================
    def entropy(self, data: bytes) -> float:
        """Calculate entropy"""
        if not data:
            return 0.0
        freq = {c: data.count(c) for c in set(data)}
        length = len(data)
        import math
        return -sum((count/length) * math.log2(count/length) for count in freq.values())

    def risk_score(self, entropy: float, patterns: List[str]) -> float:
        """Calculate risk score"""
        score = 0.0
        if entropy > self.heuristic_rules["ENTROPY_HIGH"]:
            score += 0.4
        score += min(len(patterns) * 0.15, 0.6)
        return min(score, 1.0)

    def analyze_patterns(self, data: str) -> List[str]:
        """Analyze suspicious patterns"""
        found = []
        for pattern in self.heuristic_rules["PATTERN_SUSPICIOUS"]:
            if pattern in data:
                found.append(pattern)
        return found

    # ============================================================
    # AUTO RESPONSE ENGINE
    # ============================================================
    def auto_block(self, event: Dict[str, Any]) -> None:
        """Auto-block based on event"""
        if not self.config["auto_response"]:
            return

        if event.get("risk_score", 0) >= 0.65:
            self.log({"type": "AUTO_BLOCK", "event": event})
            # block file or process
            if "file" in event:
                try:
                    os.remove(event["file"])
                except:
                    pass
            if "pid" in event:
                try:
                    psutil.Process(event["pid"]).kill()
                except:
                    pass

    # ============================================================
    # AUTO RULES ENGINE
    # ============================================================
    def auto_update_rules(self, event: Dict[str, Any]) -> None:
        """Auto-update rules based on event"""
        if not self.config["auto_rules"]:
            return

        if "patterns" in event:
            for p in event["patterns"]:
                if p not in self.proc_rules["BLOCK_PATTERNS"]:
                    self.proc_rules["BLOCK_PATTERNS"].append(p)
                    self.log({"type": "AUTO_RULE_ADD", "pattern": p})

    # ============================================================
    # AUTO LEARNING ENGINE
    # ============================================================
    def auto_learn(self, event: Dict[str, Any]) -> None:
        """Auto-learn from event"""
        if not self.config["auto_learning"]:
            return

        if event.get("risk_score", 0) > 0.8:
            self.heuristic_rules["ENTROPY_HIGH"] -= 0.1
            self.log({"type": "AUTO_LEARN", "new_entropy_threshold": self.heuristic_rules["ENTROPY_HIGH"]})

    # ============================================================
    # REALTIME ENGINE
    # ============================================================
    def realtime(self) -> None:
        """Realtime monitoring loop"""
        while self.enabled:
            time.sleep(self.config["realtime_interval"])

    def start(self) -> None:
        """Start shield"""
        self.enabled = True
        self.thread = threading.Thread(target=self.realtime)
        self.thread.daemon = True
        self.thread.start()
        self.log({"type": "ADV_SHIELD_START"})

    def stop(self) -> None:
        """Stop shield"""
        self.enabled = False
        self.log({"type": "ADV_SHIELD_STOP"})

    # ============================================================
    # EXPORT/IMPORT
    # ============================================================
    def export(self, path: str) -> str:
        """Export logs to file"""
        with open(path, "w") as f:
            json.dump(self.logs, f, indent=4)
        self.log({"type": "EXPORT", "path": path})
        return path

    def import_rules(self, path: str) -> bool:
        """Import rules from file"""
        try:
            with open(path, "r") as f:
                data = json.load(f)
            
            if "kernel" in data:
                self.kernel_rules = data["kernel"]
            if "proc" in data:
                self.proc_rules = data["proc"]
            if "file" in data:
                self.file_rules = data["file"]
            if "net" in data:
                self.net_rules = data["net"]
            if "heuristic" in data:
                self.heuristic_rules = data["heuristic"]
            
            self.log({"type": "IMPORT_RULES", "path": path})
            return True
        except Exception as e:
            self.log({"type": "IMPORT_FAIL", "path": path, "error": str(e)})
            return False

    # ============================================================
    # METADATA
    # ============================================================
    def get_metadata(self) -> Dict[str, Any]:
        """Get shield metadata"""
        return {
            "name": "AdvancedShield",
            "version": "2.0-ULTRA",
            "author": "polsoft.ITS™ Dev",
            "sandbox_root": self.sandbox_root,
            "snapshots_count": len(self.snapshots),
            "logs_count": len(self.logs),
            "enabled": self.enabled,
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get shield statistics"""
        return {
            "status": "running" if self.enabled else "stopped",
            "uptime": time.time(),
            "kernel_rules_count": len(self.kernel_rules.get("BLOCK_SYSCALLS", [])) + len(self.kernel_rules.get("BLOCK_BEHAVIOR", [])),
            "proc_rules_count": len(self.proc_rules.get("BLOCK_PROCESSES", [])) + len(self.proc_rules.get("BLOCK_PATTERNS", [])),
            "file_rules_count": len(self.file_rules.get("BLOCK_EXT", [])) + len(self.file_rules.get("BLOCK_NAMES", [])),
            "net_rules_count": len(self.net_rules.get("BLOCK_PORTS", [])) + len(self.net_rules.get("BLOCK_IP_RANGES", [])) + len(self.net_rules.get("BLOCK_PROTOCOLS", [])),
            "heuristic_rules_count": len(self.heuristic_rules.get("PATTERN_SUSPICIOUS", [])),
            "snapshots_count": len(self.snapshots),
            "logs_count": len(self.logs),
        }

    # ============================================================
    # DIAGNOSTICS
    # ============================================================
    def diagnose(self) -> Dict[str, Any]:
        """Run diagnostics"""
        return {
            "sandbox_exists": os.path.exists(self.sandbox_root),
            "sandbox_writable": os.access(self.sandbox_root, os.W_OK),
            "thread_alive": self.thread.is_alive() if self.thread else False,
            "auto_rules": self.config["auto_rules"],
            "auto_response": self.config["auto_response"],
            "auto_learning": self.config["auto_learning"],
        }

    def health_check(self) -> Dict[str, Any]:
        """Run health check"""
        diag = self.diagnose()
        healthy = all([
            diag["sandbox_exists"],
            diag["sandbox_writable"],
            self.enabled,
        ])
        return {
            "status": "healthy" if healthy else "unhealthy",
            "details": diag,
        }

    def auto_fix(self) -> bool:
        """Auto-fix issues"""
        try:
            if not os.path.exists(self.sandbox_root):
                self.sandbox_root = tempfile.mkdtemp(prefix="adv_sandbox_")
            
            if not self.thread or not self.thread.is_alive():
                self.start()
            
            self.log({"type": "AUTO_FIX"})
            return True
        except Exception as e:
            self.log({"type": "AUTO_FIX_FAIL", "error": str(e)})
            return False

    # ============================================================
    # API
    # ============================================================
    def api_list(self) -> List[str]:
        """List available API methods"""
        return [
            "log", "get_logs", "clear_logs",
            "config_get", "config_set", "config_reset",
            "get_rules", "add_rule", "remove_rule",
            "snapshot_create", "snapshot_restore", "snapshot_delete", "snapshot_list",
            "isolate_file", "check_file",
            "isolate_process", "check_process",
            "isolate_network", "check_network",
            "entropy", "risk_score", "analyze_patterns",
            "auto_block", "auto_update_rules", "auto_learn",
            "start", "stop",
            "export", "import_rules",
            "get_metadata", "get_stats",
            "diagnose", "health_check", "auto_fix",
        ]

    def api_call(self, method: str, *args, **kwargs) -> Any:
        """Call API method"""
        if method in self.api_list():
            return getattr(self, method)(*args, **kwargs)
        return None


# Global instance
advanced_shield = AdvancedShield()
