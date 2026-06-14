import sys
from pathlib import Path

PROHIBITED_TERMS = [
    "ensure",
    "establish",
    "engage",
    "align",
    "comprehensive",
    "essential",
    "crucial",
    "modern",
    "unlock",
    "elevate",
    "game-changer",
    "in today's digital landscape",
    "it is important to note",
    "when it comes to",
]

def scan(path: str) -> int:
    file_path = Path(path)

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        return 1

    text = file_path.read_text(encoding="utf-8")
    lowered = text.lower()

    failed = False

    if "—" in text:
        print("FAIL: Em dash found.")
        failed = True

    for term in PROHIBITED_TERMS:
        if term in lowered:
            print(f"FAIL: Prohibited term found: {term}")
            failed = True

    if not text.strip().startswith("# "):
        print("FAIL: Article does not start with an H1.")
        failed = True

    if failed:
        return 1

    print("PASS: QA scan passed.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python qa_scan.py <article.md>")
        sys.exit(1)

    sys.exit(scan(sys.argv[1]))
