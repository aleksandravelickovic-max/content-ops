# The Nash Casino Client Intelligence

This folder is the writer-facing source of truth for client context.

## Files

- `STYLE-GUIDE.md` — copy of the canonical client style system.
- `offerings.md` — extracted products, services, goods, treatments, collections, or solution areas.
- `offerings.json` — machine-readable version of the offerings index.
- `source-files.md` — local source material available in this repo.

## Source of truth

The canonical style system still lives at:

```text
clients/the-nash-casino/STYLE-SYSTEM.md
```

Run this to refresh this folder:

```bash
python3 scripts/build-client-context-dashboard.py
python3 scripts/organize-client-folders.py
```
