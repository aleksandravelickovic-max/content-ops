# 5Gstore — Style System

Generated: 2026-05-17
Sources: raw/research/client-overview.md, raw/research/company-profile.md
Base rules: universal-rules/UNIVERSAL-RULES.md

---

## 1. Brand & Audience

**What 5Gstore is:** A specialized online retailer for 4G and 5G cellular networking equipment — routers, antennas, signal boosters, and accessories. Differentiated by non-commissioned technical staff who guide customers from product selection through post-purchase troubleshooting.

**Parent company:** MDG Connected Solutions (acquired by Connected Solutions Group on January 27, 2026; founders Michael and Julia Ginsberg remain in brand leadership).

**Trust signals to reference when relevant:**
- A+ BBB rating (15+ consecutive years)
- Thousands of verified 5-star reviews on Shopper Approved and Google Shopping
- GSA-approved contractor
- EV SSL security

**Primary audiences:**

| Segment | Core Need |
|---|---|
| Remote workers / home users | Fix weak indoor cellular signal |
| RV owners / mobile internet users | Maintain connectivity on the move |
| Small businesses | Reliable cellular backup internet |
| Enterprise IT teams | Scalable mobile connectivity deployments |
| System integrators / network pros | Technical compatibility and sourcing |

Content must speak to technical buyers. These audiences research before purchasing and expect specificity — model numbers, band compatibility, throughput specs, use case fit.

---

## 2. Voice & Tone

**Core tone attributes:**

| Attribute | Writing Rule |
|---|---|
| Technical | Specify bands, throughput, ports, certifications — not vague claims |
| Direct | Lead with the problem or the product capability, not a preamble |
| Expert without jargon overload | Define terms on first use when writing for mixed audiences |
| Trustworthy | Cite specs from verified sources; flag anything unconfirmed |
| Practical | Focus on setup, compatibility, real-world use cases |

**Avoid:**
- Marketing fluff: "cutting-edge," "next-generation," "best-in-class"
- Vague connectivity language: "stay connected," "blazing speeds," "seamless internet"
- Overpromising signal improvement without stating conditions
- Reproducing manufacturer manual text verbatim

---

## 3. Terminology

### 3.1 Required terms

| Term | Rule |
|---|---|
| **5Gstore** | Always written exactly as: `5Gstore` — capital G, lowercase s, no space |
| Cellular connectivity | Preferred over "wireless internet" when referring to mobile broadband |
| Signal strength | Use over "signal quality" unless specifically referring to quality metrics |
| Mobile broadband | Use for general cellular internet references |
| Non-commissioned | Use when referencing 5Gstore's sales staff differentiator |
| SpeedFusion bonding | Exact Peplink product name — do not paraphrase |
| FirstNet Band 14 | Exact name for emergency-priority LTE band — use when relevant |

### 3.2 Strict avoidance list

| Banned | Reason |
|---|---|
| 5GStore | Wrong capitalization |
| 5G Store | Wrong — two words |
| Blazing fast / lightning fast | Generic, unverifiable |
| Seamless connectivity | Filler claim |
| Game-changing | Banned per universal rules |
| Simply plug in | Oversimplifies technical setup |
| Revolutionary | Generic authority claim |

---

## 4. Accuracy & Technical Standards

- **Specs must come from verified sources** in `raw/` or clearly identified product documentation. Do not invent specs.
- **Band compatibility** must be stated explicitly when writing about routers, hotspots, and boosters — do not generalize.
- **Capacity claims** (e.g., "supports up to 500 users") must match the product spec sheet.
- **Firmware requirements** for software products (e.g., SpeedFusion Connect licenses) must be stated.
- **Restrictions and limitations** must be disclosed — e.g., license stacking rules, SIM slot limitations, PoE requirements.
- When writing about signal improvement, do not guarantee outcomes. State what the hardware does, not what signal levels the customer will achieve.
- Flag any product capability not confirmed in `raw/` with `⚠ UNVERIFIED`.

---

## 5. Specificity Rules

- State model numbers in full on first reference. Example: "Peplink Balance 310 5G Router" — not "the Balance 310" or "the Peplink router."
- When citing throughput, include the conditions. Example: "1 Gbps router throughput" — not "gigabit speeds."
- When citing temperature range for industrial hardware, use exact values. Example: "-40°C to +70°C" — not "wide operating temperature."
- When referencing the BBB rating, write: "A+ rating with the Better Business Bureau" — not "top-rated."
- When referencing customer reviews, reference the platform (Shopper Approved, Google Shopping) — not just "thousands of reviews."

---

## 6. Page Structure

### Product pages

Follow the four-component framework:

**Component 1 — Product Header & Cart Module**
- Title format: `[Brand] [Model Name] | [Primary Benefit/Core Spec Line]`
- Status flags directly below cart (special order, license requirements, serial number notices)

**Component 2 — Core Narrative (Problem → Solution)**
- Open with the problem the product solves (dropped calls, POS downtime, no wired option)
- Explain the mechanism: how this specific hardware or software addresses the problem
- Do not reproduce manufacturer documentation verbatim

**Component 3 — Scannable Features & Vertical Use Cases**
Break into audience-specific blocks:
- Retail/Hospitality: POS continuity, failover speed
- Remote Work/Power Users: bandwidth aggregation, video conferencing reliability, cloud access
- Industrial/Mobile: fanless build, temperature range, FirstNet Band 14

**Component 4 — Technical Specification Table**
Always include a Markdown attribute/value table for:
- Frequency bands
- Input/output power specs
- Port configurations
- Capacity (users, throughput)
- Build specs (dimensions, operating temp, ingress rating if applicable)

### Landing pages

Use the reusable structure below:

1. **Hero** — H1 with primary keyword, short subheadline, primary CTA
2. **Core Pain** — H2 intro, H3 pain points with short explanations
3. **Solution** — H2 intro, H3 solution blocks, short explanation each
4. **Trust / Social Proof** — outcomes, trust signals (BBB, reviews, GSA), stats
5. **FAQ** — persona-specific questions, expanded answers, no repetition from above sections

---

## 7. SEO Standards

### Meta titles

Format: `[Product Name] [Core Feature] | 5Gstore`
Length: 50–60 characters maximum

Example: `Peplink Balance 310 5G Router with PrimeCare | 5Gstore`

### Meta descriptions

Format: Actionable, problem-solving phrasing. Include at least one technical differentiator (throughput, band, port config) to prevent cannibalization across similar product pages.
Length: 150–160 characters maximum

Example: `Deploy the Peplink Balance 310 5G with dual modems (5G/Cat 20 & Cat 12 LTE). Features 1Gbps throughput and SpeedFusion bonding. Order now at 5Gstore.`

### Keyword usage

- Primary keyword in H1 and first sentence of body content
- Use exact-match product names and model numbers — these are high-intent search terms
- Do not duplicate meta descriptions across product categories — use dynamic technical differentiators
- Internal links: place the focus link as high in the content as it naturally fits

### Audience-to-keyword mapping

| Persona | Primary Keyword | Usage |
|---|---|---|
| CRO / CSO | CRO Revenue Predictability Software | H1 + 5x in content |
| VP Sales Operations | Sales Ops CRM Alignment Tool | H1 + 5x in content |
| Account Executive | Enterprise Account Strategy Tool | H1 + 5x in content |
| CTO / Head of IT | Salesforce-Native Revenue Execution Platform | H1 + 5x in content |
| VP Sales Enablement | Sales Methodology Enforcement Tool | H1 + 5x in content |

---

## 8. Product / Collection Reference

### Key product categories

| Category | Examples |
|---|---|
| Enterprise Routers | Peplink Balance 310 5G, Peplink Balance 310X 5G |
| Mobile Hotspots | Inseego MiFi X PRO 5G |
| Hardware Accessories | Peplink Splitter MAX |
| Software Licenses / Cloud Services | Peplink SpeedFusion Connect |
| Antennas | Referenced in use cases; specific models TBD in campaigns |
| Signal Boosters | Referenced in use cases; specific models TBD in campaigns |

### Notable product specs (verified)

**Peplink Balance 310 5G Router**
- 1x Global 5G/Cat 20 modem + 1x Cat 12 LTE modem
- 1 Gbps router throughput
- Capacity: 50–500 users
- Includes 1-Year PrimeCare (InControl2, SpeedFusion bonding, WAN smoothing)
- No built-in Wi-Fi — requires external access point

**Peplink Balance 310X 5G Router**
- Built-in 5G modem + 2x Ethernet WAN
- 2.5 Gbps router throughput
- Capacity: up to 500 users
- Fanless, industrial temperature range, FirstNet Ready (Band 14)
- 2x Mini-SIM (2FF) slots — 1 active at a time

**Inseego MiFi X PRO 5G Mobile Hotspot**
- 5G Sub-6, C-Band, LTE Cat 20
- Wi-Fi 6
- 1 Gbps RJ45 Ethernet Port
- 5050 mAh Li-Ion battery with Quick Charge 3.0

**Peplink Splitter MAX**
- PoE Input: 802.3bt 48W
- DC Output: 12V 48W
- 2.5 Gbps Ethernet interface
- Industrial metal, fanless, -40°C to +70°C

**Peplink SpeedFusion Connect — Unlimited Plan (1 Year)**
- Unlimited cloud traffic, speeds up to 400 Mbps
- Firmware requirement: 8.1.0 or higher
- Does NOT stack with other SFC-CLD plans
- Max accumulated validity: 3 years

---

## 9. Pre-Submission Checklist

Before submitting any content for 5Gstore:

- [ ] Company name written as `5Gstore` throughout (not 5GStore or 5G Store)
- [ ] Product model numbers written in full on first reference
- [ ] All specs sourced from `raw/` or verified product documentation — nothing invented
- [ ] Unverified claims flagged with `⚠ UNVERIFIED`
- [ ] Meta title: 50–60 characters, format `[Product Name] [Core Feature] | 5Gstore`
- [ ] Meta description: 150–160 characters, includes technical differentiator
- [ ] No duplicate meta descriptions across product pages
- [ ] Technical spec table included on product pages
- [ ] No manufacturer manual text reproduced verbatim
- [ ] Status flags included below cart for special-order items or license requirements
- [ ] Internal links placed as high in content as naturally fits
- [ ] No banned language (see §3.2 and universal rules §2.2)
- [ ] Signal improvement claims describe mechanism — do not guarantee outcomes
