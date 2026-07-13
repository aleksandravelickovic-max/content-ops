import re
import sys
import unicodedata

def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or "untitled-article"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python article_slug.py <topic>")
        sys.exit(1)

    print(slugify(" ".join(sys.argv[1:])))
