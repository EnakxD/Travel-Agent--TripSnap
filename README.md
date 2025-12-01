# Travel-Agent--TripSnap
Turn WhatsApp screenshots into a complete travel itinerary
**Problem Statement:**
Planning a trip through WhatsApp group chats is messy and inefficient. Important details like dates, destinations, budgets, and preferences are buried inside long, unstructured conversations filled with screenshots, jokes, mixed opinions, and scattered messages. Travelers waste time manually scrolling through chats to extract the actual trip plan, often leading to confusion, miscommunication, and poor coordination. There is no tool that can automatically transform WhatsApp conversation screenshots into a structured, ready-to-use travel plan. This creates friction for users who simply want a clear itinerary without sorting through chaotic group messages.

**Solution Statement:**
a multimodal, agent-driven assistant that converts WhatsApp trip screenshots into a complete, actionable travel plan. Users upload screenshots; an Image Parsing Agent extracts chat text, timestamps and sender metadata with OCR and chat-bubble segmentation. A Task Extraction Agent turns raw text into structured entities (dates, destinations, budgets, preferences, constraints) and asks clarifying questions when information is missing. A Planning Agent produces a day-by-day itinerary that respects constraints and preferences, while a Pricing Agent (using web search or mock lookups) estimates flights, hotels, and activity costs. An Itinerary Agent composes the final deliverable — a shareable JSON/PDF with schedule, booking links, packing list and budget summary — and a Memory/Session service stores trip context for edits. The system logs agent actions for observability and supports a lightweight web UI (Streamlit/Gradio) for uploads and quick edits. Output: a ready-to-use trip plan generated in minutes from noisy group chat screenshots.

<img width="1332" height="940" alt="WhatsTrip Agent System Diagram (2)" src="https://github.com/user-attachments/assets/809067cd-d20b-4871-92dd-82e32cefa1a1" />
**Architecture:**
Core to the Travel Planner Agent is the travel_orchestrator_agent — a clear demonstration of how multimodal, multi-agent systems outperform single-model solutions. Instead of being a single block of logic, the system is an ecosystem of specialized, cooperative agents, each responsible for a distinct stage of the travel-planning pipeline. This modular, composable setup allows the agent to intelligently convert chaotic WhatsApp screenshots into a polished, structured travel itinerary. The orchestrator of this ecosystem is the interactive_travel_agent, which delegates tasks to the appropriate expert sub-agents.

The interactive_travel_agent uses the Agent class from the ADK and defines key components such as its name, reasoning model, high-level instructions, and—most importantly—the specialized sub_agents and tools available to it. Instead of handling all tasks itself, it intelligently routes different parts of the workflow to the appropriate expert agent. This separation of responsibilities creates a resilient, extensible architecture capable of handling complex multimodal and text-understanding tasks.

Below are the core agents and their roles in the system:

1. Image Parsing Agent: whatsapp_image_parser
This is the system’s multimodal entry point. Its role is to transform noisy WhatsApp screenshots into clean, structured text. Using OCR and bubble-detection logic, it extracts: sender names, message timestamps ,message text ,emojis ,inline media descriptions ,conversation threading
The result is a machine-readable, chronological conversation transcript.
This agent is implemented as a LoopAgent, allowing multiple passes if the OCR quality is low or if validation flags missing timestamps. A ChatOCRValidationChecker ensures the extracted text meets basic accuracy before sending it downstream.

2. Task Extraction Agent: travel_info_extractor
Once the raw transcript is created, this agent identifies all trip-related entities. Its job is to convert unstructured conversation text into structured travel data. It extracts:
destination(s) ,travel dates, number of travelers, budget constraints, hotel preferences ,activity interests
special conditions (e.g., “no trekking”, “budget-friendly hotels”, “veg food only”)
It uses a combination of NER, reasoning prompts, and pattern-based extraction.
This agent is also a LoopAgent, paired with a TripInfoValidationChecker that verifies whether the extracted JSON contains all required fields. If the data is incomplete, the LoopAgent retries with a refined prompt.

3. Planning Agent: day_wise_itinerary_planner
Once the trip information JSON is validated, control moves to the itinerary planner. This agent is responsible for generating a realistic, enjoyable day-wise itinerary. Its planning considers: flight/arrival times,  local commute times,  weather,  tourist attraction distances,  budget constraints , user preferences (adventure, shopping, culture, food, nightlife)  
It creates a chronological schedule for each day, including morning, afternoon, and night activities along with suggested landmarks, restaurants, and travel durations.
Built as a Sequential Agent, it guarantees a consistent flow from extracted data → itinerary generation.

4. Pricing Agent: travel_cost_estimator
The itinerary is then passed to a pricing agent, which estimates real-world costs using: search tool calls (flight prices, hotel rates), mock lookups for activities, local travel cost heuristics, currency conversion tools,
It returns a structured budget breakdown, including total estimated cost per person and for the whole group.
This agent uses a combination of built-in Google Search tools and custom pricing logic. If searches fail or return incomplete data, the CostValidationChecker forces a retry.

5. Itinerary Packaging Agent: final_itinerary_builder

The last step is transforming all the structured pieces into a clean, user-ready travel plan.
This agent merges: trip summary (destination, dates, group size), structured day-wise itinerary, pricing breakdown, packing checklist, weather overview, map links, recommended bookings
It exports the final output as: JSON, PDF, Shareable message format (WhatsApp-friendly text), Optional HTML version,
Because this agent has no retries needed, it's a standard Agent, but is equipped with file-generation tools.

6.Essential Tools and Utilities
1)OCR Tool (extract_whatsapp_text):
A custom OCR pipeline optimized for chat bubbles, margins, and message separators.

2)Search Tool (google_flights_search, hotel_price_search):
Used by the Pricing Agent to estimate real-world travel costs.

3)Validation Checkers (ChatOCRValidationChecker, TripInfoValidationChecker, CostValidationChecker):
These ensure reliability by validating extracted data at each stage.
If validation fails, the LoopAgent repeats its step automatically.

7.State & Memory (TripContextStore)
A simple session store that allows:
1)multi-step refinement
2)persistent trip context
3)user edits (“change hotel type”, “replace Day 2 activity”)

**Conclusion:**
The WhatsApp Travel Planner Agent transforms scattered, unstructured chat screenshots into a complete, usable travel itinerary through a coordinated team of multimodal and reasoning agents. By combining image parsing, structured information extraction, intelligent planning, real-time pricing, and itinerary packaging, it eliminates the messiness of group travel planning and turns it into a seamless, automated experience. This project demonstrates the power of multi-agent systems in solving real-world problems and highlights how AI can bring order, clarity, and efficiency to everyday tasks like planning a trip.

**Value Statement:**
The WhatsApp Travel Planner Agent saves users hours of manual coordination by automatically turning messy WhatsApp conversations into a structured, ready-to-use travel plan. It removes confusion, reduces planning errors, and delivers instant clarity—providing a personalized itinerary, budget estimates, and activity suggestions without the user needing to enter any information manually. This creates a smooth, stress-free planning experience that traditional apps and tools cannot offer.

How to run (quick)

Save the files using the layout above.

(Optional) create sample_inputs/sample1.txt with lines like:
Riya: Let's go to Goa from 12 March to 15 March.
Aman: ₹15000 per person is fine.
Neha: We are 4 people.
Riya: Beach and party preferred.

Create & activate venv, install:
python -m venv venv
# linux/mac
source venv/bin/activate
# windows
# venv\Scripts\activate
pip install -r requirements.txt

Run:
python main.py --demo

Notes & next steps (what to replace to make production-ready)

OCR: replace ocr_image_stub with pytesseract.image_to_string() or Google Vision API for accurate OCR. Add a chat-bubble segmentation model to split messages properly from screenshots.

Extraction: the TaskExtractionAgent is rule-based. For high accuracy, replace with an LLM prompt-based extractor (send transcript to LLM and ask it to return structured JSON). This yields far better date/location/budget parsing (handles messy natural language).

Planning: replace PlanningAgent.build_itinerary with an LLM planner that reasons about time, distance, opening hours, and fatigue; or use a hybrid approach: LLM for semantic planning + heuristics for time/distance.

Pricing: replace PricingAgent mock with calls to flight/hotel search APIs or run web.run (when allowed) to fetch real rates.

Validation & Clarification: add a clarifying-question loop: if required info is missing, the system should ask the user (via UI) and update trip_info.

Observability / Logging: add structured logs and counters per agent to show traceability for judges.

Session & Memory: persist memory to a simple DB (sqlite) or memory bank across sessions for edits.
UI: add Streamlit/Gradio front-end to upload images and present the itinerary. Include an "edit itinerary" flow.




