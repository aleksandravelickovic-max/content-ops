# Spec: Client Annotation System for Content Navigator

## Problem

Clients review content in the Content Navigator but have no way to leave feedback directly on the documents. Currently feedback comes through email, calls, or screenshots — disconnected from the actual content. We need inline, location-specific commenting so clients can point at exactly what they want changed and say what they want.

## Design Constraints

- **No backend.** The navigator is a self-contained HTML file opened from disk or shared as a static file. No server, no database.
- **Persistence via repo.** Comments must round-trip through the git repo as JSON files so we have version history and can process them programmatically.
- **Works offline.** Clients may open the HTML file locally. Comments are captured in-browser and exported.
- **Minimal friction.** Click a spot, type a comment, done. No login, no account creation.

## Architecture

### Data Flow

```
Client opens navigator.html
  → reads content + any existing annotations (injected at build time)
  → client clicks on content to place annotation pin
  → types comment in popover
  → annotations accumulate in browser memory (localStorage backup)
  → client clicks "Export Feedback" → downloads annotations.json
  → team commits annotations.json to repo
  → next build injects those annotations back into navigator.html
```

### Storage Format

Each annotation file lives at:
```
clients/{client}/feedback/{document-key}.annotations.json
```

Where `{document-key}` is the content store key with slashes replaced by double-dashes (e.g., `campaigns--01-product-collection-pages--drafts--01-zellige.md`).

A single consolidated file per client also exists for import/export convenience:
```
clients/{client}/feedback/all-annotations.json
```

### Annotation Schema

```json
{
  "version": 1,
  "client": "zia-tile",
  "exportedAt": "2026-05-12T14:30:00Z",
  "exportedBy": "Client Name",
  "annotations": [
    {
      "id": "ann_a1b2c3d4",
      "documentKey": "clients/zia-tile/campaigns/01-product-collection-pages/drafts/01-zellige.md",
      "createdAt": "2026-05-12T14:22:00Z",
      "author": "Sarah (Zia Tile)",
      "status": "open",
      "anchor": {
        "type": "text-position",
        "selector": {
          "exact": "handcrafted by Moroccan artisans",
          "prefix": "Each zellige tile is ",
          "suffix": " using techniques passed",
          "startOffset": 1847,
          "endOffset": 1879
        },
        "heading": "## What Makes Zellige Unique",
        "paragraphIndex": 2
      },
      "comment": "We actually source from both Moroccan and Tunisian artisans now. Can we update this?",
      "resolution": null
    }
  ]
}
```

### Anchor Strategy

Anchoring annotations to rendered content is the hardest part. We use a layered approach so annotations survive minor edits:

1. **Text selector (primary).** Store the exact highlighted text plus ~30 chars of prefix/suffix context. This is the W3C Web Annotation `TextQuoteSelector` pattern — resilient to content shifting around the target.

2. **Heading context (secondary).** Store the nearest preceding heading (`## What Makes Zellige Unique`). If the exact text match fails (content was edited), we can still locate the annotation under the right heading and show it as "unanchored" with the original quoted text.

3. **Character offsets (tertiary).** Store start/end offsets from the document beginning. Least reliable after edits, but useful for sorting and as a last-resort anchor.

4. **Paragraph index (fallback).** Zero-indexed paragraph number under the nearest heading. Survives text edits within the paragraph.

**Resolution priority:** exact text match → prefix/suffix fuzzy match → heading + paragraph index → show as detached comment at document level.

## UI Components

### 1. Annotation Mode Toggle

A button in the preview pane header, next to the close button:

```
[💬 Annotate]  [×]
```

- Off by default. Clicking activates annotation mode.
- When active, the button turns blue and the cursor changes to crosshair over the preview body.
- A subtle banner appears: "Click or highlight text to add a comment"

### 2. Placing an Annotation

**Text highlight flow (primary):**
1. Client highlights a word, phrase, or sentence in the rendered preview.
2. On `mouseup` with a non-empty selection, a small floating toolbar appears near the selection: `[Add Comment]`
3. Clicking opens the comment popover anchored to the selection.

**Click-to-pin flow (secondary):**
1. Client clicks a specific location without selecting text.
2. We find the nearest text node and anchor to the surrounding sentence.
3. Comment popover opens.

### 3. Comment Popover

Minimal popover pinned to the annotation location:

```
┌─────────────────────────────────┐
│ Your Name                       │
│ ┌─────────────────────────────┐ │
│ │ Type your comment...        │ │
│ │                             │ │
│ └─────────────────────────────┘ │
│              [Cancel] [Save]    │
└─────────────────────────────────┘
```

- **Name field**: Pre-filled from localStorage after first entry. No auth required.
- **Comment field**: Multiline textarea, 200-char soft limit with counter.
- On save: annotation gets an ID, timestamp, stored in memory, pin appears in the gutter.

### 4. Annotation Pins (Gutter Markers)

Each saved annotation shows as a numbered pin in a left gutter (12px wide) inside the preview pane:

```
  ① | Each zellige tile is handcrafted by Moroccan artisans using
    | techniques passed down through generations...
```

- Pin color: orange (open), green (resolved), gray (detached/unanchored).
- Clicking a pin opens a read-only view of the comment with a "Reply" option.
- Hover shows a tooltip preview of the comment text.

### 5. Annotation Sidebar (Summary View)

A collapsible panel at the bottom or side of the preview pane listing all annotations for the current document:

```
┌─ Annotations (3 open, 1 resolved) ───────────────┐
│                                                    │
│  ① Sarah — "We source from both Moroccan and..."  │
│     § What Makes Zellige Unique · 2 hours ago      │
│     Status: Open                                   │
│                                                    │
│  ② Sarah — "Price should be $12/sf not $14"        │
│     § Pricing · 1 hour ago                         │
│     Status: Open                                   │
│                                                    │
│  ③ Sarah — "Love this section, keep as-is"         │
│     § Installation Guide · 30 min ago              │
│     Status: Resolved ✓                             │
│                                                    │
└────────────────────────────────────────────────────┘
```

Clicking an annotation in the sidebar scrolls the preview to that location and highlights it.

### 6. Export / Import

**Export button** in the header (visible when annotations exist):
```
[📥 Export Feedback (5)]
```

- Downloads `{client}-feedback-{date}.json` containing all annotations across all documents reviewed in this session.
- Also saves to localStorage as backup.

**Import at build time:**
- `build-content-navigator.py` scans `clients/{client}/feedback/*.annotations.json`
- Injects a `ANNOTATIONS` JavaScript object alongside `REGISTRIES` and `CONTENT`
- Existing annotations render as pins on document open

**Status sync:**
- Team members can update annotation status (`open` → `resolved` → `closed`) by editing the JSON and rebuilding.
- Resolved annotations appear in green and can be filtered out.

### 7. Aggregate Feedback Dashboard

A new top-level tab in the navigator: **"Feedback"**

Shows:
- Total open annotations across all clients/documents
- Grouped by document, sorted by most recent
- Filter by status (open/resolved/all)
- Filter by author
- One-click navigation to the annotation in context

## Build Script Changes

### New function: `load_annotations()`

```python
def load_annotations(client_name, client_path):
    """Load all annotation files for a client."""
    feedback_dir = client_path / "feedback"
    if not feedback_dir.exists():
        return {}
    
    annotations_by_doc = {}
    for f in feedback_dir.glob("*.annotations.json"):
        data = json.loads(f.read_text())
        for ann in data.get("annotations", []):
            doc_key = ann["documentKey"]
            if doc_key not in annotations_by_doc:
                annotations_by_doc[doc_key] = []
            annotations_by_doc[doc_key].append(ann)
    
    return annotations_by_doc
```

### Injection into HTML

Add a third data constant alongside `REGISTRIES` and `CONTENT`:

```javascript
const ANNOTATIONS = {annotations_json};
```

## Annotation Lifecycle

```
1. Client places annotation          → status: "open"
2. Client exports feedback JSON      → file saved locally
3. Team commits JSON to repo         → persisted in git
4. Team reviews, makes content edits → content updated
5. Team sets status to "resolved"    → annotation turns green
6. Next build includes resolution    → client sees it's handled
7. After confirmation, set "closed"  → filtered from default view
```

## Edge Cases

| Scenario | Behavior |
|---|---|
| Content edited after annotation placed | Text selector tries fuzzy match; falls back to heading+paragraph; worst case shows as detached comment at doc level |
| Same text appears multiple times | Use prefix/suffix context to disambiguate; if still ambiguous, use character offset |
| Annotation on HTML file (raw preview) | Anchor to line number instead of text selector (HTML shown as `<pre>` block) |
| Browser localStorage full | Warn user, suggest exporting, continue without backup |
| Multiple clients reviewing same doc | Author field distinguishes; no conflict since annotations are additive |
| Very long comment | Soft limit at 200 chars with counter; hard limit at 1000 chars |
| Annotation on truncated content | Pin shows at truncation boundary with note that the anchored text is in the full document |

## Implementation Phases

### Phase 1: Core Annotation (MVP)
- Annotation mode toggle in preview header
- Text highlight → comment popover flow
- In-memory storage + localStorage backup
- Gutter pins with tooltip preview
- Export button → downloads JSON
- Estimated complexity: ~400 lines of JS + ~80 lines of CSS added to the HTML template

### Phase 2: Build Integration
- `load_annotations()` in build script
- Inject `ANNOTATIONS` constant
- Render pre-existing annotations on document open
- Re-anchor logic (text match → fuzzy → heading fallback)
- Status display (open/resolved/closed)

### Phase 3: Feedback Dashboard
- Top-level "Feedback" tab in navigator
- Cross-document annotation summary
- Filters by status, author, document
- Click-to-navigate from dashboard to annotation in context

### Phase 4: Polish
- Reply threads (team responds to client annotation inline)
- Keyboard shortcuts (N = next annotation, P = previous)
- Print/PDF export of annotations report
- Annotation diff view (show what changed between the annotated version and current)

## What This Does NOT Include

- **Real-time collaboration.** No WebSocket/server. Annotations sync through git commits and rebuilds.
- **Authentication.** Name field is honor-system. This is for trusted client review, not public commenting.
- **Rich text comments.** Plain text only. Keeps the JSON clean and the UI simple.
- **Image/screenshot annotations.** Text content only. Screenshots go through existing channels.

## File Changes Required

| File | Change |
|---|---|
| `scripts/build-content-navigator.py` | Add `load_annotations()`, inject `ANNOTATIONS` constant, create `feedback/` dirs |
| `reports/content-navigator.html` (template) | Add annotation mode UI, gutter pins, comment popover, export button, annotation JS (~500 lines) |
| `clients/{client}/feedback/` | New directory, created by build script or first export |
| `.gitignore` | Ensure `feedback/` directories are NOT ignored (they should be committed) |
