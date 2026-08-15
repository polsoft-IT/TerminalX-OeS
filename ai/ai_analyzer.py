"""
 ============================================================
  MODULE/PLUGIN NAME: AIAnalyzer
  VERSION: 1.0.0
  MODULE CLASS: AIAnalyzer
  DESCRIPTION:
       AI-powered analysis tools for data processing and pattern recognition

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

import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class Sentiment(Enum):
    """Sentiment values"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class RiskLevel(Enum):
    """Risk levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Intent(Enum):
    """Command intents"""
    NAVIGATE = "navigate"
    LIST = "list"
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"
    NETWORK = "network"
    SYSTEM = "system"
    UNKNOWN = "unknown"


class AIAnalyzer:
    """AI-powered analyzer"""
    
    def __init__(self):
        self.patterns: Dict[str, List[str]] = {}
        self.rules: Dict[str, Any] = {}
        self.analysis_history: List[Dict] = []
        self.notification_callback = None
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize analyzer"""
        self.config = config or {}
        self.patterns = self.config.get('patterns', {})
        self.rules = self.config.get('rules', {})
        
    def set_notification_callback(self, callback):
        """Set callback for analyzer notifications"""
        self.notification_callback = callback
        
    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text"""
        results = {
            'sentiment': await self._analyze_sentiment(text),
            'entities': await self._extract_entities(text),
            'keywords': await self._extract_keywords(text),
            'language': await self._detect_language(text),
            'timestamp': datetime.now().isoformat(),
        }
        
        # Add to history
        self.analysis_history.append({
            'type': 'text_analysis',
            'input': text[:100],  # Truncate for history
            'results': results,
            'timestamp': datetime.now().isoformat(),
        })
        
        # Keep only last 100 analyses
        if len(self.analysis_history) > 100:
            self.analysis_history = self.analysis_history[-100:]
            
        return results
        
    async def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment"""
        # Extended sentiment analysis
        positive_words = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'awesome', 'brilliant', 'perfect', 'love', 'happy', 'success',
            'best', 'beautiful', 'incredible', 'outstanding', 'superb'
        ]
        negative_words = [
            'bad', 'terrible', 'awful', 'horrible', 'poor', 'worst',
            'hate', 'sad', 'failure', 'ugly', 'disappointing', 'frustrating',
            'annoying', 'disaster', 'catastrophe', 'unacceptable', 'broken'
        ]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return Sentiment.POSITIVE.value
        elif negative_count > positive_count:
            return Sentiment.NEGATIVE.value
        return Sentiment.NEUTRAL.value
        
    async def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities"""
        entities = {
            'emails': [],
            'urls': [],
            'ips': [],
            'phone_numbers': [],
            'dates': [],
            'credit_cards': [],
        }
        
        # Email addresses
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        entities['emails'] = emails
        
        # URLs
        urls = re.findall(r'https?://\S+', text)
        entities['urls'] = urls
        
        # IP addresses
        ips = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', text)
        entities['ips'] = ips
        
        # Phone numbers (simple pattern)
        phones = re.findall(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', text)
        entities['phone_numbers'] = phones
        
        # Credit card numbers (simple pattern - Luhn validation would be better)
        cards = re.findall(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', text)
        entities['credit_cards'] = cards
        
        return entities
        
    async def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords"""
        # Simple keyword extraction
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter common words (extended stop words)
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be', 
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 
            'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can', 
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 
            'they', 'what', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why', 'how'
        }
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Count frequency
        freq = {}
        for word in keywords:
            freq[word] = freq.get(word, 0) + 1
            
        # Return top keywords
        sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_keywords[:10]]
        
    async def _detect_language(self, text: str) -> str:
        """Detect language"""
        # Simple language detection based on character patterns
        if re.search(r'[\u4e00-\u9fff]', text):
            return 'chinese'
        elif re.search(r'[\u0400-\u04ff]', text):
            return 'russian'
        elif re.search(r'[\u0590-\u05ff]', text):
            return 'hebrew'
        elif re.search(r'[\u0600-\u06ff]', text):
            return 'arabic'
        elif re.search(r'[\u0370-\u03ff]', text):
            return 'greek'
        elif re.search(r'[\u0400-\u04ff]', text):
            return 'cyrillic'
        elif re.search(r'[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþß]', text):
            return 'european'
        else:
            return 'english'
            
    async def analyze_command(self, command: str) -> Dict[str, Any]:
        """Analyze command for safety and intent"""
        result = {
            'safe': await self._check_safety(command),
            'intent': await self._detect_intent(command),
            'risk_level': await self._assess_risk(command),
            'timestamp': datetime.now().isoformat(),
        }
        
        # Add to history
        self.analysis_history.append({
            'type': 'command_analysis',
            'input': command,
            'results': result,
            'timestamp': datetime.now().isoformat(),
        })
        
        # Send notification for unsafe commands
        if not result['safe'] and self.notification_callback:
            await self.notification_callback(
                f"Unsafe command detected: {command[:50]}",
                f"Risk level: {result['risk_level']}",
                'security',
                result['risk_level']
            )
        
        return result
        
    async def _check_safety(self, command: str) -> bool:
        """Check if command is safe"""
        dangerous_patterns = [
            r'rm\s+-rf\s+/',
            r'del\s+/f\s+/',
            r'format\s+[a-z]:',
            r'shutdown\s+',
            r'reboot\s+',
            r':(){:|:&};:',  # Fork bomb
            r'chmod\s+777',
            r'chown\s+root',
            r'wget.*\|.*sh',
            r'curl.*\|.*bash',
            r'eval\s*\(',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                return False
        return True
        
    async def _detect_intent(self, command: str) -> str:
        """Detect command intent"""
        cmd_lower = command.lower()
        
        if cmd_lower.startswith('cd') or 'pushd' in cmd_lower or 'popd' in cmd_lower:
            return Intent.NAVIGATE.value
        elif cmd_lower.startswith('ls') or cmd_lower.startswith('dir') or 'll' in cmd_lower:
            return Intent.LIST.value
        elif cmd_lower.startswith('cat') or cmd_lower.startswith('type') or cmd_lower.startswith('less') or cmd_lower.startswith('more'):
            return Intent.READ.value
        elif cmd_lower.startswith('mkdir') or cmd_lower.startswith('md') or 'touch' in cmd_lower:
            return Intent.WRITE.value
        elif cmd_lower.startswith('rm') or cmd_lower.startswith('del') or cmd_lower.startswith('rmdir'):
            return Intent.DELETE.value
        elif 'chmod' in cmd_lower or 'chown' in cmd_lower:
            return Intent.SYSTEM.value
        elif 'wget' in cmd_lower or 'curl' in cmd_lower or 'ssh' in cmd_lower or 'scp' in cmd_lower:
            return Intent.NETWORK.value
        elif './' in cmd_lower or cmd_lower.endswith('.sh') or cmd_lower.endswith('.exe'):
            return Intent.EXECUTE.value
        else:
            return Intent.UNKNOWN.value
            
    async def _assess_risk(self, command: str) -> str:
        """Assess risk level"""
        if not await self._check_safety(command):
            return RiskLevel.CRITICAL.value
        elif 'sudo' in command or 'admin' in command or 'root' in command:
            return RiskLevel.HIGH.value
        elif 'rm' in command or 'del' in command or 'format' in command:
            return RiskLevel.MEDIUM.value
        else:
            return RiskLevel.LOW.value
            
    async def get_history(self, limit: int = 50) -> List[Dict]:
        """Get analysis history"""
        return self.analysis_history[-limit:]
        
    async def clear_history(self):
        """Clear analysis history"""
        self.analysis_history.clear()
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get analyzer statistics"""
        return {
            'total_analyses': len(self.analysis_history),
            'text_analyses': sum(1 for a in self.analysis_history if a.get('type') == 'text_analysis'),
            'command_analyses': sum(1 for a in self.analysis_history if a.get('type') == 'command_analysis'),
        }
