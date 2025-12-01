# agents/planner.py
from typing import Dict, Any, List
import datetime

class PlanningAgent:
    """
    Builds a simple day-wise itinerary from Trip Info.
    In production replace with a planning LLM that considers travel times, attractions, etc.
    """
    def __init__(self):
        pass

    def build_itinerary(self, trip_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        # crude default: if dates found, fill days; else assume 3 days
        dates = trip_info.get("start_end_dates") or []
        if len(dates) >= 2:
            try:
                start = datetime.date.fromisoformat(dates[0])
                end = datetime.date.fromisoformat(dates[-1])
                num_days = (end - start).days + 1
            except Exception:
                num_days = 3
        else:
            num_days = 3

        dest = trip_info.get("destinations")[0] if trip_info.get("destinations") else "Destination"
        prefs = trip_info.get("preferences") or []

        itinerary = []
        for i in range(1, num_days + 1):
            day_plan = {
                "day": i,
                "date": None,
                "morning": f"Arrival & settle in at {dest}" if i == 1 else f"Explore local attractions in {dest}",
                "afternoon": "Recommended activity: " + (prefs[0] if prefs else "sightseeing"),
                "evening": "Local dinner and rest",
            }
            itinerary.append(day_plan)
        return itinerary
