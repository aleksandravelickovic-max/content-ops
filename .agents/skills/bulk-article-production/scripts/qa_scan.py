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

    lines = text.splitlines()
    has_h1 = any(line.startswith("# ") for line in lines[:30])
    if not has_h1:
        print("FAIL: No H1 found in the first 30 lines.")
        failed = True

    has_faq = any(
        line.lower().startswith("## faq") or line.lower().startswith("## frequently asked")
        for line in lines
    )
    if not has_faq:
        print("FAIL: No FAQ section found (required H2: '## FAQ' or '## Frequently asked questions').")
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
