# agents/task_extractor.py
"""
Extract structured trip info from a chat transcript.
This is a stubbed rule-based extractor. Replace or augment with an LLM for
higher accuracy (eg. use prompt-based extraction with Gemini / OpenAI).
"""
from typing import List, Dict, Any
import re
from dateutil import parser as date_parser

class TaskExtractionAgent:
    def __init__(self):
        pass

    def extract_dates(self, text: str):
        # naive detection: looks for patterns like '12 March' or 'Jan 12-15'
        # For demo we try to parse first date-like token
        tokens = re.findall(r'\b\d{1,2}\s+\w+\b|\b\w+\s+\d{1,2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b', text, flags=re.IGNORECASE)
        parsed = []
        for t in tokens:
            try:
                d = date_parser.parse(t, fuzzy=True, dayfirst=True)
                parsed.append(d.date().isoformat())
            except Exception:
                continue
        return parsed

    def extract_budget(self, text: str):
        m = re.search(r'(\b₹?\s?\d{3,6}\b|\b\d{2,5}\s?(?:inr|rupees|rs|rs\.)\b|\bunder\s+\d{3,6}\b)', text, flags=re.IGNORECASE)
        return m.group(0) if m else None

    def extract_locations(self, text: str):
        # naive: capitalize words or known place keywords; for demo use simple heuristics
        # In production, call a geocoding/NER model.
        places = []
        candidates = re.findall(r'\b([A-Z][a-z]{2,})(?:\b|\s)', text)
        for c in candidates:
            # filter common words
            if c.lower() not in ("let", "we", "go", "the", "from"):
                places.append(c)
        return list(dict.fromkeys(places))  # dedupe preserving order

    def extract_trip_info(self, transcript: List[Dict]) -> Dict[str, Any]:
        """
        Assemble Trip Info JSON from transcript. For missing fields, leave None.
        """
        combined = " ".join([m["message"] for m in transcript])
        dates = self.extract_dates(combined)
        locations = self.extract_locations(combined)
        budget = self.extract_budget(combined)
        # group size detection
        m = re.search(r'\b(\d{1,2})\s*(people|ppl|persons)\b', combined, flags=re.IGNORECASE)
        group_size = int(m.group(1)) if m else None

        # preferences (keywords)
        prefs = []
        for k in ["beach", "trek", "hiking", "party", "shopping", "food", "temple", "scuba"]:
            if k in combined.lower():
                prefs.append(k)

        trip_info = {
            "raw_text": combined,
            "destinations": locations or None,
            "start_end_dates": dates or None,
            "group_size": group_size,
            "budget": budget,
            "preferences": prefs or None,
            "notes": "Extracted using rule-based stub. Replace with LLM/NER for production."
        }
        return trip_info
