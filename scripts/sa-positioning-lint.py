#!/usr/bin/env python3
"""
Search Atlas positioning + voice linter.

Scans the visible copy of a Search Atlas page for the rebrand-positioning and
voice violations we keep having to catch by hand. Works on:
  - a searchatlas-static page.json  (walks the data fields)
  - a markdown / plain-text draft   (scans the text)

Usage:
    python3 scripts/sa-positioning-lint.py <path-to-page.json|draft.md> [--strict]

Exit code: 1 if any CRITICAL violations (so it can gate a workflow); else 0.
--strict makes WARN-level findings also exit 1.

Rules mirror clients/searchatlas/STYLE-SYSTEM.md §5-6 and the 2026-06-17
positioning guide. It does NOT judge whether copy "answers the question" or
leads with the outcome — that stays a human step (see QA-CHECKLIST.md).
"""
import json
import re
import sys

# ---- rule data (mirrors STYLE-SYSTEM §5.4 / positioning guide) -------------

AI_FILLER = [
    "delve", "leverage", "harness", "robust", "seamless", "elevate", "unlock",
    "supercharge", "game-changing", "game changing", "cutting-edge", "cutting edge",
    "best-in-class", "best in class", "tapestry", "boasts", "testament", "pivotal",
    "ever-evolving", "in today's world", "when it comes to", "that being said",
    "it's worth noting", "dive in", "deep dive", "foster", "empower", "streamline",
    "holistic", "synergy", "realm", "next-generation", "next generation",
    "revolutionize", "powerful", "world-class",
    # additions from the /human-writing banned vocabulary
    "crucial", "vital", "fast-paced", "at its core", "in today's age",
]

# (label, compiled regex, severity)
PATTERNS = [
    # command-and-control — CRITICAL
    ("1-click",        re.compile(r"\b(?:in\s+)?1[\s-]?click\b", re.I), "CRITICAL"),
    ("one-click",      re.compile(r"\bone[\s-]click\b", re.I), "CRITICAL"),
    ("command",        re.compile(r"\bcommand(s|ing)?\b", re.I), "CRITICAL"),
    ("command-center", re.compile(r"\bcommand\s+center\b", re.I), "CRITICAL"),
    ("take-control",   re.compile(r"\btake\s+control\b", re.I), "CRITICAL"),
    # antithesis — CRITICAL
    ("antithesis-notjust",  re.compile(r"\bnot\s+just\b", re.I), "CRITICAL"),
    ("antithesis-doesnt",   re.compile(r"\bdoesn'?t\s+just\b", re.I), "CRITICAL"),
    ("antithesis-isnt",     re.compile(r"\bisn'?t\s+(?:a|an|just|only|about)\b", re.I), "CRITICAL"),
    ("antithesis-itsnot",   re.compile(r"\bit'?s\s+not\b[^.!?]*\bit'?s\b", re.I), "CRITICAL"),
    ("antithesis-notonly",  re.compile(r"\bnot\s+only\b[^.!?]*\bbut\b", re.I), "CRITICAL"),
    # naming — CRITICAL (Search Atlas is TWO words; catch any concatenation)
    ("naming-searchatlas",  re.compile(r"\bsearchatlas\b", re.I), "CRITICAL"),
    ("naming-atlasbrain",   re.compile(r"\bAtlas\s+Brain\b"), "CRITICAL"),
    # tool/software framing — WARN (allowed for competitor stack; confirm by hand)
    ("tool-for-SA",    re.compile(r"\b(tool|tools|software)\b", re.I), "WARN"),
    ("assistant",      re.compile(r"\bassistant\b", re.I), "WARN"),
    # command-and-control — WARN (context-dependent)
    ("manage",         re.compile(r"\bmanage(s|d|ment)?\b", re.I), "WARN"),
    ("from-one-X",     re.compile(r"\bfrom\s+one\s+(dashboard|console|system|place)\b", re.I), "WARN"),
    # user-action framing (Sophia's rule) — WARN
    ("user-you-verb",  re.compile(r"\byou\s+(set|tell|describe|type|ask|just|need|can|get|run|do|click)\b", re.I), "WARN"),
    ("user-tell-it",   re.compile(r"\btell\s+it\b", re.I), "WARN"),
    ("user-say",       re.compile(r"\bsay\s+what\s+you\b", re.I), "WARN"),
    ("user-describe",  re.compile(r"\bdescribe\s+your\b", re.I), "WARN"),
    # /human-writing tells — deterministic ones
    ("setup-payoff",   re.compile(r"\b(here'?s the thing|here'?s the kicker|the result\?|the best part\?|but here'?s the)\b", re.I), "CRITICAL"),
    ("ing-tail",       re.compile(r"\b(making it|highlighting the|cementing|underscoring|solidifying|positioning it as)\b", re.I), "WARN"),
    ("inflated-verb",  re.compile(r"\b(underscores|stands as a testament|speaks to the|reflects a broader)\b", re.I), "WARN"),
    ("throat-clearing", re.compile(r"^(great question|let'?s break this down|let'?s dive in|in this (article|post|guide))\b", re.I), "WARN"),
    ("wrap-up",        re.compile(r"^(in conclusion|ultimately|at the end of the day|in summary)\b", re.I), "WARN"),
    ("em-dash",        re.compile(r"—"), "WARN"),
]
# NOTE: reflexive-triad and staccato detection are too noisy to lint against
# SA copy (legit channel lists everywhere) — they live in the QA-CHECKLIST as
# human-judgment items instead.

# imperative sentence-openers (user-action) — WARN, only on body/title copy >3 words
IMPERATIVE_OPENERS = re.compile(
    r"^(Identify|Launch|Track|Ask|Describe|Tell|Say|Type|Choose|Select|Generate|"
    r"Analyze|Discover|Monitor|Enter|Drop|Browse|Review|Create|Run|Build|Optimize|"
    r"Get|Win|Fix|Produce|Add|Make|Use|Set)\b", re.I)

# JSON keys whose string values are NOT marketing copy — skip them
SKIP_KEYS = {
    "src", "href", "image", "icon", "variant", "id", "type", "component", "slug",
    "template", "canonical", "ogImage", "columnsTemplate", "badge", "alt",
    "post_subtype_id", "content_format", "channel_id", "number", "suffix", "value",
    "width", "height", "initialIndex", "bodyIconAlignment", "mediaImageSizing",
    "quote",  # testimonials are verbatim customer words — exempt from voice rules
}
# repetition check only on flowing marketing copy (not table cells / FAQ answers)
REPETITION_KEYS = {
    "headline", "subheadline", "heading", "title", "html", "descriptionHtml",
    "leadHtml", "description",
}
# keys that hold a heading/title or body copy (imperative-opener check applies)
BODY_TITLE_KEYS = {
    "headline", "subheadline", "heading", "title", "html", "description",
    "descriptionHtml", "leadHtml", "answerHtml", "bodyHtml", "lead", "text",
}

TAG_RE = re.compile(r"<[^>]+>")
ENTITY = {"&amp;": "&", "&#x27;": "'", "&#8217;": "'", "&rsquo;": "'",
          "&#8211;": "-", "&ndash;": "-", "&nbsp;": " ", "&quot;": '"'}


def strip_html(s: str) -> str:
    s = TAG_RE.sub(" ", s)
    for k, v in ENTITY.items():
        s = s.replace(k, v)
    return re.sub(r"\s+", " ", s).strip()


def looks_noncopy(s: str) -> bool:
    s = s.strip()
    if not s:
        return True
    if s.startswith(("/", "#", "http")) or re.fullmatch(r"#?[0-9a-fA-F]{3,8}", s):
        return True
    return False


def walk(node, path, out):
    """Yield (path, key, text) for every copy string in a JSON structure."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k in SKIP_KEYS:
                continue
            walk(v, f"{path}.{k}", out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]", out)
    elif isinstance(node, str):
        if not looks_noncopy(node):
            key = path.rsplit(".", 1)[-1].split("[")[0]
            out.append((path, key, strip_html(node)))


def load_copy(filepath):
    raw = open(filepath, encoding="utf-8", errors="ignore").read()
    try:
        data = json.loads(raw)
        out = []
        walk(data, "root", out)
        return out
    except json.JSONDecodeError:
        # markdown / plain text: one entry per non-empty line
        out = []
        for i, line in enumerate(raw.splitlines()):
            t = strip_html(line).lstrip("#->*| ").strip()
            if t and not looks_noncopy(t):
                out.append((f"line {i+1}", "text", t))
        return out


def lint(filepath):
    copy = load_copy(filepath)
    findings = []  # (severity, label, path, snippet)

    for path, key, text in copy:
        low = text.lower()
        for word in AI_FILLER:
            if re.search(r"\b" + re.escape(word) + r"\b", low):
                findings.append(("CRITICAL", f"ai-filler:{word}", path, text))
        for label, rx, sev in PATTERNS:
            m = rx.search(text)
            if m:
                findings.append((sev, label, path, text))
        if key in BODY_TITLE_KEYS and len(text.split()) > 3 and IMPERATIVE_OPENERS.match(text):
            findings.append(("WARN", "imperative-opener", path, text))

    # repetition: 3+ consecutive body/title strings sharing the first word
    seq = [(p, t) for p, k, t in copy if k in REPETITION_KEYS and t.split()]
    run, last = [], None
    for p, t in seq:
        w = t.split()[0].lower().strip(".,:")
        if w == last:
            run.append((p, t))
        else:
            if len(run) >= 3:
                findings.append(("WARN", f"repetition:'{last}' x{len(run)}", run[0][0],
                                 " / ".join(t[:40] for _, t in run[:4])))
            run, last = [(p, t)], w
    if len(run) >= 3:
        findings.append(("WARN", f"repetition:'{last}' x{len(run)}", run[0][0],
                         " / ".join(t[:40] for _, t in run[:4])))
    return findings


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    if not args:
        print("usage: sa-positioning-lint.py <page.json|draft.md> [--strict]")
        sys.exit(2)
    fp = args[0]
    findings = lint(fp)
    crit = [f for f in findings if f[0] == "CRITICAL"]
    warn = [f for f in findings if f[0] == "WARN"]

    print(f"\nSA POSITIONING LINT — {fp}")
    print("=" * 64)

    def show(group, title):
        if not group:
            return
        print(f"\n{title} ({len(group)}):")
        for sev, label, path, snip in group:
            loc = path.replace("root.", "")
            s = snip if len(snip) <= 110 else snip[:107] + "..."
            print(f"  [{label}]  {loc}")
            print(f"      “{s}”")

    show(crit, "CRITICAL")
    show(warn, "WARN (confirm by hand — 'tool' etc. is fine for competitors)")
    print("\n" + "-" * 64)
    print(f"Summary: {len(crit)} critical, {len(warn)} warn")
    if crit:
        print("FAIL — fix critical findings before publish.")
    elif warn:
        print("PASS with warnings — eyeball the WARN list, then run the QA-CHECKLIST.")
    else:
        print("CLEAN — still run the QA-CHECKLIST for the judgment calls.")
    sys.exit(1 if crit or (strict and warn) else 0)


if __name__ == "__main__":
    main()
