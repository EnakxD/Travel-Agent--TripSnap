# main.py
"""
Run a local demo of the WhatsApp Travel Planner agent pipeline.
You can place sample .txt files under 'sample_inputs/' that mimic WhatsApp OCR output,
or point to real images (if you replace the OCR stub).
"""
import argparse
from orchestrator import Orchestrator
from pathlib import Path

def demo():
    orch = Orchestrator()

    sample_dir = Path("sample_inputs")
    # If you have prepared .txt stubs, read all; else pass an empty list to use the default stub text.
    if sample_dir.exists():
        inputs = [str(p) for p in sample_dir.glob("*") if p.suffix in (".txt", ".png", ".jpg", ".jpeg")]
    else:
        inputs = []

    result = orch.handle_upload(inputs)
    print("Trip ID:", result["trip_id"])
    print("Trip Info (extracted):")
    print(result["trip_info"])
    print("Package saved to:", result["package"])
    print("\nOpen sample_outputs/ to view generated JSON/PDF (or .txt fallback).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Run demo pipeline")
    args = parser.parse_args()
    demo()
