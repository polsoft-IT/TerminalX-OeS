"""
 ============================================================
  MODULE/PLUGIN NAME: AISentinel
  VERSION: 1.0.0
  MODULE CLASS: AISentinel
  DESCRIPTION:
       AI-powered security monitoring for anomaly detection and threat analysis

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
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class AlertSeverity(Enum):
    """Alert severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnomalyType(Enum):
    """Anomaly types"""
    SPIKE = "spike"
    DROP = "drop"
    TREND = "trend"
    OUTLIER = "outlier"
    PATTERN = "pattern"


class AISentinel:
    """AI-powered security sentinel"""
    
    def __init__(self):
        self.enabled = False
        self.alerts: List[Dict] = []
        self.thresholds: Dict[str, Dict] = {}
        self.baseline: Dict[str, Any] = {}
        self.monitoring_tasks: List[asyncio.Task] = []
        self.notification_callback = None
        self.stats = {
            'total_alerts': 0,
            'anomalies_detected': 0,
            'metrics_monitored': 0,
        }
        
    async def initialize(self, config: Dict[str, Any] = None):
        """Initialize sentinel"""
        self.config = config or {}
        self.enabled = self.config.get('enabled', False)
        self.thresholds = self.config.get('thresholds', {})
        
    def set_notification_callback(self, callback):
        """Set callback for sentinel notifications"""
        self.notification_callback = callback
        
    async def monitor(self, metrics: Dict[str, Any]) -> Optional[Dict]:
        """Monitor metrics for anomalies"""
        if not self.enabled:
            return None
            
        self.stats['metrics_monitored'] += 1
        anomalies = await self._detect_anomalies(metrics)
        
        if anomalies:
            self.stats['anomalies_detected'] += len(anomalies)
            alert = {
                'id': f"alert_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                'timestamp': datetime.now().isoformat(),
                'type': 'anomaly',
                'severity': self._calculate_severity(anomalies),
                'anomalies': anomalies,
                'metrics': metrics,
            }
            self.alerts.append(alert)
            self.stats['total_alerts'] += 1
            
            # Send notification
            if self.notification_callback:
                await self.notification_callback(
                    f"Anomaly detected: {len(anomalies)} anomalies",
                    f"Severity: {alert['severity']}",
                    'security',
                    alert['severity']
                )
            
            return alert
            
        return None
        
    async def _detect_anomalies(self, metrics: Dict[str, Any]) -> List[Dict]:
        """Detect anomalies in metrics"""
        anomalies = []
        
        for key, value in metrics.items():
            if key in self.thresholds:
                threshold = self.thresholds[key]
                
                if isinstance(value, (int, float)):
                    if value > threshold.get('max', float('inf')):
                        anomalies.append({
                            'metric': key,
                            'value': value,
                            'threshold': threshold['max'],
                            'type': AnomalyType.SPIKE.value,
                            'severity': AlertSeverity.HIGH.value,
                        })
                    elif value < threshold.get('min', float('-inf')):
                        anomalies.append({
                            'metric': key,
                            'value': value,
                            'threshold': threshold['min'],
                            'type': AnomalyType.DROP.value,
                            'severity': AlertSeverity.MEDIUM.value,
                        })
                        
        # Check for statistical anomalies based on baseline
        for key, value in metrics.items():
            if key in self.baseline and isinstance(value, (int, float)):
                baseline_stats = await self.get_baseline(key)
                if baseline_stats:
                    mean = baseline_stats['mean']
                    std = (max(baseline_stats['values']) - min(baseline_stats['values'])) / 4  # Approximate std
                    
                    if abs(value - mean) > 2 * std:
                        anomalies.append({
                            'metric': key,
                            'value': value,
                            'baseline_mean': mean,
                            'type': AnomalyType.OUTLIER.value,
                            'severity': AlertSeverity.MEDIUM.value,
                        })
                        
        return anomalies
        
    def _calculate_severity(self, anomalies: List[Dict]) -> str:
        """Calculate overall severity from anomalies"""
        if not anomalies:
            return AlertSeverity.LOW.value
            
        max_severity = AlertSeverity.LOW.value
        for anomaly in anomalies:
            severity = anomaly.get('severity', AlertSeverity.LOW.value)
            if severity == AlertSeverity.CRITICAL.value:
                return AlertSeverity.CRITICAL.value
            elif severity == AlertSeverity.HIGH.value:
                max_severity = AlertSeverity.HIGH.value
            elif severity == AlertSeverity.MEDIUM.value and max_severity == AlertSeverity.LOW.value:
                max_severity = AlertSeverity.MEDIUM.value
                
        return max_severity
        
    async def learn_baseline(self, metrics: Dict[str, Any]):
        """Learn baseline from metrics"""
        for key, value in metrics.items():
            if key not in self.baseline:
                self.baseline[key] = {'values': []}
                
            if isinstance(value, (int, float)):
                self.baseline[key]['values'].append(value)
                
                # Keep only last 100 values
                if len(self.baseline[key]['values']) > 100:
                    self.baseline[key]['values'] = self.baseline[key]['values'][-100:]
                    
    async def get_baseline(self, metric: str) -> Optional[Dict]:
        """Get baseline for metric"""
        if metric in self.baseline:
            values = self.baseline[metric]['values']
            if values:
                return {
                    'mean': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values),
                    'count': len(values),
                }
        return None
        
    async def get_alerts(self, limit: int = 100) -> List[Dict]:
        """Get recent alerts"""
        return self.alerts[-limit:]
        
    async def get_alert(self, alert_id: str) -> Optional[Dict]:
        """Get specific alert by ID"""
        for alert in self.alerts:
            if alert.get('id') == alert_id:
                return alert
        return None
        
    async def clear_alerts(self):
        """Clear all alerts"""
        self.alerts.clear()
        self.stats['total_alerts'] = 0
        
    async def set_threshold(self, metric: str, min_val: float = None, max_val: float = None, 
                          severity: str = 'medium'):
        """Set threshold for metric"""
        self.thresholds[metric] = {
            'min': min_val,
            'max': max_val,
            'severity': severity,
        }
        
    async def remove_threshold(self, metric: str) -> bool:
        """Remove threshold for metric"""
        if metric in self.thresholds:
            del self.thresholds[metric]
            return True
        return False
        
    async def start_monitoring(self, interval: int = 60):
        """Start continuous monitoring"""
        if not self.enabled:
            return
            
        task = asyncio.create_task(self._monitoring_loop(interval))
        self.monitoring_tasks.append(task)
        
    async def stop_monitoring(self):
        """Stop continuous monitoring"""
        for task in self.monitoring_tasks:
            task.cancel()
        self.monitoring_tasks.clear()
        
    async def _monitoring_loop(self, interval: int):
        """Monitoring loop for continuous monitoring"""
        while self.enabled:
            try:
                await asyncio.sleep(interval)
                # This would be called with actual metrics in a real implementation
                # await self.monitor(current_metrics)
            except asyncio.CancelledError:
                break
            except Exception:
                pass
                
    async def enable(self):
        """Enable sentinel"""
        self.enabled = True
        
    async def disable(self):
        """Disable sentinel"""
        self.enabled = False
        await self.stop_monitoring()
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get sentinel statistics"""
        return {
            'enabled': self.enabled,
            'total_alerts': self.stats['total_alerts'],
            'anomalies_detected': self.stats['anomalies_detected'],
            'metrics_monitored': self.stats['metrics_monitored'],
            'thresholds_configured': len(self.thresholds),
            'baselines_learned': len(self.baseline),
            'active_monitoring_tasks': len(self.monitoring_tasks),
        }
