---
name: human-writing
description: Rewrite, edit, QA, or draft LinkGraph client content so it sounds human, client-specific, and free of AI slop. Use for any client article, landing page, email, social post, ad copy, report, outline, brief, or revision where the writing must avoid generic AI cadence, cliches, filler, fake authority, and cross-client voice drift across 20+ LinkGraph clients.
---

# Human Writing For LinkGraph Clients

Use this skill as the final writing filter and as the main editing mode for LinkGraph client work. The goal is not prettier prose. The goal is copy that sounds like a real specialist wrote it for the right client, with the right facts, for the right audience.

## Hard Gate

Before writing or editing client content:

1. Identify the client from the user request or file path.
2. Read `clients/{client}/STYLE-SYSTEM.md` in this session.
3. Read `universal-rules/UNIVERSAL-RULES.md` in this session.
4. Treat the client style system as the source of truth when it conflicts with universal rules or this skill.
5. Use only verified facts from the draft, the client style system, `clients/{client}/raw/`, or cited sources. Flag missing facts instead of filling gaps.

If the client is unclear, ask before writing. Do not guess from topic alone.

## Editing Order

Edit in this order:

1. **Accuracy:** remove invented claims, unsupported numbers, vague product promises, compliance risks, and wrong client terminology.
2. **Intent:** make sure the piece answers the searcher, buyer, patient, visitor, or stakeholder early.
3. **Structure:** fix logic, section order, heading specificity, repetition, and transitions before changing style.
4. **Client voice:** match the client style system, not the last client you edited.
5. **Human texture:** remove AI cadence, cliches, decorative rhythm, and generic SEO filler.
6. **SEO fit:** keep natural keyword use, entity clarity, and direct answers without padding.

Do not rewrite good sentences for sport. Preserve strong client-specific language.

## AI Slop To Remove On Sight

Delete or rewrite these patterns:

- Antithesis templates: `not just X but Y`, `more than X, it is Y`, `isn't about X, it's about Y`.
- Rule-of-three rhythm: `fast, simple, and powerful`; `plan, create, optimize`; three parallel clauses that exist for cadence.
- Rhetorical setup: `The result?`, `Here's the thing:`, `What makes this different?`, `Let's dive in`.
- Press-release verbs: `underscores`, `showcases`, `boasts`, `stands as a testament to`, `reflects a broader shift`.
- Generic authority claims: `industry-leading`, `best-in-class`, `world-class`, `next-generation`, `trusted by businesses` unless the client proof says it.
- Decorative transitions: `In today's landscape`, `When it comes to`, `At its core`, `In an ever-evolving world`, `That being said`.
- Fake helpfulness: `It is important to note`, `It is worth mentioning`, `Needless to say`, `Of course`.
- Inflated outcomes: `unlock`, `elevate`, `transform`, `supercharge`, `revolutionize`, `game-changing`, `seamless`, `robust`, `holistic`.
- Ending summaries that restate the article. Stop after the useful final point or CTA.

Literal uses are allowed when they are precise, such as `navigate a menu` or `robust statistical test`. Decorative uses are not.

## Client-Specific Discipline

LinkGraph writers handle many clients. Prevent cross-client contamination:

- Keep each client's banned terms, preferred terms, compliance constraints, geography, audience, and proof points separate.
- Do not carry SearchAtlas SaaS language into healthcare, legal, home services, storage, casino, relocation, aesthetics, or tourism clients.
- Do not carry one client's claims into another client's draft, even when the industries overlap.
- Match regional requirements: British English when the client style system requires it, Canadian cheque/check spelling when required, local geography when specified.
- Keep regulated categories conservative. For medical, addiction treatment, financial, legal, gaming, peptides, and healthcare content, avoid guaranteed outcomes, diagnosis/treatment overclaims, price promises, and unsupported safety claims.
- Use the client's exact product, service, staff, brand, and location names. Do not normalize them into generic terms.

## What Human Copy Sounds Like

Prefer:

- Specific nouns over vague abstractions.
- Mechanism before claim: say how it works before saying it helps.
- One exact detail over a polished generality.
- Plain verbs over inflated verbs.
- Uneven, natural sentence rhythm.
- Direct section openings that answer the heading.
- Transitions that carry logic: `but`, `so`, `because`, `while`, `which`.

Avoid turning every sentence short. Choppy prose can sound as generated as over-polished prose.

## SEO Without Slop

For SEO content:

- Answer the primary query in the first paragraph.
- Use the primary keyword where it fits naturally; never force it into every heading.
- Add sections only when they answer a real user question or cover a needed entity.
- Remove filler sections created only for word count.
- Replace vague benefits with mechanisms, capabilities, examples, eligibility details, service limits, comparisons, or process steps.
- Make headings specific enough to be useful without becoming keyword-stuffed.

## Rewrite Tactics

Use these moves during revision:

- Cut the first sentence when it is setup.
- Replace broad claims with the exact proof available.
- Merge repetitive sections or delete the weaker one.
- Change `can help you` to the actual action when the client proof supports it.
- Replace `solutions` with the named service, product, treatment, platform, tour, case type, or offer.
- Replace `businesses` with the actual audience: agencies, homeowners, researchers, patients, families, operators, employers, storage renters, HR teams, etc.
- Change cliche conclusions into a specific next step, or delete the conclusion.

## QA Checklist

Before returning copy, scan for:

- Client style system was loaded this session.
- Universal rules were loaded this session.
- No unsupported claims, stats, testimonials, guarantees, or invented examples.
- No cross-client terminology drift.
- No banned AI slop patterns.
- No decorative em dashes; use commas, periods, or rewrites.
- No generic authority language.
- No duplicated sections or repeated claims.
- Headings answer real subtopics.
- The draft still matches the client voice after cleanup.

If a draft fails the checklist, revise it before returning it.
