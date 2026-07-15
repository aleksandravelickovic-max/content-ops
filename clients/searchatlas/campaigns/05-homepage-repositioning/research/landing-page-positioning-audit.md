# Search Atlas Landing-Page Positioning Audit

**Date:** 2026-06-30 · **Bar:** 2026-06-17 rebrand positioning (STYLE-SYSTEM §2)
**Status note:** `/atlas-agent/` (P1) shipped 2026-06-30 via MR #594 + #599. Everything else below is open.

## Bottom line
The new hero line — *"Search Atlas runs your marketing across every channel and fixes what breaks while you sleep"* — was pasted in as a global subhead on ~15 pages, but the headlines and body copy underneath were never rewritten. So almost every page has an on-positioning subhead sitting on top of old command-and-control, "tool," and DIY copy that contradicts it. Three defects repeat everywhere, and several are single templated strings — fix those first and you lift 10+ pages at once.

## P0 — Sitewide template strings (one edit each, fixes 10+ pages)
Boilerplate, not page-specific. Highest leverage on the board.

| Fix | Where it appears | Why it's wrong |
|---|---|---|
| "Automate your SEO in 1 click" (the Activate OTTO banner) | OTTO, Content Genius, Landing Page Gen, GBP Galactic, Local SEO, DA Checker, Blog Ideas, GMB, Site Auditor/Explorer, Keyword, Backlink, Topical Maps, PatentBrain… | "1 click" is the banned command-and-control lever; contradicts "you don't do the work" |
| "A first-of-its-kind AI SEO tool that will revolutionize the way you do SEO" | Local SEO, Site Auditor, Site Explorer, DA Checker, Topical Maps, GMB, SE Ranking, Enterprise pages, otto-implementer… | Calls Search Atlas a "tool" (Manick's hard ban) + AI filler ("revolutionize," "first-of-its-kind") |
| "1-Click Publishing" / "1-Click X" feature labels | All comparison pages + most product pages (shared tables) | Command-and-control in feature chips |
| Global nav "Atlas Agent" → naming | Every page's header | In-app interface is "Atlas Agent," but the messaging-app/autonomy story should surface the Coworker; nav label is stale brand chrome |
| "SearchAtlas" (one word) in logo/SVG | Site Explorer, Backlink, On-Page Audit, Profound, etc. | Brand is two words — design ticket, not editorial |

## P1 — Highest-traffic / first-touch pages (fix next)
- **/atlas-agent/ — Full overhaul.** The single worst page on the site, built entirely on command-and-control: H1 "One Command Activates Your Entire Marketing Execution," "Control Everything Through Conversation," dead "Atlas Agent" naming. Flip from "you command it" to "it works and reports back unprompted." **✅ SHIPPED 2026-06-30 (MR #594 + #599).**
- **Homepage body — Minor drift, high traffic.** Hero is on-positioning; body still says "Automate your SEO in 1 click" and "OTTO SEO tool / AI SEO tool." Quick, high-visibility win.
- **/features/ — Full overhaul.** Hero promises an autonomous engine; body is a 40+ "tools" catalog. The promise dies after the hero.
- **/pricing/ — Major rewrite.** "You stay in control—deploy automations or approve changes individually" and tier copy built on "managing." Reframe around "priced like a coworker," not a tool stack you operate.

## P2 — Flagship product pages (major rewrite / overhaul)
- **/gbp-galactic/ — Full overhaul.** Most off-brand single line on the site: "Control Every Listing from One Command Center."
- **/otto-seo/ — Major.** "Win Every Search in 1 Click" hero; no agentic story; OTTO reads as a standalone brand, not a Search Atlas skill.
- **/local-seo/, /local-seo-software/, /google-my-business-management-software/ — Full overhaul.** All three call SA a "tool"/"software/dashboard of tools" in the headline, with "Manage… in one dashboard" fighting the autonomy banner below.
- **/content-genius/ — Major.** Antithesis pattern ("isn't a writer. It's a passage-level architect") + "AI Tools" framing.
- **/landing-page-generator/ — Major.** "Build Landing Pages Without Ever Leaving the Dashboard" — console framing; should be SA building pages on its own.
- **/llm-visibility/ — Major.** Shows you what AI says but never closes the loop to the Coworker fixing it. Reads as standalone monitoring.

## P3 — Deeper SEO tool pages (full overhaul, lower traffic)
Site Explorer, Keyword Research, Backlink Analyzer, On-Page Audit, Link-Building Outreach — all framed as DIY data utilities ("drop in a domain," "Browse keywords," "Review backlinks in the dashboard"), three with "Tool" in the H1. Lower priority only because they're bottom-of-funnel, but they need full rewrites.

## Comparison pages — mostly fine, don't over-invest
The shared template already carries the autonomy wedge ("they show, we do"). Surfer and Profound nail it. They need the two P0 string fixes plus:
- **/search-atlas-vs-se-ranking/ — Major.** Inverts the wedge: "Stop managing SEO tools. Start executing your entire marketing stack" tells the buyer to execute. Fix this one hero.
- **/search-atlas-vs-profound/** — change "gives you the tools to act" → "acts on it for you" (currently undercuts self-healing).

## Already aligned — leave alone
**Smart Ads** ("Your Google Ads Run Themselves Now," correct Atlas Agent naming) and **local-citations** are closest to the bar.

## Two things to flag beyond positioning
1. **The Coworker (Slack/Teams/ClickUp) story — pillar 3 — is absent from every single page.** Nothing shows the Coworker posting unprompted. Strategic content gap, not just a copy fix.
2. **Live bugs to fix regardless:** broken hero on /otto-implementer/ ("SEO Success for with an OTTO Implementer"), heading collapse on /otto-pixel/, OTTO boilerplate bled onto /patentbrain/, typo'd subhead on /press-release-software/ ("turned made visible"). Also: /otto-implementer/ sells a human done-for-you service that contradicts "the engine does the work" — needs a positioning decision, not just an edit.
