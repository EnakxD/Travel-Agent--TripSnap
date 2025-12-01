# agents/packager.py
from typing import Dict, Any
from tools.save_tools import save_json, save_pdf_simple

class ItineraryPackager:
    """
    Combine itinerary, pricing and trip info and export JSON/PDF.
    """
    def __init__(self):
        pass

    def package(self, trip_id: str, trip_info: Dict[str, Any], itinerary, pricing) -> Dict[str, Any]:
        package = {
            "trip_id": trip_id,
            "summary": {
                "destinations": trip_info.get("destinations"),
                "dates": trip_info.get("start_end_dates"),
                "group_size": trip_info.get("group_size"),
                "budget": trip_info.get("budget")
            },
            "itinerary": itinerary,
            "pricing": pricing,
            "raw_notes": trip_info.get("raw_text")
        }
        path_json = save_json(package, f"itinerary_{trip_id}.json")
        # create a simple human-readable text and save pdf (or fallback to txt)
        pretty = f"Trip: {trip_info.get('destinations')} Dates: {trip_info.get('start_end_dates')}\n\nItinerary:\n"
        for d in itinerary:
            pretty += f"Day {d['day']}: {d['morning']} | {d['afternoon']} | {d['evening']}\n"
        pretty += f"\nPricing:\n{pricing}\n"
        path_pdf = save_pdf_simple(pretty, f"itinerary_{trip_id}.pdf")
        return {"json": path_json, "pdf": path_pdf}
