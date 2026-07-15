#!/usr/bin/env python3
"""
Build a multi-page LinkGraph client context dashboard.

This creates one writer-facing HTML page per client, plus an index page:

    reports/client-context-dashboard/index.html
    reports/client-context-dashboard/{client}.html
    reports/client-context-dashboard/data.json

Each client page combines:
- the client's STYLE-SYSTEM.md
- offerings/products/services extracted from style-system and raw markdown
- website sitemap/page intelligence
- source files available in the repo
"""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = ROOT / "clients"
OUT_DIR = ROOT / "reports" / "client-context-dashboard"
DATA_PATH = OUT_DIR / "data.json"
EXCLUDED_CLIENT_SLUGS = {"searchatlas"}

MAX_SOURCE_CHARS = 24_000
MAX_OFFERINGS = 80
MAX_EVIDENCE = 6

SERVICE_TAXONOMY_PATHS = (
    ("raw", "knowledge", "service-taxonomy.md"),
    ("raw", "knowledge", "services.md"),
    ("raw", "knowledge", "offerings.md"),
)

OFFERING_HEADINGS = re.compile(
    r"(?i)(products?|services?|solutions?|offerings?|treatments?|procedures?|"
    r"tours?|charters?|storage types?|locations?|materials?|collections?|"
    r"product categories|service categories)"
)

NON_OFFERING_HEADINGS = re.compile(
    r"(?i)(page structure|product pages?|landing pages?|notable product specs?|"
    r"technical specification|seo standards?|meta titles?|meta descriptions?|"
    r"terminology|avoid|voice|tone|accuracy|checklist|specificity rules?|"
    r"(?:standard )?tour inclusions|tour route|sea caves|snorkel locations|"
    r"wildlife commonly seen|service / program pages?|program and service pages?|"
    r"solution / feature pages?|service category pages?|service details)"
)

CLIENT_SECTION_HEADINGS = re.compile(
    r"(?i)(brand|audience|voice|tone|terminology|avoid|accuracy|technical|"
    r"products?|services?|solutions?|offerings?|treatments?|locations?|seo|"
    r"page structure|compliance|proof|claims|style)"
)

STOPWORDS = {
    "about", "after", "again", "also", "and", "are", "available", "because",
    "before", "being", "best", "blog", "business", "can", "client", "company",
    "content", "does", "each", "for", "from", "guide", "have", "help", "home", "into",
    "learn", "more", "near", "needs", "new", "our", "page", "people", "read",
    "service", "services", "site", "solution", "solutions", "that", "the",
    "their", "them", "this", "through", "use", "using", "what", "when", "where",
    "with", "your",
}

SEMANTIC_STOPWORDS = STOPWORDS | {
    "all", "any", "below", "click", "core", "could", "example", "examples",
    "format", "here", "included", "includes", "including", "latest", "must",
    "not", "one", "only", "other", "per", "posts", "question", "required", "rule", "rules",
    "referenced", "section", "sections", "submit", "tbd", "these", "those", "throughout", "video",
    "videos", "warranty", "will", "within", "without", "youtube", "year",
    "years",
}


@dataclass
class SourceDoc:
    path: str
    title: str
    text: str


@dataclass
class ClientContext:
    slug: str
    display_name: str
    path: Path
    style_system_text: str
    style_sections: list[dict[str, str]] = field(default_factory=list)
    source_docs: list[SourceDoc] = field(default_factory=list)
    offerings: list[dict[str, Any]] = field(default_factory=list)
    website_intelligence: dict[str, Any] = field(default_factory=dict)
    quick_facts: list[str] = field(default_factory=list)
    voice_rules: list[str] = field(default_factory=list)
    avoid_rules: list[str] = field(default_factory=list)
    terminology: list[str] = field(default_factory=list)
    semantic_topics: list[str] = field(default_factory=list)


def esc(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def slug_to_name(slug: str) -> str:
    return slug.replace("/", " / ").replace("-", " ").title()


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def strip_md(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"[*_>#]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip(" -|\t")


def discover_clients() -> list[ClientContext]:
    clients = []
    for style_path in sorted(CLIENTS_DIR.rglob("STYLE-SYSTEM.md")):
        slug = style_path.parent.relative_to(CLIENTS_DIR).as_posix()
        if slug in EXCLUDED_CLIENT_SLUGS:
            continue
        style_text = style_path.read_text(encoding="utf-8", errors="replace")
        display_name = extract_display_name(style_text, slug)
        client = ClientContext(
            slug=slug,
            display_name=display_name,
            path=style_path.parent,
            style_system_text=style_text,
        )
        client.style_sections = extract_sections(style_text)
        client.source_docs = load_source_docs(client)
        client.website_intelligence = load_json(client.path / "raw" / "research" / "website-intelligence.json")
        client.offerings = extract_offerings(client)
        client.quick_facts = extract_quick_facts(client)
        client.voice_rules = extract_voice_rules(client)
        client.avoid_rules = extract_avoid_rules(client)
        client.terminology = extract_terminology(client)
        client.semantic_topics = extract_semantic_topics(client)
        clients.append(client)
    return sorted(clients, key=lambda c: c.display_name.lower())


def extract_display_name(style_text: str, slug: str) -> str:
    first = next((line.strip("# ").strip() for line in style_text.splitlines() if line.startswith("# ")), "")
    if first:
        return first.replace("Style System", "").replace("—", "").strip() or slug_to_name(slug)
    return slug_to_name(slug)


def extract_sections(markdown: str) -> list[dict[str, str]]:
    sections = []
    current_title = "Overview"
    current_lines: list[str] = []
    for line in markdown.splitlines():
        match = re.match(r"^(#{1,3})\s+(.+)$", line)
        if match:
            if current_lines:
                sections.append({"title": current_title, "text": "\n".join(current_lines).strip()})
            current_title = strip_md(match.group(2))
            current_lines = []
        else:
            current_lines.append(line)
    if current_lines:
        sections.append({"title": current_title, "text": "\n".join(current_lines).strip()})
    return sections


def load_source_docs(client: ClientContext) -> list[SourceDoc]:
    docs = []
    for path in sorted(client.path.rglob("*.md")):
        if ".beads" in path.parts:
            continue
        if path.name == "website-intelligence.md":
            continue
        rel = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        title = first_title(text) or path.stem.replace("-", " ").title()
        docs.append(SourceDoc(rel, title, text[:MAX_SOURCE_CHARS]))
    return docs


def first_title(text: str) -> str:
    for line in text.splitlines()[:30]:
        if line.startswith("# "):
            return strip_md(line[2:])
        if line.lower().startswith("title:"):
            return strip_md(line.split(":", 1)[1])
    return ""


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def extract_offerings(client: ClientContext) -> list[dict[str, Any]]:
    candidates: dict[str, dict[str, Any]] = {}
    add_offerings_from_markdown(candidates, client.style_system_text, "STYLE-SYSTEM.md")
    add_offerings_from_service_taxonomy_docs(candidates, client)
    add_offerings_from_product_docs(candidates, client)
    add_offerings_from_website(candidates, client.website_intelligence)
    for item in candidates.values():
        if not item["description"]:
            item["description"] = fallback_description(client.display_name, item["name"], item.get("sections", []))
        item["description"] = normalize_description(item["description"], item["name"])
    ranked = sorted(candidates.values(), key=lambda item: (-item["score"], item["name"].lower()))
    return ranked[:MAX_OFFERINGS]


def add_offerings_from_markdown(candidates: dict[str, dict[str, Any]], markdown: str, source: str) -> None:
    sections = extract_sections(markdown)
    for section in sections:
        title = section["title"]
        text = section["text"]
        section_is_relevant = OFFERING_HEADINGS.search(title) is not None
        if NON_OFFERING_HEADINGS.search(title):
            continue
        if "reserved" in title.lower():
            continue
        if "reserved" in text.lower() and len(strip_md(text)) < 260:
            continue
        section_offering = offering_name_from_section_title(title)
        if not section_offering and re.match(r"^\d+\.\d+\s+", title) and re.search(r"\*\*(Core value|Key capabilities|Key services):\*\*", text):
            section_offering = re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", strip_md(title)).strip()
        if section_offering:
            section_is_relevant = True
        lines = [line.rstrip() for line in text.splitlines()]
        if not section_is_relevant:
            continue
        if section_offering:
            add_candidate(candidates, section_offering, first_body_paragraph(text), source, title, 4)
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            item = parse_table_row(stripped) or parse_bullet(stripped)
            if not item and section_is_relevant and not section_offering:
                if stripped.startswith("|"):
                    continue
                item = parse_short_sentence(stripped)
            if not item:
                continue
            name, description = item
            if not valid_offering_name(name):
                continue
            add_candidate(candidates, name, description, source, title, 3 if section_is_relevant else 1)


def offering_name_from_section_title(title: str) -> str:
    name = re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", strip_md(title)).strip()
    lowered = name.lower()
    generic = {
        "products", "product", "services", "service", "solutions", "offerings",
        "product categories", "service categories", "key product categories",
        "product / collection reference", "service reference", "storage types",
        "products & solutions", "product collections", "product knowledge",
    }
    if lowered in generic:
        return ""
    if any(phrase in lowered for phrase in [
        "reference", "knowledge", "reserved", "section ", " elements",
        "standard", "standards", "spec", "specs", "specification",
        "page standard", "product page",
    ]):
        return ""
    if any(word in lowered for word in ["service", "services", "solution", "solutions", "product", "products"]):
        return name
    return ""


def parse_table_row(line: str) -> tuple[str, str] | None:
    if not (line.startswith("|") and line.endswith("|")):
        return None
    cells = [strip_md(cell) for cell in line.strip("|").split("|")]
    cells = [cell for cell in cells if cell and not set(cell) <= {"-", ":"}]
    if len(cells) < 2:
        return None
    if cells[0].lower() in {"term", "avoid", "attribute", "goal", "page", "url", "category", "material", "service"}:
        return None
    return cells[0][:90], " | ".join(cells[1:])[:260]


def parse_bullet(line: str) -> tuple[str, str] | None:
    if not re.match(r"^[-*]\s+", line):
        return None
    text = strip_md(re.sub(r"^[-*]\s+", "", line))
    if len(text) < 4:
        return None
    parts = re.split(r"\s+[—-]\s+|:\s+", text, maxsplit=1)
    if len(parts) == 2:
        return parts[0][:90], parts[1][:260]
    if len(text.split()) <= 9:
        return text[:90], ""
    return None


def parse_short_sentence(line: str) -> tuple[str, str] | None:
    text = strip_md(line)
    if len(text) < 5 or len(text) > 180:
        return None
    if text.endswith(":"):
        return None
    if re.match(r"^H[1-6]\b", text, flags=re.I):
        return None
    if re.match(r"^(Meta title|Meta description|CTA|FAQ)\b", text, flags=re.I):
        return None
    if re.match(r"^\d+\.", text):
        text = re.sub(r"^\d+\.\s*", "", text)
    if len(text.split()) <= 12:
        return text[:90], ""
    return None


def valid_offering_name(name: str) -> bool:
    lowered = name.lower().strip()
    if len(lowered) < 3 or len(lowered) > 90:
        return False
    if lowered.startswith("[ ]"):
        return False
    bad = {
        "avoid", "use instead", "reason", "notes", "writing rule", "core focus",
        "primary keyword", "headings", "headings:", "meta", "type", "url",
        "results", "what to expect", "about the author", "latest blog posts about this product",
        "latest youtube videos about this product", "click here to submit a new question",
        "term", "use", "examples", "details", "category", "service", "collection",
        "material", "component", "content", "feature", "features", "frequency bands",
        "firmware requirement", "explain the mechanism", "purpose", "elements",
        "secondary", "tertiary",
        "cta", "phone", "contact link",
    }
    if lowered in bad:
        return False
    if lowered.startswith(("http://", "https://")):
        return False
    if lowered.startswith(("what ", "when ", "why ", "how ", "where ", "which ")):
        return False
    if lowered.startswith(("primary keyword", "secondary:", "tertiary:", "purpose:", "elements:")):
        return False
    if re.match(r"^h[1-6]\b", lowered):
        return False
    if lowered.startswith(("generated:", "sources:", "base rules:", "csm:", "cta ")):
        return False
    if any(char in name for char in ['{', '}', '"']):
        return False
    if re.match(r"^[a-z_ -]+:$", lowered):
        return False
    if re.match(r"^\d{3,}\b", lowered):
        return False
    if lowered.endswith((".html", ".htm")):
        return False
    if lowered in {"capacity", "category", "bestfor", "build", "battery", "brand voice phrases"}:
        return False
    if any(phrase in lowered for phrase in [
        "when writing", "when contrasting", "attribute outcomes", "frame confidence",
        "must be", "do not", "should be", "title format", "multiple locations span",
        "band compatibility", "about the author", "site copy", "target urls",
        "tone is", "no comparative", "no exaggerated", "no guaranteed",
        "location-specific content", "a clinic", "a practice", "a provider",
        "gbps", "ethernet port", "router throughput", "mini-sim", "mah",
        "li-ion", "quick charge", "dc output", "built-in 5g modem",
        "sub-6", "c-band", "cat 20", "does not stack", "component ",
        "technical specification", "core narrative", "scannable features",
        "product header", "cart module", "best seo tool", "best-in-class",
        "standalone", "domain authority", "google my business", "gmb /",
        "all-in-one", "without specifics", "primary keyword", "secondary:",
        "tertiary:", "purpose:", "elements:", "reserved",
        "meta description", "meta title", "faq", "minimum questions",
        "phone contact link", "what we build", "why a plus",
        "how to book", "pricing and booking", "what's customizable",
        "bullet list", "program and service pages", "service category pages",
        "unit sizes", "reserve-focused", "service details",
        "standard tour inclusions", "snorkel gear", "soft drinks",
        "freshwater showers", "onboard restroom", "deli-style lunch",
        "cultural narration", "lead with the personalization angle",
        "service / program pages", "solution / feature pages",
    ]):
        return False
    if re.search(r"\b20[0-9]{2}\b", lowered) and any(word in lowered for word in ["best", "tips", "wins", "tested", "approved"]):
        return False
    if any(word in lowered for word in ["do not", "never", "avoid", "wrong", "banned"]):
        return False
    return True


def candidate_key(name: str) -> str:
    lowered = name.lower()
    lowered = re.sub(r"\([^)]*\)", " ", lowered)
    lowered = re.sub(r"\b(treatments?|services?|solutions?|procedures?|products?|goods?|page|pages)\b", " ", lowered)
    lowered = re.sub(r"\b(for|near|in|at|by|with|and|the|a|an)\b", " ", lowered)
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return lowered


def preferred_name(current: str, candidate: str) -> str:
    current_words = current.split()
    candidate_words = candidate.split()
    if not current:
        return candidate
    if len(candidate_words) < len(current_words) and len(candidate) >= 4:
        return candidate
    if any(word in current.lower() for word in ["treatment", "service", "page"]) and not any(
        word in candidate.lower() for word in ["treatment", "service", "page"]
    ):
        return candidate
    return current


def normalize_description(description: str, name: str) -> str:
    description = clean_text(description)
    description = re.sub(r"\s*\|\s*", "; ", description)
    description = re.sub(r"(?i)\b(learn more|shop now|book now|contact us|get started)\b\.?", "", description)
    description = clean_text(description)
    if len(description) > 320:
        description = description[:317].rstrip(" ,.;") + "..."
    return description


def fallback_description(display_name: str, name: str, sections: list[str]) -> str:
    section_hint = next((section for section in sections if section and section.lower() != name.lower()), "")
    if section_hint:
        return f"{name} is listed under {section_hint} in the {display_name} client context. Check the source links before adding specific claims."
    return f"{name} is listed as an offering for {display_name}. Check the source links before adding specific claims."


def add_offerings_from_product_docs(candidates: dict[str, dict[str, Any]], client: ClientContext) -> None:
    products_dir = client.path / "raw" / "knowledge" / "products"
    if not products_dir.exists():
        return
    for path in sorted(products_dir.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        name = frontmatter_value(text, "name") or first_title(text) or path.stem.replace("-", " ").title()
        if not valid_offering_name(name):
            continue
        description = first_section_paragraph(text, "Definition") or first_body_paragraph(text)
        source = path.relative_to(ROOT).as_posix()
        add_candidate(candidates, name, description, source, "raw product knowledge", 5)


def add_offerings_from_service_taxonomy_docs(candidates: dict[str, dict[str, Any]], client: ClientContext) -> None:
    for parts in SERVICE_TAXONOMY_PATHS:
        path = client.path.joinpath(*parts)
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        source = path.relative_to(ROOT).as_posix()
        current_section = "service taxonomy"
        for raw_line in text.splitlines():
            stripped = raw_line.strip()
            if not stripped:
                continue
            heading = re.match(r"^#{2,4}\s+(.+)$", stripped)
            if heading:
                current_section = strip_md(heading.group(1))
                continue
            item = parse_table_row(stripped) or parse_bullet(stripped)
            if not item:
                continue
            name, description = item
            if not valid_offering_name(name):
                continue
            add_candidate(candidates, name, description, source, current_section, 6)


def frontmatter_value(text: str, key: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for line in lines[1:40]:
        if line.strip() == "---":
            break
        if line.lower().startswith(f"{key.lower()}:"):
            return strip_md(line.split(":", 1)[1])
    return ""


def first_section_paragraph(text: str, title: str) -> str:
    pattern = re.compile(rf"^#+\s+{re.escape(title)}\s*$", flags=re.I | re.M)
    match = pattern.search(text)
    if not match:
        return ""
    tail = text[match.end():]
    return first_body_paragraph(tail)


def first_body_paragraph(text: str) -> str:
    lines: list[str] = []
    in_frontmatter = False
    for raw in text.splitlines():
        line = raw.strip()
        if line == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter or not line:
            if lines:
                break
            continue
        if line.startswith("#"):
            if lines:
                break
            continue
        if line.startswith(("-", "*", "|")):
            if lines:
                break
            continue
        lines.append(strip_md(line))
    return clean_text(" ".join(lines))[:320]


def add_candidate(
    candidates: dict[str, dict[str, Any]],
    name: str,
    description: str,
    source: str,
    section: str,
    score: int,
) -> None:
    name = clean_text(name)
    description = normalize_description(description, name)
    key = candidate_key(name)
    if not key:
        return
    existing = candidates.setdefault(
        key,
        {"name": name, "description": "", "sources": [], "sections": [], "score": 0},
    )
    existing["name"] = preferred_name(existing["name"], name)
    if description and len(description) > len(existing["description"]):
        existing["description"] = description
    if source not in existing["sources"]:
        existing["sources"].append(source)
    if section not in existing["sections"]:
        existing["sections"].append(section)
    existing["score"] += score


def add_offerings_from_website(candidates: dict[str, dict[str, Any]], intel: dict[str, Any]) -> None:
    for page in intel.get("sample_pages", []) + intel.get("offering_pages", []):
        if page.get("page_type") not in {"product", "service"}:
            continue
        if not useful_website_offering_page(page):
            continue
        title = strip_site_suffix(page.get("title", ""))
        if title and valid_offering_name(title):
            if candidate_key(title) not in candidates:
                continue
            description = page.get("meta_description", "")
            source = "website offering page" if page in intel.get("offering_pages", []) else "website sitemap sample"
            add_candidate(candidates, title, description, source, page.get("url") or page.get("page_type", "website"), 1)


def useful_website_offering_page(page: dict[str, Any]) -> bool:
    url = page.get("url", "")
    title = strip_site_suffix(page.get("title", ""))
    description = clean_text(page.get("meta_description", ""))
    if not url or re.search(r"/(?:blog|articles|resources|category|tag)/", url):
        return False
    if not title or not description or len(description) < 45:
        return False
    lowered_title = title.lower()
    lowered_description = description.lower()
    if lowered_title in {"home", "homepage"}:
        return False
    if any(phrase in lowered_title for phrase in ["homepage", "warranty & returns"]):
        return False
    if any(phrase in lowered_description for phrase in [
        "one-stop-shop", "wide range", "warranty on all", "if you have any problems",
        "ammunition license", "welcome to",
    ]):
        return False
    return True


def strip_site_suffix(title: str) -> str:
    title = clean_text(title)
    title = re.split(r"\s+[|]\s+|\s+[-]\s+", title)[0]
    return title[:90]


def url_to_name(url: str) -> str:
    path = re.sub(r"/+$", "", re.sub(r"[?#].*$", "", url))
    leaf = path.split("/")[-1]
    if not leaf:
        return ""
    leaf = re.sub(r"\.(html?|php|aspx?)$", "", leaf, flags=re.I)
    leaf = re.sub(r"^\d+[_-]+", "", leaf)
    return leaf.replace("-", " ").replace("_", " ").title()


def extract_quick_facts(client: ClientContext) -> list[str]:
    facts: list[str] = []
    for section in sections_matching(client, ["brand", "audience", "overview"]):
        for line in section["text"].splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            bold_label = re.match(r"^\*\*([^*]+):\*\*\s*(.+)$", stripped)
            if bold_label:
                facts.append(f"{strip_md(bold_label.group(1))}: {strip_md(bold_label.group(2))}")
                continue
            if stripped.startswith(("-", "*")):
                fact = strip_md(re.sub(r"^[-*]\s+", "", stripped))
                if fact:
                    facts.append(fact)
                continue
            text = strip_md(stripped)
            if text.endswith(":"):
                continue
            if 40 <= len(text) <= 240 and not stripped.startswith("|"):
                facts.append(text)
        if facts:
            break
    return unique_lines(facts, limit=10)


def extract_lines_by_keywords(text: str, keywords: list[str], limit: int) -> list[str]:
    out = []
    for line in text.splitlines():
        stripped = strip_md(line)
        if not stripped or len(stripped) < 8 or len(stripped) > 260:
            continue
        lowered = stripped.lower()
        if any(keyword in lowered for keyword in keywords):
            if stripped not in out:
                out.append(stripped)
        if len(out) >= limit:
            break
    return out


def sections_matching(client: ClientContext, keywords: list[str]) -> list[dict[str, str]]:
    matches = []
    for section in client.style_sections:
        title = section["title"].lower()
        if any(keyword in title for keyword in keywords):
            matches.append(section)
    return matches


def unique_lines(lines: list[str], limit: int) -> list[str]:
    out = []
    seen = set()
    for line in lines:
        cleaned = clean_context_line(line)
        if not cleaned:
            continue
        key = re.sub(r"[^a-z0-9]+", " ", cleaned.lower()).strip()
        if key in seen:
            continue
        seen.add(key)
        out.append(cleaned)
        if len(out) >= limit:
            break
    return out


def clean_context_line(line: str) -> str:
    line = strip_md(line)
    line = re.sub(r"\s*\|\s*", ": ", line)
    line = re.sub(r"\s+", " ", line)
    line = line.strip(" -|")
    line = line.strip("*_ ")
    if not line:
        return ""
    lowered = line.lower()
    if lowered in {"term: rule", "banned: reason", "attribute: writing rule", "segment: core need"}:
        return ""
    if set(line) <= {"-", ":"}:
        return ""
    if line.endswith(":"):
        return ""
    return line


def markdown_table_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [strip_md(cell) for cell in stripped.strip("|").split("|")]
        cells = [cell for cell in cells if cell]
        if not cells or all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        rows.append(cells)
    if rows and all(cell.lower() in {"term", "rule", "banned", "reason", "attribute", "writing rule", "segment", "core need"} for cell in rows[0]):
        rows = rows[1:]
    return rows


def bullet_lines_after_marker(text: str, marker: str) -> list[str]:
    lines = text.splitlines()
    collecting = False
    out = []
    for raw in lines:
        stripped = raw.strip()
        if marker.lower() in stripped.lower():
            collecting = True
            continue
        if collecting and stripped.startswith("##"):
            break
        if collecting and stripped and not stripped.startswith(("-", "*")) and not stripped.startswith("|"):
            if out:
                break
        if collecting and stripped.startswith(("-", "*")):
            out.append(strip_md(re.sub(r"^[-*]\s+", "", stripped)))
    return out


def extract_voice_rules(client: ClientContext) -> list[str]:
    rules: list[str] = []
    for section in sections_matching(client, ["voice", "tone"]):
        voice_text = re.split(r"(?im)^\s*\*\*?Avoid:?\*\*?\s*$", section["text"], maxsplit=1)[0]
        for cells in markdown_table_rows(voice_text):
            if len(cells) >= 2:
                rules.append(f"{cells[0]}: {cells[1]}")
        for line in voice_text.splitlines():
            stripped = line.strip()
            if stripped.startswith(("-", "*")) and "avoid" not in stripped.lower():
                rules.append(strip_md(re.sub(r"^[-*]\s+", "", stripped)))
    return unique_lines(rules, limit=8)


def extract_avoid_rules(client: ClientContext) -> list[str]:
    rules: list[str] = []
    for section in sections_matching(client, ["voice", "tone"]):
        rules.extend(bullet_lines_after_marker(section["text"], "Avoid"))
    for section in sections_matching(client, ["strict avoidance", "avoid"]):
        for cells in markdown_table_rows(section["text"]):
            if len(cells) >= 2:
                rules.append(f"{cells[0]}: {cells[1]}")
    for section in sections_matching(client, ["accuracy", "technical standards", "specificity rules"]):
        for line in section["text"].splitlines():
            stripped = line.strip()
            if stripped.startswith(("-", "*")):
                rules.append(strip_md(re.sub(r"^[-*]\s+", "", stripped)))
    return unique_lines(rules, limit=14)


def extract_terminology(client: ClientContext) -> list[str]:
    terms: list[str] = []
    for section in sections_matching(client, ["required terms", "terminology"]):
        if "avoid" in section["title"].lower():
            continue
        for cells in markdown_table_rows(section["text"]):
            if len(cells) >= 2:
                terms.append(f"{cells[0]}: {cells[1]}")
    return unique_lines(terms, limit=10)


def extract_semantic_topics(client: ClientContext) -> list[str]:
    topics: list[str] = []
    topics.extend(item.get("name", "") for item in client.offerings)
    topics.extend(term.split(":", 1)[0] for term in client.terminology)

    source_text = " ".join(
        [
            " ".join(client.quick_facts),
            " ".join(client.voice_rules),
            " ".join(client.terminology),
        ]
    )
    candidates: Counter[str] = Counter()
    for phrase in semantic_phrases(source_text):
        candidates[phrase] += 1
    topics.extend(phrase for phrase, count in candidates.most_common(40) if count >= 2)
    return unique_topic_lines(topics, limit=30)


def semantic_phrases(text: str) -> list[str]:
    cleaned = strip_md(text)
    cleaned = re.sub(r"https?://\S+", " ", cleaned)
    phrases: list[str] = []
    for segment in re.split(r"[\n.;:()\[\]|]+", cleaned):
        tokens = [
            token
            for token in re.findall(r"[A-Za-z][A-Za-z0-9+/-]*", segment)
            if token.lower().strip("-/") not in SEMANTIC_STOPWORDS and len(token) >= 3
        ]
        if len(tokens) < 2:
            continue
        for size in (3, 2):
            for index in range(0, len(tokens) - size + 1):
                phrase = " ".join(tokens[index:index + size])
                if useful_topic(phrase):
                    phrases.append(normalize_topic(phrase))
    return phrases


def normalize_topic(value: str) -> str:
    value = clean_text(value).strip(" -/|")
    replacements = {
        "Seo": "SEO",
        "Hrs": "HRS",
        "Hr": "HR",
        "Ukg": "UKG",
        "Gbp": "GBP",
        "Gsa": "GSA",
        "Bbb": "BBB",
        "Lte": "LTE",
        "Wifi": "WiFi",
        "Wi-fi": "Wi-Fi",
        "5g": "5G",
        "4g": "4G",
    }
    titled = value if any(char.isupper() for char in value[1:]) else value.title()
    for old, new in replacements.items():
        titled = re.sub(rf"\\b{old}\\b", new, titled)
    return titled


def useful_topic(value: str) -> bool:
    lowered = value.lower()
    if len(lowered) < 4 or len(lowered) > 70:
        return False
    if len(lowered.split()) == 1 and lowered not in {
        "5gstore", "peplink", "speedfusion", "firstnet", "ukg", "salesforce",
        "botox", "dysport", "kybella", "coolsculpting", "hydrafacial",
        "antennas", "facials", "zellige", "marble", "limestone", "terrazzo",
        "ceramics",
    }:
        return False
    if any(char.isdigit() for char in lowered) and not re.search(r"\\b[45]g\\b|\\blte\\b|\\bband\\b|\\bcat\\b", lowered):
        return False
    bad_fragments = {
        "latest", "warranty", "click", "submit", "question", "youtube", "videos",
        "posts", "landing pages", "all extended", "examples", "format", "length",
        "primary keyword", "secondary keyword", "tertiary", "usage", "rule",
        "product technical", "technical specify", "writing", "claims",
        "listed under", "check source", "source links", "adding specific",
        "tbd campaigns", "models tbd", "referenced cases",
    }
    return not any(fragment in lowered for fragment in bad_fragments)


def unique_topic_lines(lines: list[str], limit: int) -> list[str]:
    out: list[str] = []
    seen = set()
    for line in lines:
        cleaned = normalize_topic(clean_context_line(line))
        if not cleaned or not useful_topic(cleaned):
            continue
        key = re.sub(r"[^a-z0-9]+", " ", cleaned.lower()).strip()
        if key in seen:
            continue
        seen.add(key)
        out.append(cleaned)
        if len(out) >= limit:
            break
    return out


def render_markdown_excerpt(markdown: str) -> str:
    escaped = esc(markdown)
    escaped = re.sub(r"^### (.+)$", r"<h4>\1</h4>", escaped, flags=re.M)
    escaped = re.sub(r"^## (.+)$", r"<h3>\1</h3>", escaped, flags=re.M)
    escaped = re.sub(r"^# (.+)$", r"<h2>\1</h2>", escaped, flags=re.M)
    escaped = re.sub(r"^- (.+)$", r"<li>\1</li>", escaped, flags=re.M)
    escaped = escaped.replace("\n\n", "</p><p>")
    escaped = escaped.replace("\n", "<br>")
    escaped = escaped.replace("<p><li>", "<ul><li>").replace("</li></p>", "</li></ul>")
    return f"<p>{escaped}</p>"


def render_index(clients: list[ClientContext]) -> str:
    cards = "\n".join(render_index_card(client) for client in clients)
    generated = datetime.now(timezone.utc).isoformat()
    total_offerings = sum(len(client.offerings) for client in clients)
    ok_count = sum(1 for client in clients if client.website_intelligence.get("status") == "ok")
    return html_page(
        "LinkGraph Client Context Dashboard",
        f"""
        <nav class="topnav">
          <a class="brand" href="https://www.linkgraph.com/"><span>LG</span>LinkGraph</a>
          <div class="nav-meta">Client delivery intelligence</div>
        </nav>
        <section class="hero index-hero">
          <div class="hero-copy">
            <div class="kicker">LinkGraph Content Ops</div>
            <h1>Client Context Command Center</h1>
            <p>Style systems, offerings, services, goods, sitemap context, and delivery folders for LinkGraph writers working across active client accounts.</p>
          </div>
          <div class="stat-stack hero-stats">
            <div><strong>{len(clients)}</strong><span>clients</span></div>
            <div><strong>{total_offerings}</strong><span>offerings mapped</span></div>
            <div><strong>{ok_count}</strong><span>clean crawls</span></div>
          </div>
        </section>
        <section class="report-meta">
          <span>Generated {esc(generated)}</span>
          <span>SearchAtlas internal context excluded</span>
        </section>
        <section class="grid cards">{cards}</section>
        """,
        current="index",
    )


def render_index_card(client: ClientContext) -> str:
    intel = client.website_intelligence
    return f"""
    <a class="card client-card" href="{esc(client_filename(client.slug))}">
      <div class="card-topline">
        <div class="kicker">{esc(client.slug)}</div>
        <span class="status-pill">{esc(intel.get('status', 'missing'))}</span>
      </div>
      <h2>{esc(client.display_name)}</h2>
      <p>{len(client.offerings)} offerings, services, goods, or product lines captured for writers.</p>
      <div class="metrics">
        <span>{intel.get('url_count', 0)} URLs</span>
        <span>{len(intel.get('product_or_service_urls', []))} product/service URLs</span>
      </div>
    </a>
    """


def client_filename(slug: str) -> str:
    return slug.replace("/", "__") + ".html"


def render_client_page(client: ClientContext) -> str:
    intel = client.website_intelligence
    offerings = "\n".join(render_offering(item) for item in client.offerings[:MAX_OFFERINGS])
    context_cards = "\n".join(
        [
            render_context_card("Quick Facts", client.quick_facts, "Company, audience, and proof points."),
            render_context_card("Voice", client.voice_rules, "How this client should sound."),
            render_context_card("Avoid / Compliance", client.avoid_rules, "Claims, terms, and wording to avoid."),
            render_context_card("Terminology", client.terminology, "Client-specific naming and required language."),
        ]
    )
    sources = "\n".join(
        f"<li><code>{esc(doc.path)}</code> — {esc(doc.title)}</li>" for doc in client.source_docs
    )
    website_pages = "\n".join(render_sample_page(page) for page in intel.get("sample_pages", [])[:16])
    product_urls = render_list(intel.get("product_or_service_urls", [])[:80], empty="No product/service URLs classified from sitemap paths.")
    semantic_topics = render_topic_chips(client.semantic_topics, empty="No semantic topics extracted.")
    style_sections = "\n".join(render_style_section(section) for section in client.style_sections)
    body = f"""
    <nav class="topnav">
      <a class="brand" href="index.html"><span>LG</span>LinkGraph</a>
      <a class="nav-link" href="index.html">All clients</a>
    </nav>
    <section class="hero client-hero">
      <div class="hero-copy">
        <div class="kicker">{esc(client.slug)}</div>
        <h1>{esc(client.display_name)}</h1>
        <p>{len(client.offerings)} extracted offerings, {intel.get('url_count', 0)} sitemap URLs, and {len(client.source_docs)} local source documents for client-specific writing context.</p>
      </div>
      <div class="stat-stack">
        <div><strong>{esc(intel.get('status', 'missing'))}</strong><span>crawl status</span></div>
        <div><strong>{intel.get('url_count', 0)}</strong><span>URLs found</span></div>
        <div><strong>{len(intel.get('product_or_service_urls', []))}</strong><span>product/service URLs</span></div>
      </div>
    </section>
    <section class="layout">
      <main>
        <section class="context-grid">{context_cards}</section>
        <section class="panel">
          <h2>Offerings, Services, Goods</h2>
          <p class="muted">Writer-facing catalog from the client style system, approved source files, and usable product/service pages. Raw crawl evidence is separated below.</p>
          <div class="offerings">{offerings or '<p>No offerings extracted.</p>'}</div>
        </section>
        <section class="panel">
          <h2>Website Intelligence</h2>
          <div class="split">
            <div>
              <h3>Website URLs</h3>{render_list(intel.get('website_urls', []), empty='No website URLs found.')}
              <h3>Sitemaps</h3>{render_list(intel.get('sitemaps', []), empty='No usable sitemaps found.')}
            </div>
            <div>
              <h3>Semantic / Topical Terms</h3>{semantic_topics}
              <h3>Blockers</h3>{render_list(intel.get('blockers', []), empty='None')}
            </div>
          </div>
          <h3>Product / Service URLs</h3>{product_urls}
          <h3>Sampled Pages</h3><div class="sample-pages">{website_pages}</div>
        </section>
        <section class="panel">
          <h2>Full Style System</h2>
          <details open><summary>Show style-system sections</summary>{style_sections}</details>
        </section>
        <section class="panel">
          <h2>Local Source Files Read</h2>
          <ul>{sources}</ul>
        </section>
      </main>
    </section>
    """
    return html_page(f"{client.display_name} Context", body, current=client.slug)


def render_context_card(title: str, items: list[str], note: str) -> str:
    return f"""
    <article class="context-card">
      <div class="aside-label">{esc(title)}</div>
      <p class="context-note">{esc(note)}</p>
      {render_list(items, empty='No clean lines extracted yet.')}
    </article>
    """


def render_topic_chips(items: list[str], empty: str) -> str:
    if not items:
        return f"<p class=\"muted\">{esc(empty)}</p>"
    return "<div class=\"topic-chips\">" + "".join(f"<span>{esc(item)}</span>" for item in items[:30]) + "</div>"


def render_offering(item: dict[str, Any]) -> str:
    evidence = ", ".join(item.get("sources", [])[:MAX_EVIDENCE])
    sections = ", ".join(item.get("sections", [])[:3])
    description = item.get("description") or "No short description extracted yet."
    return f"""
    <article class="offering">
      <div class="offering-marker"></div>
      <h3>{esc(item['name'])}</h3>
      <p>{esc(description)}</p>
      <div class="evidence">Sources: {esc(evidence)}{f' · Sections: {esc(sections)}' if sections else ''}</div>
    </article>
    """


def render_sample_page(page: dict[str, Any]) -> str:
    headings = render_list(page.get("headings", [])[:8], empty="No headings captured.")
    return f"""
    <article class="sample">
      <h4>{esc(page.get('title') or page.get('url'))}</h4>
      <a href="{esc(page.get('url'))}">{esc(page.get('url'))}</a>
      <p>{esc(page.get('meta_description', ''))}</p>
      {headings}
    </article>
    """


def render_style_section(section: dict[str, str]) -> str:
    text = section["text"].strip()
    if len(text) > 12_000:
        text = text[:12_000] + "\n\n[Section truncated in HTML. Open STYLE-SYSTEM.md for full text.]"
    return f"""
    <details class="style-section">
      <summary>{esc(section['title'])}</summary>
      <div class="markdown">{render_markdown_excerpt(text)}</div>
    </details>
    """


def render_list(items: list[Any], empty: str) -> str:
    if not items:
        return f"<p class=\"muted\">{esc(empty)}</p>"
    return "<ul>" + "".join(f"<li>{render_link_or_text(item)}</li>" for item in items) + "</ul>"


def render_link_or_text(item: Any) -> str:
    text = str(item)
    if text.startswith(("http://", "https://")):
        return f"<a href=\"{esc(text)}\">{esc(text)}</a>"
    return esc(text)


def html_page(title: str, body: str, current: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <style>
    :root {{
      --bg:#f4f7f5; --panel:#ffffff; --ink:#09110f; --muted:#63716c; --line:#dce5df;
      --black:#050907; --graph:#14d878; --graph-dark:#079d55; --soft:#eaf8f0; --soft-ink:#19392a;
      --accent:#087a47; --red:#b5362d; --shadow:0 18px 46px rgba(5,9,7,.08);
    }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background:
      linear-gradient(180deg, #ffffff 0, var(--bg) 360px); color:var(--ink); line-height:1.45; }}
    a {{ color:var(--accent); text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}
    .topnav {{ min-height:64px; padding:14px max(32px, calc((100vw - 1380px) / 2 + 32px)); background:var(--black); border-bottom:1px solid rgba(255,255,255,.08); position:sticky; top:0; z-index:2; display:flex; align-items:center; justify-content:space-between; gap:18px; }}
    .brand {{ color:#fff; display:inline-flex; align-items:center; gap:10px; font-weight:800; letter-spacing:0; }}
    .brand:hover {{ text-decoration:none; }}
    .brand span {{ width:32px; height:32px; border-radius:8px; background:var(--graph); color:var(--black); display:inline-grid; place-items:center; font-size:13px; font-weight:900; }}
    .nav-meta, .nav-link {{ color:#b8c6c0; font-size:13px; font-weight:700; }}
    .hero {{ margin:0; padding:42px max(32px, calc((100vw - 1380px) / 2 + 32px)) 38px; background:var(--black); color:#fff; border-bottom:1px solid rgba(255,255,255,.08); }}
    .index-hero, .client-hero {{ display:flex; justify-content:space-between; gap:28px; align-items:flex-start; }}
    .hero h1 {{ margin:0 0 12px; font-size:clamp(32px, 5vw, 62px); line-height:.98; letter-spacing:0; max-width:900px; }}
    .hero p {{ margin:0; color:#c7d5cf; max-width:840px; font-size:17px; }}
    .hero-copy {{ max-width:940px; }}
    .kicker {{ color:var(--graph); font-size:12px; text-transform:uppercase; letter-spacing:.08em; font-weight:900; }}
    .report-meta {{ display:flex; flex-wrap:wrap; gap:10px; padding:14px 32px; background:#fff; border-bottom:1px solid var(--line); color:var(--muted); font-size:13px; max-width:1380px; margin:0 auto; }}
    .report-meta span {{ background:var(--soft); color:var(--soft-ink); border-radius:999px; padding:6px 10px; font-weight:700; }}
    .grid.cards {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(290px, 1fr)); gap:16px; padding:24px 32px 42px; max-width:1380px; margin:0 auto; }}
    .card, .panel, .context-card {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; box-shadow:var(--shadow); }}
    .client-card {{ display:block; padding:20px; color:inherit; min-height:184px; transition:transform .15s ease, border-color .15s ease, box-shadow .15s ease; }}
    .client-card:hover {{ text-decoration:none; transform:translateY(-2px); border-color:rgba(20,216,120,.55); box-shadow:0 24px 58px rgba(5,9,7,.12); }}
    .card-topline {{ display:flex; justify-content:space-between; gap:10px; align-items:center; }}
    .client-card h2 {{ margin:14px 0 8px; font-size:23px; line-height:1.1; }}
    .client-card p {{ margin:0; color:var(--muted); }}
    .metrics {{ display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }}
    .metrics span, .evidence, .status-pill {{ background:var(--soft); border:1px solid rgba(20,216,120,.22); border-radius:999px; padding:5px 9px; font-size:12px; color:var(--soft-ink); font-weight:800; }}
    .topic-chips {{ display:flex; flex-wrap:wrap; gap:8px; margin:8px 0 18px; }}
    .topic-chips span {{ background:#f6fbf8; border:1px solid var(--line); border-radius:999px; color:#183a2a; padding:7px 10px; font-size:13px; font-weight:750; }}
    .layout {{ display:block; padding:22px 32px 46px; max-width:1380px; margin:0 auto; }}
    main {{ min-width:0; }}
    .context-grid {{ display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:14px; margin-bottom:20px; }}
    .context-card {{ padding:18px; min-height:220px; }}
    .context-card ul {{ margin-bottom:0; }}
    .context-note {{ color:var(--muted); font-size:13px; margin:4px 0 12px; }}
    .aside-label {{ color:var(--graph-dark); font-size:11px; text-transform:uppercase; font-weight:900; letter-spacing:.08em; margin-bottom:5px; }}
    .panel h2 {{ margin-top:0; }}
    .panel {{ padding:22px; margin-bottom:20px; }}
    .panel h2 {{ font-size:26px; letter-spacing:0; }}
    .offerings {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:13px; margin-top:16px; }}
    .offering, .sample {{ border:1px solid var(--line); border-radius:8px; padding:15px; background:#fff; }}
    .offering {{ position:relative; overflow:hidden; }}
    .offering-marker {{ position:absolute; inset:0 auto 0 0; width:4px; background:var(--graph); }}
    .offering h3, .sample h4 {{ margin:0 0 6px; }}
    .offering p {{ margin:0 0 10px; }}
    .split {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
    .stat-stack {{ display:grid; grid-template-columns:repeat(3, minmax(100px, 1fr)); gap:8px; min-width:340px; }}
    .stat-stack div {{ border:1px solid rgba(255,255,255,.15); border-radius:8px; padding:14px; background:rgba(255,255,255,.06); }}
    .stat-stack strong {{ display:block; font-size:26px; color:#fff; }}
    .stat-stack span, .muted {{ color:var(--muted); font-size:13px; }}
    .hero .stat-stack span {{ color:#b8c6c0; }}
    ul {{ padding-left:20px; }}
    li {{ margin:4px 0; }}
    code {{ background:var(--soft); color:var(--soft-ink); padding:2px 4px; border-radius:4px; }}
    details {{ margin:10px 0; }}
    summary {{ cursor:pointer; font-weight:700; }}
    .style-section {{ border-top:1px solid var(--line); padding-top:10px; }}
    .markdown {{ color:#2d2f35; }}
    @media (max-width: 980px) {{
      .layout, .split, .client-hero, .index-hero {{ grid-template-columns:1fr; display:block; }}
      .context-grid {{ grid-template-columns:1fr; }}
      .stat-stack {{ min-width:0; margin-top:16px; }}
      .hero, .grid.cards, .layout, .topnav, .report-meta {{ padding-left:16px; padding-right:16px; }}
      .hero h1 {{ font-size:36px; }}
      .stat-stack {{ grid-template-columns:1fr; }}
    }}
  </style>
</head>
<body>{body}</body>
</html>
"""


def write_outputs(clients: list[ClientContext]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "index.html").write_text(render_index(clients), encoding="utf-8")
    for client in clients:
        (OUT_DIR / client_filename(client.slug)).write_text(render_client_page(client), encoding="utf-8")
    DATA_PATH.write_text(json.dumps(to_data(clients), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def to_data(clients: list[ClientContext]) -> dict[str, Any]:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "client_count": len(clients),
        "clients": [
            {
                "slug": client.slug,
                "display_name": client.display_name,
                "offerings": client.offerings,
                "semantic_topics": client.semantic_topics,
                "quick_facts": client.quick_facts,
                "voice_rules": client.voice_rules,
                "avoid_rules": client.avoid_rules,
                "terminology": client.terminology,
                "website_intelligence": {
                    "status": client.website_intelligence.get("status"),
                    "url_count": client.website_intelligence.get("url_count", 0),
                    "product_or_service_count": len(client.website_intelligence.get("product_or_service_urls", [])),
                },
                "source_files": [doc.path for doc in client.source_docs],
            }
            for client in clients
        ],
    }


def main() -> int:
    clients = discover_clients()
    write_outputs(clients)
    print(f"Built {len(clients)} client pages")
    print(f"Index: {OUT_DIR.relative_to(ROOT) / 'index.html'}")
    print(f"Data: {DATA_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
