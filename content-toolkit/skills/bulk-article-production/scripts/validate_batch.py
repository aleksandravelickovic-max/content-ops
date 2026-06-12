import csv
import sys
from pathlib import Path

REQUIRED_COLUMNS = [
    "topic",
    "primary_keyword",
    "search_intent",
    "audience",
    "product_angle",
    "word_count",
    "internal_links",
    "competitors",
    "notes",
]

def validate_csv(path: str) -> int:
    file_path = Path(path)

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        return 1

    with file_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []

        missing = [col for col in REQUIRED_COLUMNS if col not in columns]

        if missing:
            print("ERROR: Missing required columns:")
            for col in missing:
                print(f"- {col}")
            return 1

        rows = list(reader)

    if not rows:
        print("ERROR: Batch file has no topic rows.")
        return 1

    failed = False

    for index, row in enumerate(rows, start=2):
        for col in REQUIRED_COLUMNS:
            if not str(row.get(col, "")).strip():
                print(f"ERROR: Row {index} has empty required field: {col}")
                failed = True

    if failed:
        return 1

    print(f"OK: {len(rows)} topic rows validated.")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_batch.py <batch.csv>")
        sys.exit(1)

    sys.exit(validate_csv(sys.argv[1]))
