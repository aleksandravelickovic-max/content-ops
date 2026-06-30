# Search Atlas page QA — run before every page ships

Two layers. The linter catches the mechanical violations; this checklist covers
the judgment calls it can't. Run both on **any** searchatlas.com page we change,
**before** showing a preview or opening an MR.

## 1. Run the linter (mechanical)

```
python3 scripts/sa-positioning-lint.py <path-to/page.json>
```

- **Fix every CRITICAL** before anything else (command / 1-click / antithesis /
  AI filler / `SearchAtlas` one-word / `Atlas Brain` / setup-payoff).
- **Eyeball every WARN** and decide: `tool`/`software`/`assistant` and `manage`
  are only OK when they describe the *competitor stack*, never Search Atlas.
  `from one dashboard`, `you …`, imperative openers, em-dashes — rewrite unless
  there's a real reason. `--strict` makes warnings fail too.

## 2. The judgment checklist (human — linter can't see these)

**Positioning**
- [ ] Leads with the **outcome**, not the machine. (What the customer gets, not the console.)
- [ ] Every section/card **answers its own heading** in the agent's voice — "It does X," not "Do X."
- [ ] No **user-action framing** anywhere in the promise copy. The product acts; the reader isn't given a task. ("without you …" is fine — that's *less* work.)
- [ ] Advances at least one of the five pillars (runs while you sleep · self-healing · lives in your workspace · every channel + builds the assets · priced like a coworker). Scope autonomy honestly per page — the hands-off "while you sleep" line belongs to OTTO / the Coworker, not the in-app Atlas Agent.

**Naming**
- [ ] **Search Atlas** — two words, every time.
- [ ] **Atlas Agent** = the in-app conversational agent. **Search Atlas Coworker** = the Slack/Teams/ClickUp presence. Don't conflate or swap them.
- [ ] Sub-products (OTTO, GBP Galactic, Smart Ads, Content Genius) read as skills/features, not co-equal brands in first-touch copy.

**Voice (/human-writing — the parts a regex can't judge)**
- [ ] No **reflexive triad** for rhythm ("fast, simple, and powerful"). A real list of distinct things is fine; three parallel words for cadence is not.
- [ ] No **staccato run** — a row of clipped short sentences. Vary length; join related clauses with but / so / because / while.
- [ ] Not **over-structured** — if three sentences do it, don't make it a bullet deck.
- [ ] No **mid-sentence bolding** to fake emphasis.
- [ ] **Read it aloud.** If you wouldn't say it to a colleague at their desk, rewrite it.

**Facts**
- [ ] Stats and testimonials are the real, cleared versions (not placeholders).
- [ ] Pricing matches current plans ($99/mo anchor traces to plan details).

## 3. Then

Preview → get sign-off → push/MR → reviewer merges. Never skip the preview +
sign-off step (see memory: review before publish).
