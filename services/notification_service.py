"""
HealthAware AI - Notification Service
Provider abstraction for medication reminders, appointment alerts, and health tips.
"""

from typing import Dict, Any, List


class NotificationProvider:
    def send_notification(self, user_id: int, title: str, message: str, channel: str = "in_app") -> bool:
        raise NotImplementedError


class MockNotificationProvider(NotificationProvider):
    def __init__(self):
        self.sent_notifications: List[Dict[str, Any]] = []

    def send_notification(self, user_id: int, title: str, message: str, channel: str = "in_app") -> bool:
        self.sent_notifications.append({
            "user_id": user_id,
            "title": title,
            "message": message,
            "channel": channel
        })
        return True


_default_notifier = MockNotificationProvider()


def get_notification_provider() -> NotificationProvider:
    return _default_notifier
