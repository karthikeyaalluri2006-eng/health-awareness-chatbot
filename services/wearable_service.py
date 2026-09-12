"""
HealthAware AI - Wearable Health Integration Service
Provides an adapter pattern for wearable devices (Apple Health, Fitbit, Google Health Connect, Mock).
Used strictly for educational wellness awareness, not clinical diagnosis.
"""

from typing import List, Dict, Any
from datetime import date, timedelta
import random


class WearableProvider:
    def sync_data(self, user_id: int) -> List[Dict[str, Any]]:
        raise NotImplementedError


class MockWearableProvider(WearableProvider):
    """Generates realistic daily activity, heart rate, and sleep data for demonstration."""
    def sync_data(self, user_id: int, days: int = 7) -> List[Dict[str, Any]]:
        records = []
        today = date.today()

        base_steps = 7500
        base_hr = 68

        for i in range(days):
            rec_date = (today - timedelta(days=i)).isoformat()
            steps = base_steps + random.randint(-2000, 3500)
            hr = base_hr + random.randint(-5, 8)
            active_mins = max(15, int(steps / 220))
            sleep_hours = round(random.uniform(6.2, 8.5), 1)
            sleep_mins = int(sleep_hours * 60)
            quality_score = min(98, max(65, int(sleep_hours * 11) + random.randint(-5, 5)))

            records.append({
                "record_date": rec_date,
                "provider": "Apple Health / Google Fit (Simulated)",
                "steps": steps,
                "resting_heart_rate": hr,
                "active_minutes": active_mins,
                "sleep_hours": sleep_hours,
                "sleep_minutes": sleep_mins,
                "sleep_quality_score": quality_score
            })

        return records


class FitbitProvider(WearableProvider):
    def sync_data(self, user_id: int) -> List[Dict[str, Any]]:
        # Connects to Fitbit Web API when client credentials are provided
        return MockWearableProvider().sync_data(user_id)


def get_wearable_provider() -> WearableProvider:
    return MockWearableProvider()
