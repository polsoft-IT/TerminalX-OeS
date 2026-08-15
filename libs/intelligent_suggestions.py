"""
 ============================================================
  MODULE/PLUGIN NAME: IntelligentSuggestions
  VERSION: 1.0.0
  MODULE CLASS: IntelligentSuggestions
  DESCRIPTION:
       Intelligent command suggestions for TerminalX

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

from typing import List, Dict, Optional, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass
from libs.clean_logger import CleanLogger, LogLevel
from libs.command_prediction import CommandPredictor, Prediction


@dataclass
class Suggestion:
    """Command suggestion"""
    command: str
    reason: str
    confidence: float
    category: str


class IntelligentSuggestionEngine:
    """Intelligent suggestion engine"""
    
    def __init__(self, logger: Optional[CleanLogger] = None):
        """
        Initialize suggestion engine
        
        Args:
            logger: Logger instance
        """
        self.logger = logger or CleanLogger("SuggestionEngine", LogLevel.INFO)
        self.command_predictor = CommandPredictor()
        self.context_patterns: Dict[str, List[str]] = defaultdict(list)
        self.error_corrections: Dict[str, str] = {}
        self.command_aliases: Dict[str, List[str]] = defaultdict(list)
        
        # Initialize common patterns
        self._initialize_patterns()
        
    def _initialize_patterns(self) -> None:
        """Initialize common command patterns"""
        self.context_patterns['file_operations'] = [
            'ls', 'cd', 'cp', 'mv', 'rm', 'mkdir', 'touch', 'find'
        ]
        self.context_patterns['network'] = [
            'ping', 'curl', 'wget', 'ssh', 'net', 'traceroute'
        ]
        self.context_patterns['system'] = [
            'ps', 'top', 'kill', 'df', 'du', 'systemctl'
        ]
        self.context_patterns['git'] = [
            'git', 'clone', 'commit', 'push', 'pull', 'branch'
        ]
        self.context_patterns['development'] = [
            'python', 'npm', 'pip', 'make', 'gcc', 'vim'
        ]
        
        # Common typos and corrections
        self.error_corrections = {
            'ls -la': 'ls -la',
            'grpe': 'grep',
            'gerp': 'grep',
            'miv': 'vim',
            'cd..': 'cd ..',
            'cd ~/': 'cd ~',
            'cls': 'clear',
            'exi': 'exit',
            'quit': 'exit',
            'sudo !!': 'sudo $(history -p !!)'
        }
        
    def get_suggestions(self, current_input: str, context: str = '', 
                       top_k: int = 5) -> List[Suggestion]:
        """
        Get intelligent suggestions
        
        Args:
            current_input: Current command input
            context: Context information
            top_k: Number of suggestions
            
        Returns:
            List of suggestions
        """
        suggestions = []
        
        # Check for typos
        typo_correction = self._check_typo(current_input)
        if typo_correction:
            suggestions.append(Suggestion(
                command=typo_correction,
                reason="Typo correction",
                confidence=0.9,
                category="correction"
            ))
            
        # Get predictions from command predictor
        predictions = self.command_predictor.predict_next(current_input, top_k)
        for pred in predictions:
            suggestions.append(Suggestion(
                command=pred.command,
                reason=f"Based on history ({pred.context})",
                confidence=pred.confidence,
                category="prediction"
            ))
            
        # Get context-based suggestions
        context_suggestions = self._get_context_suggestions(context, current_input)
        for cmd, reason in context_suggestions:
            suggestions.append(Suggestion(
                command=cmd,
                reason=reason,
                confidence=0.7,
                category="context"
            ))
            
        # Get similar commands
        similar = self.command_predictor.get_similar_commands(current_input, top_k)
        for cmd, similarity in similar:
            suggestions.append(Suggestion(
                command=cmd,
                reason=f"Similar command ({similarity:.2f})",
                confidence=similarity,
                category="similarity"
            ))
            
        # Sort by confidence and limit
        suggestions.sort(key=lambda x: x.confidence, reverse=True)
        return suggestions[:top_k]
        
    def _check_typo(self, input_text: str) -> Optional[str]:
        """
        Check for common typos
        
        Args:
            input_text: Input text
            
        Returns:
            Corrected text or None
        """
        for typo, correction in self.error_corrections.items():
            if typo.lower() in input_text.lower():
                return correction
        return None
        
    def _get_context_suggestions(self, context: str, current_input: str) -> List[Tuple[str, str]]:
        """
        Get context-based suggestions
        
        Args:
            context: Context string
            current_input: Current input
            
        Returns:
            List of (command, reason) tuples
        """
        suggestions = []
        
        # Match context to patterns
        for pattern_name, commands in self.context_patterns.items():
            if pattern_name in context.lower():
                for cmd in commands:
                    if cmd.startswith(current_input) or current_input in cmd:
                        suggestions.append((cmd, f"Common {pattern_name} command"))
                        
        return suggestions
        
    def add_alias(self, command: str, alias: str) -> None:
        """
        Add command alias
        
        Args:
            command: Original command
            alias: Alias
        """
        self.command_aliases[command].append(alias)
        self.logger.info(f"Added alias: {alias} -> {command}")
        
    def get_aliases(self, command: str) -> List[str]:
        """
        Get aliases for command
        
        Args:
            command: Command name
            
        Returns:
            List of aliases
        """
        return self.command_aliases.get(command, [])
        
    def expand_alias(self, alias: str) -> Optional[str]:
        """
        Expand alias to full command
        
        Args:
            alias: Alias to expand
            
        Returns:
            Full command or None
        """
        for command, aliases in self.command_aliases.items():
            if alias in aliases:
                return command
        return None
        
    def learn_from_history(self, command_history: List[str]) -> None:
        """
        Learn from command history
        
        Args:
            command_history: List of commands
        """
        for cmd in command_history:
            self.command_predictor.add_command(cmd)
            
    def add_context_pattern(self, name: str, commands: List[str]) -> None:
        """
        Add context pattern
        
        Args:
            name: Pattern name
            commands: List of commands
        """
        self.context_patterns[name] = commands
        self.logger.info(f"Added context pattern: {name}")
        
    def add_error_correction(self, typo: str, correction: str) -> None:
        """
        Add error correction
        
        Args:
            typo: Common typo
            correction: Corrected version
        """
        self.error_corrections[typo] = correction
        self.logger.info(f"Added error correction: {typo} -> {correction}")
        
    def get_stats(self) -> Dict[str, any]:
        """
        Get suggestion engine statistics
        
        Returns:
            Statistics dictionary
        """
        predictor_stats = self.command_predictor.get_statistics()
        
        return {
            'context_patterns': len(self.context_patterns),
            'error_corrections': len(self.error_corrections),
            'command_aliases': len(self.command_aliases),
            'predictor_stats': predictor_stats
        }
        
    def clear_history(self) -> None:
        """Clear learning history"""
        self.command_predictor.clear_history()
        self.logger.info("Cleared suggestion history")


# Global suggestion engine instance
intelligent_suggestions = IntelligentSuggestionEngine()
