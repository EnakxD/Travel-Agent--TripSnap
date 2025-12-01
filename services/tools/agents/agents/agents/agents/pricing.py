# agents/pricing.py
from typing import Dict, Any

class PricingAgent:
    """
    Mocks or estimates costs for flight, hotel, activities.
    Replace mock logic with real search API calls (Skyscanner, Google Flights, hotel APIs).
    """
    def __init__(self, search_tool=None):
        self.search_tool = search_tool  # inject search API if available

    def estimate_costs(self, trip_info: Dict[str, Any], itinerary) -> Dict[str, Any]:
        # simple heuristics:
        people = trip_info.get("group_size") or 2
        budget_token = trip_info.get("budget") or "15000"
        try:
            # attempt to extract number from budget_token
            import re
            digits = re.findall(r'\d+', str(budget_token))
            base = int(digits[0]) if digits else 15000
        except Exception:
            base = 15000

        flights = int(base * 0.6)
        hotel = int((base * 0.25) * (len(itinerary) if itinerary else 3))
        activities = int(base * 0.15)

        return {
            "per_person_estimate": {
                "flights": flights,
                "hotel_total": hotel,
                "activities": activities,
                "total_estimate": flights + hotel + activities
            },
            "group_estimate": {
                "total": (flights + hotel + activities) * people
            },
            "notes": "Estimates are mocked. Replace with real search-based pricing for production."
        }
