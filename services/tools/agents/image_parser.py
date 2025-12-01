# agents/image_parser.py
from typing import List, Dict
from tools.ocr_tools import ocr_image_stub, parse_chat_bubbles_from_text

class ImageParsingAgent:
    """
    Converts uploaded screenshots into structured chat transcripts.
    Replace ocr_image_stub with production OCR call when ready.
    """
    def __init__(self, ocr_func=None):
        self.ocr_func = ocr_func or ocr_image_stub

    def parse_images(self, image_paths: List[str]) -> List[Dict]:
        """
        Accepts list of file paths (images or .txt stubs). Returns chronological
        transcript as list of {"sender","timestamp","message"}.
        """
        transcript = []
        for p in image_paths:
            raw = self.ocr_func(p)
            bubbles = parse_chat_bubbles_from_text(raw)
            transcript.extend(bubbles)
        # In production you should sort by timestamp; here we assume upload order
        return transcript
