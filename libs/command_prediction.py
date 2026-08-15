"""
 ============================================================
  MODULE/PLUGIN NAME: CommandPrediction
  VERSION: 1.0.0
  MODULE CLASS: CommandPrediction
  DESCRIPTION:
       Command prediction based on history for TerminalX

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

from typing import List, Dict, Tuple, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass
from libs.clean_logger import CleanLogger, LogLevel


@dataclass
class Prediction:
    """Command prediction"""
    command: str
    confidence: float
    context: str


class CommandPredictor:
    """Command prediction system based on history"""
    
    def __init__(self, logger: Optional[CleanLogger] = None, max_history: int = 1000):
        """
        Initialize command predictor
        
        Args:
            logger: Logger instance
            max_history: Maximum history size
        """
        self.logger = logger or CleanLogger("CommandPredictor", LogLevel.INFO)
        self.max_history = max_history
        self.command_history: List[str] = []
        self.ngram_model: Dict[str, Counter] = defaultdict(Counter)
        self.context_model: Dict[str, List[str]] = defaultdict(list)
        self.frequency: Counter = Counter()
        
    def add_command(self, command: str, context: str = "") -> None:
        """
        Add command to history
        
        Args:
            command: Command string
            context: Context information
        """
        self.command_history.append(command)
        self.frequency[command] += 1
        
        # Trim history if needed
        if len(self.command_history) > self.max_history:
            removed = self.command_history.pop(0)
            self.frequency[removed] -= 1
            if self.frequency[removed] <= 0:
                del self.frequency[removed]
                
        # Update n-gram model
        words = command.split()
        for i in range(len(words) - 1):
            prefix = ' '.join(words[:i+1])
            next_word = words[i+1]
            self.ngram_model[prefix][next_word] += 1
            
        # Update context model
        if context:
            self.context_model[context].append(command)
            
    def predict_next(self, current_input: str, top_k: int = 5) -> List[Prediction]:
        """
        Predict next command based on current input
        
        Args:
            current_input: Current command input
            top_k: Number of predictions to return
            
        Returns:
            List of predictions
        """
        predictions = []
        words = current_input.split()
        
        if not words:
            # Return most frequent commands
            for cmd, count in self.frequency.most_common(top_k):
                total = sum(self.frequency.values())
                confidence = count / total
                predictions.append(Prediction(cmd, confidence, "frequency"))
            return predictions
            
        # Use n-gram model
        prefix = ' '.join(words)
        if prefix in self.ngram_model:
            for next_word, count in self.ngram_model[prefix].most_common(top_k):
                total = sum(self.ngram_model[prefix].values())
                confidence = count / total
                predicted_command = f"{prefix} {next_word}"
                predictions.append(Prediction(predicted_command, confidence, "ngram"))
                
        # Fall back to frequency if no n-gram predictions
        if not predictions:
            for cmd, count in self.frequency.most_common(top_k):
                if cmd.startswith(current_input):
                    total = sum(self.frequency.values())
                    confidence = count / total
                    predictions.append(Prediction(cmd, confidence, "prefix"))
                    
        return predictions[:top_k]
        
    def predict_context(self, context: str, top_k: int = 5) -> List[Prediction]:
        """
        Predict command based on context
        
        Args:
            context: Context information
            top_k: Number of predictions
            
        Returns:
            List of predictions
        """
        predictions = []
        
        if context in self.context_model:
            commands = self.context_model[context]
            counter = Counter(commands)
            
            for cmd, count in counter.most_common(top_k):
                total = len(commands)
                confidence = count / total
                predictions.append(Prediction(cmd, confidence, context))
                
        return predictions
        
    def get_similar_commands(self, command: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Get similar commands using simple string similarity
        
        Args:
            command: Command to match
            top_k: Number of similar commands
            
        Returns:
            List of (command, similarity) tuples
        """
        similarities = []
        
        for cmd in self.frequency.keys():
            similarity = self._calculate_similarity(command, cmd)
            if similarity > 0.5:
                similarities.append((cmd, similarity))
                
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
        
    def _calculate_similarity(self, s1: str, s2: str) -> float:
        """
        Calculate string similarity using Jaccard similarity
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            Similarity score (0-1)
        """
        set1 = set(s1.lower().split())
        set2 = set(s2.lower().split())
        
        if not set1 or not set2:
            return 0.0
            
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        return intersection / union if union > 0 else 0.0
        
    def get_statistics(self) -> Dict[str, any]:
        """
        Get predictor statistics
        
        Returns:
            Statistics dictionary
        """
        return {
            'total_commands': len(self.command_history),
            'unique_commands': len(self.frequency),
            'ngram_entries': len(self.ngram_model),
            'context_entries': len(self.context_model),
            'most_frequent': self.frequency.most_common(5)
        }
        
    def clear_history(self) -> None:
        """Clear command history"""
        self.command_history.clear()
        self.ngram_model.clear()
        self.context_model.clear()
        self.frequency.clear()
        self.logger.info("Command history cleared")
        
    def export_history(self, path: str) -> bool:
        """
        Export command history to file
        
        Args:
            path: Export path
            
        Returns:
            True if exported successfully
        """
        try:
            with open(path, 'w') as f:
                for cmd in self.command_history:
                    f.write(cmd + '\n')
            self.logger.info(f"History exported to {path}")
            return True
        except Exception as e:
            self.logger.error(f"Export failed: {e}")
            return False
            
    def import_history(self, path: str) -> bool:
        """
        Import command history from file
        
        Args:
            path: Import path
            
        Returns:
            True if imported successfully
        """
        try:
            with open(path, 'r') as f:
                for line in f:
                    command = line.strip()
                    if command:
                        self.add_command(command)
            self.logger.info(f"History imported from {path}")
            return True
        except Exception as e:
            self.logger.error(f"Import failed: {e}")
            return False


# Global command predictor instance
command_predictor = CommandPredictor()
