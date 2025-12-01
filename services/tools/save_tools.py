# tools/save_tools.py
import json
from pathlib import Path
from typing import Any, Dict

OUTDIR = Path("sample_outputs")
OUTDIR.mkdir(parents=True, exist_ok=True)

def save_json(obj: Dict[str, Any], filename: str) -> str:
    path = OUTDIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return str(path)

# Optional small pdf export (uses reportlab). For demo it's simple text PDF.
def save_pdf_simple(text: str, filename: str) -> str:
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except Exception:
        # reportlab not installed — fallback to saving .txt
        path = OUTDIR / filename.replace(".pdf", ".txt")
        path.write_text(text, encoding="utf-8")
        return str(path)
    path = OUTDIR / filename
    c = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    # naive line wrapping
    y = height - 40
    for line in text.splitlines():
        if y < 60:
            c.showPage()
            y = height - 40
        c.drawString(40, y, line)
        y -= 14
    c.save()
    return str(path)
