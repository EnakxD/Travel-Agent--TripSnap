# tools/ocr_tools.py
"""
OCR helpers. By default this file provides a 'stub' OCR that reads text from .txt
files in sample_inputs for easy demos. Replace with pytesseract or Google Vision
in production. See commented example for using pytesseract.
"""
from pathlib import Path
from typing import List, Dict

def ocr_image_stub(path: str) -> str:
    """
    Demo stub: if path ends with .txt, read it and treat as 'extracted text'.
    If a real image, return placeholder text. Replace this with real OCR.
    """
    p = Path(path)
    if p.suffix == ".txt" and p.exists():
        return p.read_text(encoding="utf-8")
    return "User: let's go to Goa from 12 March to 15 March. Budget 15000 per person. 4 of us."

# Example using pytesseract (production)
# from PIL import Image
# import pytesseract
# def ocr_image_pytesseract(path: str) -> str:
#     img = Image.open(path)
#     text = pytesseract.image_to_string(img)
#     return text

def parse_chat_bubbles_from_text(raw_text: str) -> List[Dict]:
    """
    Very simple chat-bubble parser for demo: splits by newline and attributes
    sender heuristically. Real parsing should detect sender / timestamp / emoji.
    """
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    out = []
    for i, line in enumerate(lines):
        # naive heuristic: if line contains ':' treat left of ':' as sender
        if ':' in line:
            sender, msg = line.split(':', 1)
            out.append({"sender": sender.strip(), "timestamp": None, "message": msg.strip()})
        else:
            out.append({"sender": f"msg_{i}", "timestamp": None, "message": line})
    return out
