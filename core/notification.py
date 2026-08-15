"""
Notification System - Internal notification management for TerminalX
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from enum import Enum


class NotificationPriority(Enum):
    """Notification priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class NotificationType(Enum):
    """Notification types"""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    SYSTEM = "system"
    SECURITY = "security"
    NETWORK = "network"
    AI = "ai"


class Notification:
    """Single notification object"""
    
    def __init__(
        self,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.id = self._generate_id()
        self.title = title
        self.message = message
        self.type = notification_type
        self.priority = priority
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.read = False
        self.archived = False
        
    def _generate_id(self) -> str:
        """Generate unique notification ID"""
        return f"notif_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert notification to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'type': self.type.value,
            'priority': self.priority.value,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat(),
            'read': self.read,
            'archived': self.archived
        }
    
    def mark_read(self):
        """Mark notification as read"""
        self.read = True
    
    def mark_unread(self):
        """Mark notification as unread"""
        self.read = False
    
    def archive(self):
        """Archive notification"""
        self.archived = True
    
    def unarchive(self):
        """Unarchive notification"""
        self.archived = False


class NotificationSystem:
    """Notification system manager"""
    
    def __init__(self, max_notifications: int = 1000):
        self.notifications: List[Notification] = []
        self.max_notifications = max_notifications
        self.subscribers: List[Callable] = []
        self.enabled = True
        self._lock = asyncio.Lock()
        
    async def initialize(self):
        """Initialize notification system"""
        self.enabled = True
    
    async def shutdown(self):
        """Shutdown notification system"""
        self.enabled = False
        self.notifications.clear()
        self.subscribers.clear()
    
    async def create(
        self,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Notification:
        """Create a new notification"""
        async with self._lock:
            notification = Notification(
                title=title,
                message=message,
                notification_type=notification_type,
                priority=priority,
                metadata=metadata
            )
            
            # Add to notifications list
            self.notifications.append(notification)
            
            # Trim if exceeding max
            if len(self.notifications) > self.max_notifications:
                # Remove oldest archived notifications first
                archived = [n for n in self.notifications if n.archived]
                if archived:
                    self.notifications.remove(archived[0])
                else:
                    self.notifications.pop(0)
            
            # Notify subscribers
            await self._notify_subscribers(notification)
            
            return notification
    
    async def _notify_subscribers(self, notification: Notification):
        """Notify all subscribers of new notification"""
        for callback in self.subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(notification)
                else:
                    callback(notification)
            except Exception as e:
                print(f"Error notifying subscriber: {e}")
    
    def subscribe(self, callback: Callable):
        """Subscribe to new notifications"""
        self.subscribers.append(callback)
    
    def unsubscribe(self, callback: Callable):
        """Unsubscribe from notifications"""
        if callback in self.subscribers:
            self.subscribers.remove(callback)
    
    async def get_all(
        self,
        unread_only: bool = False,
        archived: bool = False,
        notification_type: Optional[NotificationType] = None,
        priority: Optional[NotificationPriority] = None
    ) -> List[Notification]:
        """Get notifications with filters"""
        async with self._lock:
            filtered = self.notifications
            
            if unread_only:
                filtered = [n for n in filtered if not n.read]
            
            if not archived:
                filtered = [n for n in filtered if not n.archived]
            
            if notification_type:
                filtered = [n for n in filtered if n.type == notification_type]
            
            if priority:
                filtered = [n for n in filtered if n.priority == priority]
            
            # Sort by created time (newest first)
            filtered.sort(key=lambda x: x.created_at, reverse=True)
            
            return filtered
    
    async def get_by_id(self, notification_id: str) -> Optional[Notification]:
        """Get notification by ID"""
        async with self._lock:
            for notification in self.notifications:
                if notification.id == notification_id:
                    return notification
            return None
    
    async def mark_read(self, notification_id: str) -> bool:
        """Mark notification as read"""
        async with self._lock:
            notification = await self.get_by_id(notification_id)
            if notification:
                notification.mark_read()
                return True
            return False
    
    async def mark_all_read(self) -> int:
        """Mark all notifications as read"""
        async with self._lock:
            count = 0
            for notification in self.notifications:
                if not notification.read:
                    notification.mark_read()
                    count += 1
            return count
    
    async def archive(self, notification_id: str) -> bool:
        """Archive notification"""
        async with self._lock:
            notification = await self.get_by_id(notification_id)
            if notification:
                notification.archive()
                return True
            return False
    
    async def delete(self, notification_id: str) -> bool:
        """Delete notification"""
        async with self._lock:
            notification = await self.get_by_id(notification_id)
            if notification:
                self.notifications.remove(notification)
                return True
            return False
    
    async def clear_all(self) -> int:
        """Clear all notifications"""
        async with self._lock:
            count = len(self.notifications)
            self.notifications.clear()
            return count
    
    async def clear_archived(self) -> int:
        """Clear all archived notifications"""
        async with self._lock:
            archived = [n for n in self.notifications if n.archived]
            count = len(archived)
            for notification in archived:
                self.notifications.remove(notification)
            return count
    
    async def get_unread_count(self) -> int:
        """Get count of unread notifications"""
        async with self._lock:
            return len([n for n in self.notifications if not n.read and not n.archived])
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get notification statistics"""
        async with self._lock:
            total = len(self.notifications)
            unread = len([n for n in self.notifications if not n.read and not n.archived])
            archived = len([n for n in self.notifications if n.archived])
            
            # Count by type
            type_counts = {}
            for notification in self.notifications:
                type_name = notification.type.value
                type_counts[type_name] = type_counts.get(type_name, 0) + 1
            
            # Count by priority
            priority_counts = {}
            for notification in self.notifications:
                priority_name = notification.priority.value
                priority_counts[priority_name] = priority_counts.get(priority_name, 0) + 1
            
            return {
                'total': total,
                'unread': unread,
                'archived': archived,
                'by_type': type_counts,
                'by_priority': priority_counts
            }
    
    async def export(self, filepath: str):
        """Export notifications to JSON file"""
        async with self._lock:
            data = [n.to_dict() for n in self.notifications]
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
    
    async def import_from(self, filepath: str):
        """Import notifications from JSON file"""
        async with self._lock:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            for item in data:
                notification = Notification(
                    title=item['title'],
                    message=item['message'],
                    notification_type=NotificationType(item['type']),
                    priority=NotificationPriority(item['priority']),
                    metadata=item.get('metadata', {})
                )
                notification.id = item['id']
                notification.read = item.get('read', False)
                notification.archived = item.get('archived', False)
                notification.created_at = datetime.fromisoformat(item['created_at'])
                self.notifications.append(notification)
