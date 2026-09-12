"""
HealthAware AI - Healthcare Directory Service
Facilitates searching for nearby hospitals, clinics, 24/7 pharmacies, and diagnostic labs.
Provides external web direction links (No JavaScript maps).
"""

from typing import List, Dict, Any, Optional
import urllib.parse
from sqlalchemy.orm import Session
from database.repositories import HealthcareServiceRepository


def _build_search_query(service: Any) -> str:
    """Create a robust Google Maps search string from healthcare data."""
    parts = [
        getattr(service, "name", ""),
        getattr(service, "address", ""),
        getattr(service, "city", ""),
        getattr(service, "state", ""),
    ]
    cleaned = []
    for value in parts:
        if value and str(value).strip():
            cleaned.append(str(value).strip())
    return ", ".join(cleaned) if cleaned else "healthcare facility"


def _build_map_url(service: Any) -> str:
    """Return a stable map URL that works in a browser and survives special characters."""
    location = _build_search_query(service)
    query = urllib.parse.quote_plus(location)
    return f"https://www.google.com/maps/search/?api=1&query={query}"


class HealthcareDirectoryService:
    @staticmethod
    def get_services(
        db: Session,
        category: Optional[str] = None,
        city: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        services = HealthcareServiceRepository.get_all(db, category=category, city=city, search=search_query)
        result = []
        for s in services:
            map_url = _build_map_url(s)

            result.append({
                "id": s.id,
                "name": s.name,
                "category": s.category.title(),
                "address": s.address,
                "city": s.city,
                "phone": s.phone,
                "open_hours": s.open_hours,
                "emergency_available": s.emergency_available,
                "map_url": map_url
            })
        return result
