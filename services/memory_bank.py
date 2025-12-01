# services/memory_bank.py
from typing import Dict, Any

class MemoryBank:
    """
    Simple in-memory store for current trip sessions.
    """
    def __init__(self):
        self.trips: Dict[str, Dict[str, Any]] = {}

    def save_trip(self, trip_id: str, trip_data: Dict[str, Any]):
        self.trips[trip_id] = trip_data

    def get_trip(self, trip_id: str) -> Dict[str, Any]:
        return self.trips.get(trip_id, {})

    def update_trip(self, trip_id: str, updates: Dict[str, Any]):
        self.trips.setdefault(trip_id, {}).update(updates)
