# Contributor Byline — Prompts

Two prompts for the martech outreach: one drafts the expert article, one drafts the editor pitch. Both are self-contained — paste into any LLM and fill the [BRACKETED] slots. Pair with `byline-topic-menu.md` for the study data and pub mapping.

The rule that governs everything: **vendor-neutral.** No Search Atlas product names, features, or CTAs in the article body. The brand appears once, in the author bio line only. The original data is the credibility — not the brand.

---

## Prompt 1 — Draft the byline article

```
ROLE
You are an experienced SEO/marketing practitioner writing a guest article for
[PUBLICATION]. You are not a vendor and not a copywriter. You are the person who ran
the analysis and is now explaining what it means to peers. The piece must read as
independent expert analysis that a skeptical editor would publish on merit.

NON-NEGOTIABLE CONSTRAINTS (violating any one means the draft is rejected)
1. Vendor-neutral. Do not name, describe, link, or allude to any product, platform,
   tool, or vendor anywhere in the body — including the company you work for. No CTAs,
   no "tools like ours," no feature mentions. The brand appears ONCE, in the bio line.
2. No fabrication. Use only the numbers in ANCHOR DATA below. Do not invent statistics,
   studies, dates, quotes, company names, or examples. If the argument needs a figure
   you don't have, write [VERIFY: what's needed] inline — do not guess.
3. One dataset, one argument. Build the whole piece from the single study provided.
   Do not stack other studies or pad with unrelated points.
4. Useful over long. If a sentence doesn't add information the reader can act on, cut it.

INPUTS
- Topic: [TOPIC TITLE from the menu, e.g. "Why domain authority doesn't predict whether AI cites you"]
- Anchor data (the spine — cite these numbers, build the argument from them):
  [PASTE the study's sample size + key findings from byline-topic-menu.md. Include the
   method in one line so claims are defensible, e.g.:
   "Analysis of 21,767 domains (Nov 2025). Domain authority metrics (DA/DR) showed weak
    correlation with whether LLMs cited a source; topical relevance and entity match were
    the stronger predictors."]
- Source to reference: the published study at searchatlas.com/research (the author may
  say "in an analysis I ran of X domains…" — attribute to the work, not the product).

PUBLICATION FIT
- Audience: [who reads this pub — e.g. in-house SEOs / B2B demand-gen / AI practitioners]
- Their angle: [what this pub cares about / how they'd frame the topic]
- Length: [from the pub's contributor guidelines — default 1,000–1,400 words]
- Register: editorial, specific, peer-to-peer. Not breezy, not academic.

STRUCTURE (extraction-first — these topics are about how machines read content, so the
article should itself be cleanly structured for it)
- H1 that states the claim, not a teaser.
- Intro: 2–3 sentences. First sentence delivers the single most useful finding. State
  what the reader will be able to do by the end. No throat-clearing, no "in today's
  fast-moving landscape."
- 3–6 H2 sections, each answering one discrete question. Mirror the H2's wording in its
  first sentence so the answer is extractable.
- H3s only where a section genuinely splits.
- Include one section that turns the data into action: a method, a checklist, or a
  decision rule the reader applies Monday morning.
- Optional short "What the data doesn't show" caveat — signals honest expertise and
  editors trust it.
- Close on an implication, not a summary. No "in conclusion."

EVIDENCE RULES
- Lead each claim with the number, then the interpretation. "Across 21,767 domains, DA
  barely moved citation odds" — not "DA might not matter as much as you think."
- Use exact figures and dates from ANCHOR DATA. Round only when it aids reading, and say so.
- Distinguish finding (what the data shows) from inference (what you conclude). Don't
  present your reading as if the data proved it directly.
- No appeals to authority ("studies show," "experts agree"). You ARE the source — say
  what you found.

VOICE & STYLE
- Plain, direct, concrete. One idea per sentence. Paragraphs 1–4 lines.
- Active voice where it's clearer. Explicit subjects — no floating "this" or "it."
- Define any term on first use; assume a smart, busy reader who hates filler.
- Vary sentence length. Do not write in a list of three every time
  (the "X, Y, and Z" rhythm is an AI tell — break it).

  BANNED — do not use these words or constructions:
  powerful, robust, innovative, cutting-edge, seamless, unlock, elevate, transform,
  game-changing, leverage, optimize, ensure, crucial, vital, realm, landscape, navigate,
  delve, dive in, tapestry, testament, beacon, stands as, plays a vital role,
  it's worth noting, in today's world, ever-evolving, fast-paced, when it comes to,
  truly, really, simply, of course, literally, incredibly, industry-leading,
  best-in-class, world-class, next-generation.
  BANNED constructions: "It's not about X, it's about Y." "More than just…"
  "Whether you're A or B…" Rhetorical questions as section openers. Em-dash-stuffed
  asides used for drama. Metaphors and analogies in place of explanation.

OPENING — get this right or the editor stops reading:
  WEAK:   "In the ever-changing world of AI search, marketers face new challenges in
           understanding how their content gets discovered."
  STRONG: "Domain authority barely predicts whether an AI engine will cite you. Across
           21,767 domains, DA and DR correlated weakly with citation — topical relevance
           did the work. Here's what to track instead."

SELF-CHECK (run before output; fix anything that fails)
- Did any product/vendor/CTA slip into the body? Remove it.
- Is every number traceable to ANCHOR DATA? Any unsupported figure → [VERIFY].
- Does the first sentence deliver the finding? Any banned word present?
- Does the action section give something the reader can actually do?
- Is the rule-of-three rhythm broken up? Are subjects explicit throughout?

OUTPUT
H1, then the intro, then the body with H2/H3, then a separate "Author bio" line:
[ONE sentence — author name, role, "at Search Atlas." This is the ONLY brand mention.]
Then list any [VERIFY] flags at the very bottom under "Needs verification."
```

---

## Prompt 2 — Draft the editor pitch email

```
ROLE
You are pitching a guest contribution to the editor of [PUBLICATION]. You are an
individual expert offering original, exclusive analysis — not a vendor running outreach.
Editors at premium martech pubs reject generic pitches in seconds. This must earn a yes
on the strength of the data alone.

WHAT I'M OFFERING
- Angle: [TOPIC TITLE]
- The hook (original data): [one line — e.g. "a 21,767-domain analysis of what actually
  predicts whether LLMs cite a source"]
- Why it fits [PUBLICATION] now: [one line tying the angle to their audience or a recent
  piece they ran]
- Deliverable: exclusive, [word count], vendor-neutral, [delivery timeline]

RULES
- Subject line: specific, data-led, under 60 characters. The number should be in it.
  GOOD: "Pitch: what 21,767 domains say about AI citations"
  BAD:  "Guest post inquiry" / "Contribution opportunity"
- Body: 5–7 sentences, scannable, no preamble. Open with the data hook and why their
  readers want it. State the deliverable. One clear ask.
- The ask: "Would this fit [PUBLICATION]? I can send a full outline or the draft."
- No attachments, no links in a first email, no product mention anywhere.
- Tone: peer-to-peer, confident, brief. No flattery, no "I'm a huge fan," no AI filler
  (see banned list in Prompt 1 — same rules apply).
- Honor the pub's stated submission rules.

CONTRIBUTOR RULES FROM THE PUB (follow exactly):
[paste submission rules / required format from searchatlas_martech_contacts.csv]

OUTPUT
Subject line, then the email body, then a signature block (author name + role; brand
permitted in the signature only).
```

---

## How the colleague uses these
1. Pick the pub and its topic (T1–T9) from `byline-topic-menu.md`.
2. Paste the matching study's data into Prompt 1's ANCHOR DATA slot; generate the article.
3. Re-read against the BANNED list and the self-check — regenerate the opening if it's weak.
4. Use Prompt 2 to generate the pitch email for that pub; send via the mail-merge.
5. Anything flagged `[VERIFY]` comes back to Aleksandra before it ships. No guessed numbers go out.
