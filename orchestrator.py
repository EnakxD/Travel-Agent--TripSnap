# orchestrator.py
import uuid
from agents.image_parser import ImageParsingAgent
from agents.task_extractor import TaskExtractionAgent
from agents.planner import PlanningAgent
from agents.pricing import PricingAgent
from agents.packager import ItineraryPackager
from services.memory_bank import MemoryBank

class Orchestrator:
    def __init__(self):
        self.memory = MemoryBank()
        self.image_parser = ImageParsingAgent()
        self.task_extractor = TaskExtractionAgent()
        self.planner = PlanningAgent()
        self.pricing = PricingAgent()
        self.packager = ItineraryPackager()

    def handle_upload(self, image_paths):
        """
        End-to-end pipeline: parse images -> extract trip info -> plan -> price -> package.
        Returns package paths.
        """
        trip_id = str(uuid.uuid4())[:8]
        # 1. parse images to transcript
        transcript = self.image_parser.parse_images(image_paths)
        # 2. extract trip info
        trip_info = self.task_extractor.extract_trip_info(transcript)
        # save preliminary state
        self.memory.save_trip(trip_id, {"transcript": transcript, "trip_info": trip_info})
        # 3. planning
        itinerary = self.planner.build_itinerary(trip_info)
        # 4. pricing
        pricing = self.pricing.estimate_costs(trip_info, itinerary)
        # 5. package
        package_paths = self.packager.package(trip_id, trip_info, itinerary, pricing)
        # update memory
        self.memory.update_trip(trip_id, {"itinerary": itinerary, "pricing": pricing, "package": package_paths})
        return {"trip_id": trip_id, "package": package_paths, "trip_info": trip_info}
