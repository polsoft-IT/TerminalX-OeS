"""
Process Analyzer - Process behavior analysis
"""

from typing import Dict, Any, List, Optional


class ProcessAnalyzer:
    """Process behavior analyzer"""
    
    def __init__(self):
        self.rules: Dict[str, Dict] = {}
        self.alerts: List[Dict] = {}
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize analyzer"""
        self.config = config or {}
        self.rules = self.config.get('rules', {})
        
    async def analyze(self, process_info: Dict) -> Dict[str, Any]:
        """Analyze process behavior"""
        return {
            'suspicious': await self._check_suspicious(process_info),
            'resource_heavy': await self._check_resources(process_info),
            'anomalies': await self._detect_anomalies(process_info),
            'risk_score': await self._calculate_risk(process_info),
        }
        
    async def _check_suspicious(self, process_info: Dict) -> bool:
        """Check if process is suspicious"""
        suspicious_names = [
            'miner', 'crypto', 'bitcoin', 'malware', 'trojan',
            'backdoor', 'rootkit', 'keylog'
        ]
        
        name = process_info.get('name', '').lower()
        cmdline = ' '.join(process_info.get('cmdline', [])).lower()
        
        for susp in suspicious_names:
            if susp in name or susp in cmdline:
                return True
                
        return False
        
    async def _check_resources(self, process_info: Dict) -> bool:
        """Check if process is resource heavy"""
        cpu = process_info.get('cpu_percent', 0)
        memory = process_info.get('memory_percent', 0)
        
        return cpu > 80 or memory > 80
        
    async def _detect_anomalies(self, process_info: Dict) -> List[str]:
        """Detect anomalies in process behavior"""
        anomalies = []
        
        # Check for unusual number of threads
        num_threads = process_info.get('num_threads', 0)
        if num_threads > 100:
            anomalies.append('high_thread_count')
            
        # Check for unusual number of file descriptors
        num_fds = process_info.get('num_fds', 0)
        if num_fds > 1000:
            anomalies.append('high_fd_count')
            
        # Check for hidden processes
        if not process_info.get('cmdline'):
            anomalies.append('no_cmdline')
            
        return anomalies
        
    async def _calculate_risk(self, process_info: Dict) -> float:
        """Calculate risk score (0-1)"""
        risk = 0.0
        
        if await self._check_suspicious(process_info):
            risk += 0.5
            
        if await self._check_resources(process_info):
            risk += 0.2
            
        anomalies = await self._detect_anomalies(process_info)
        risk += len(anomalies) * 0.1
        
        return min(risk, 1.0)
        
    async def compare_processes(self, pid1: int, pid2: int, 
                                history1: List, history2: List) -> Dict[str, Any]:
        """Compare two processes"""
        return {
            'cpu_diff': self._compare_metric(history1, history2, 'cpu_percent'),
            'memory_diff': self._compare_metric(history1, history2, 'memory_percent'),
            'similarity': self._calculate_similarity(history1, history2),
        }
        
    def _compare_metric(self, history1: List, history2: List, metric: str) -> float:
        """Compare a metric between two process histories"""
        if not history1 or not history2:
            return 0.0
            
        avg1 = sum(h.get(metric, 0) for h in history1) / len(history1)
        avg2 = sum(h.get(metric, 0) for h in history2) / len(history2)
        
        return abs(avg1 - avg2)
        
    def _calculate_similarity(self, history1: List, history2: List) -> float:
        """Calculate similarity between two process histories"""
        if not history1 or not history2:
            return 0.0
            
        # Simple similarity based on name and cmdline
        if history1 and history2:
            name1 = history1[0].get('name', '')
            name2 = history2[0].get('name', '')
            
            if name1 == name2:
                return 1.0
                
        return 0.0
