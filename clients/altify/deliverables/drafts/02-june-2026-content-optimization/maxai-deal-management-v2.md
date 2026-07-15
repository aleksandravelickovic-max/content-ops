<!--
v2 — restructured to match the LIVE WEBFLOW COMPONENT SHAPE, not freeform markdown.
v1 (maxai-deal-management-v1.md) proposed 5 free-flowing sections including a visible FAQ.
This version keeps v1's retargeting (deal management software / deal management / AI platforms to
prioritize deals and accounts) and its "why this matters" narrative, but fits the copy into the
four component types actually observed on the live page:
  1. Hero
  2. 3-icon pain row (short caption each) + one richtext intro paragraph above it
  3. 4-stat row (short caption each, unchanged in shape) + one richtext intro paragraph above it
  4. 7-item feature repeater (H3 + 1 sentence + 3 bullets each) — kept at 7 slots, not condensed to 4
No visible FAQ is drafted here — see "FAQ — flagged, not drafted" at the bottom.

WEBFLOW DEPENDENCY — apply manually, not deployable via OTTO:
RECOMMENDED TITLE TAG (53 characters): Deal Management Software for Salesforce Teams | MaxAI
RECOMMENDED H1: Deal Management Software Built Inside Salesforce
RECOMMENDED META DESCRIPTION (155 characters): Altify is a deal management software that helps revenue teams prioritize deals and accounts inside Salesforce, improving win rates and forecast accuracy.
CURRENT LIVE VALUES (four different strings across title/og/twitter/schema — standardize on one): see research/live-baseline/maxai-deal-management.md
-->

# Hero

## Deal Management Software Built Inside Salesforce

MaxAI is Altify's deal management software for Salesforce. It ranks deals and accounts using signals already in Salesforce, including stakeholder coverage, deal stage, and buying-group engagement, so reps know which deal needs their attention first.

**[Request a Demo]**

---

# 3-icon pain row

**Richtext intro (above the icons — this is where the narrative goes; the icon captions themselves stay short):**

Deal management breaks down when reps don't know which deal to work on next. Data piles up in Salesforce, but it doesn't rank itself, which pushes revenue teams back onto spreadsheets, gut feel, and whichever opportunity is making the most noise that week. MaxAI ranks that data from inside Salesforce, where reps already work.

**Icon 1 — short caption (was "Guide Sellers"):**
Prioritize by Signal
*Rank deals by buying-group engagement and deal stage.*

**Icon 2 — short caption (was "Eliminate Problem"):**
Catch Risk Early
*Flag a stalled deal weeks before it shows up as "stalled" in a pipeline report.*

**Icon 3 — short caption (was "Boost Adoption"):**
Keep Data Current
*Auto-update relationship maps as buying committees and org charts change.*

---

# 4-stat row

**Richtext intro (above the stats — same move: the stats stay as bare captions, the connecting story lives here):**

None of this is a data problem. Reps already log deals, contacts, and activity in Salesforce every day. The gap is that nobody turns that data into a ranked list of what actually needs attention.

**Stat captions (unchanged facts, only lightly tightened for consistency — no new stats invented):**
- 59% of buyers say sellers don't understand their goals.
- Sellers spend only 30% of their time actually selling.
- 94% of sales leaders want sellers to extract more value from the customer data already in Salesforce.
- 70% of CRM investments fall short on ROI when seller adoption stalls.

---

# 7-item feature repeater (kept at 7 slots to match the live component — not condensed)

### 1. Identify and auto-populate key players
A missing stakeholder is one of the clearest early risk signals a deal review can catch, but only if the map stays current. When a new contact shows up in an email thread or a meeting invite, MaxAI adds them to the account automatically, so the map reflects who's actually involved instead of who was involved at kickoff.
- Fills in contact information automatically as it's discovered.
- Frees up the time reps would spend rebuilding org charts by hand.
- Keeps the buying group visible well past the initial kickoff.

### 2. Uncover critical buying insights
The same account data that flags a missing stakeholder also points to what that account cares about: the goals, pressures, and initiatives actually driving the deal. A rep doesn't have to go digging for it between calls.
- Handles the account research legwork before the rep needs to ask for it.
- Surfaces relationships and data points a rep would otherwise miss.
- Gives reps a way to check the accuracy of what surfaces before they act on it.

### 3. Turn signals into deal execution
Knowing a deal is at risk isn't the same as knowing what to do about it, and that's usually where the trail goes cold. MaxAI closes that gap with a plain-language summary: what's at risk, and the next action to take.
- Spotlights risk in a clear, plain-language summary.
- Delivers real-time coaching on missing stakeholders and overdue reviews.
- Points reps toward the deals that need their time this week.

### 4. Feed the account strategy, not just the deal
A deal doesn't exist in isolation from the account it sits in. MaxAI pulls the same signals up a level, summarizing a company's mission and strategic priorities so a rep can see whether a deal fits where the account is actually headed, not just whether it's likely to close this quarter.
- Summarizes the company's mission and strategic priorities.
- Populates account details automatically, so they're ready before the next QBR.
- Connects account-level context back to which deals get worked first.

### 5. Simplify competitive research
Competitive threats are a risk signal like any other; a deal with an unaddressed competitor should rank differently than one without. MaxAI identifies which competitors are actually relevant to a given opportunity, so that risk shows up in the same priority list instead of a separate spreadsheet.
- Identifies the competitors relevant to a given opportunity.
- Cuts the manual research time reps would spend hunting for this themselves.
- Feeds directly into the same risk and priority signals reps already see.

### 6. Make Salesforce the place sellers want to work
Five capabilities, one effect: none of them add work for the rep. Between auto-populated contacts, surfaced insights, deal summaries, account context, and competitive research, Salesforce starts giving reps something back every time they log in, which is the actual fix for the adoption problem most Salesforce rollouts run into.
- Surfaces the next best action inside the opportunity record itself.
- Embeds qualification, stakeholder mapping, and close planning into the existing workflow.
- Gives managers real-time pipeline visibility without chasing status updates.

### 7. Coach sellers in the flow of work
The same signals driving prioritization are what a coach would flag in a deal review anyway, so MaxAI surfaces them as they happen instead of waiting for the next one. A missing stakeholder or an incomplete qualification step shows up as a prompt inside the opportunity record, not a line item in next week's pipeline meeting.
- Triggers coaching prompts from live deal signals as they change.
- Reinforces Altify's Strategic Account Planning methodology inside the account plan and Relationship Map.
- Gives managers the same visibility into deal signals reps see, so deal reviews focus on the deal itself.

---

# FAQ — flagged, not drafted

The live page has no visible FAQ; there is a hidden FAQPage JSON-LD schema (~30 auto-generated Q&As from OTTO) that is not rendered in the body copy. Several of its answers reference things not evidenced anywhere on the page or in `raw/` ("live webinars," "numerous clients... significant sales growth"). Recommend one of two paths, not a silent content decision:
1. Have a Webflow dev add a visible FAQ component, then draft 5–6 grounded questions against it (I can do this once the component exists).
2. Leave FAQ out of visible copy entirely and have someone audit/replace the hidden OTTO schema separately, since it currently carries unverified claims regardless of what happens with this page.
