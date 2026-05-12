# Spec: Text-Anchored Annotations for Content Review Portal

## Problem

Clients review content via the portal's share-link system but can only leave general comments — they can't point at a specific sentence and say "change this." Feedback arrives disconnected from the text it refers to, requiring manual back-and-forth to clarify.

## Solution

Extend the existing comment system with text anchoring. Clients highlight text in the rendered content, and their comment is pinned to that exact location. Existing comments with anchors render as inline highlights in the content.

## Architecture

All annotation functionality lives in the existing portal app (`portal/`). No separate server, no new database — just new columns on the existing `comments` table and client-side JS for text selection and highlighting.

### What Changed

| File | Change |
|---|---|
| `portal/app/models.py` | Added 6 anchor columns to `Comment` model |
| `portal/app/routes/api.py` | `CommentCreate` schema accepts anchor fields |
| `portal/app/routes/review.py` | Serializes comments as JSON for client-side highlighting |
| `portal/app/templates/review/content.html` | Annotation toggle, selection quote UI, CSS/JS includes |
| `portal/app/static/annotation.css` | Styles for highlights, selection tooltip, annotation mode |
| `portal/app/static/annotation.js` | Text selection, anchor extraction, re-anchoring, inline highlights |

### Database Changes

Six nullable columns added to `comments`:

```
anchor_prefix           TEXT    ~40 chars before the selected text
anchor_suffix           TEXT    ~40 chars after the selected text
anchor_start_offset     INT     character offset from document start
anchor_end_offset       INT     character offset end
anchor_heading          TEXT    nearest preceding heading text
anchor_paragraph_index  INT     paragraph index under that heading
```

The existing `highlight_text` column stores the selected text itself. These anchor fields provide the surrounding context needed to re-locate the annotation after content edits.

### Anchor Strategy (W3C TextQuoteSelector)

1. **Exact match** — find `highlight_text` in the rendered content
2. **Prefix/suffix disambiguation** — if multiple matches, use surrounding context to pick the right one
3. **Heading + paragraph fallback** — if text was edited, locate the general area

### User Flow

```
Client opens review link → /review/{token}/{content_path}
  → page loads with comments in sidebar + highlights on content
  → client clicks "Annotate" button in header
  → banner: "Highlight text to pin your feedback"
  → client highlights a sentence → "Add Comment" tooltip appears
  → client clicks tooltip → selection quote appears in comment form
  → client types feedback and submits
  → page reloads → new comment has anchor data → highlight renders inline
```

### UI Components

**Annotation mode toggle** — button in review header, toggles crosshair cursor and text selection handling.

**Selection tooltip** — floating "Add Comment" button appears above highlighted text. Clicking it fills the comment form with the anchor data and shows the quoted text.

**Inline highlights** — comments with `highlight_text` render as yellow-highlighted spans with numbered badges. Clicking a highlight scrolls to its comment in the sidebar. Resolved comments show green.

**"Show in text" links** — comment cards in the sidebar get a link that scrolls to and flashes the corresponding highlight.

## Static Navigator

The standalone `reports/content-navigator.html` remains a read-only content browser. It does not include annotation functionality — that lives exclusively in the portal.
