# LinkGraph Writer Guide

Use the command center before writing anything for a LinkGraph client. It tells you what the client offers, how the client sounds, what claims are allowed, and where your deliverable belongs.

## Open The Dashboard

If the local report server is running, open:

```text
http://127.0.0.1:8765/client-context-dashboard/index.html
http://127.0.0.1:8765/linkgraph-delivery-dashboard.html
```

If the server is not running:

```bash
cd /Users/aleksandravelickovic/content-ops
python3 -m http.server 8765 --directory reports
```

Use the client context dashboard first. Use the delivery dashboard to see status, monthly work, and Google Drive handoff state.

## Before You Draft

Open the client's dashboard page and read these sections:

1. Quick context
2. Offering catalog
3. Voice and avoid rules
4. Terminology
5. Website intelligence
6. Source files

Then check the client folder:

```text
clients/{client}/STYLE-SYSTEM.md
clients/{client}/raw/knowledge/service-taxonomy.md
clients/{client}/client-intelligence/offerings.md
clients/{client}/raw/research/website-intelligence.md
```

The `service-taxonomy.md` file is the fastest way to confirm what the client actually sells or provides. Do not invent services, products, treatments, programs, specs, locations, or guarantees.

## Find Your Assignment

Monthly work lives here:

```text
clients/{client}/deliverables/{YYYY-MM}/
```

Each month has:

```text
intake/
briefs/
drafts/
reviews/
final/
platform-uploads/
registry.json
```

Start with the brief:

```text
clients/{client}/deliverables/{YYYY-MM}/briefs/{deliverable_id}.md
```

The brief tells you:

- topic
- primary keyword
- secondary keywords
- notes
- due date
- draft path
- final path
- source context to load

## Where To Put Work

Drafts go here:

```text
clients/{client}/deliverables/{YYYY-MM}/drafts/
```

Reviewed or editor-marked files go here:

```text
clients/{client}/deliverables/{YYYY-MM}/reviews/
```

Approved final files go here:

```text
clients/{client}/deliverables/{YYYY-MM}/final/
```

Upload receipts or platform handoff records go here:

```text
clients/{client}/deliverables/{YYYY-MM}/platform-uploads/
```

Do not save active work in random campaign folders or desktop folders. If a folder is missing, ask before creating a new structure.

## Writing Rules

Follow the client style system first, then the universal rules.

Hard rules:

- Use the exact client terminology.
- Use the exact product, service, treatment, program, model, or location names.
- Do not copy manufacturer or website text verbatim.
- Do not reuse the same meta description across pages.
- Do not add claims that are not in the client folder, website intelligence, or approved source material.
- Do not say a product or service guarantees an outcome unless the source explicitly supports that claim.
- For technical clients, verify specs before writing them.
- For medical, legal, financial, and regulated clients, stay inside confirmed language.

Avoid AI filler:

- cutting-edge
- best-in-class
- seamless
- robust
- game-changing
- unlock
- elevate
- delve
- in today's world
- it's worth noting
- transform your
- oasis
- stunning

If a sentence could fit any client, rewrite it.

## Using Client Offerings

The offering catalog is there so you do not miss context. Use it to answer:

- What does this client actually sell?
- Which services or products are related to this topic?
- What terms must be exact?
- What limitations should be disclosed?
- Which claims need verification?

For example, Altify has products and features such as:

- Altify Insights
- Altify Sales Process
- Altify Opportunities
- Altify Accounts
- Revenue Enablement Services
- MaxAI
- Relationship Map
- Insight Map
- TeamView
- Test and Improve
- Opportunity Map

If you are writing for Altify and mention account planning, relationship mapping, Salesforce-native execution, or revenue enablement, check that taxonomy before drafting.

## Intake Workflow

Weekly topics and keywords are imported from CSV files in:

```text
content-production/weekly-intake/
```

Template:

```text
content-production/weekly-intake/example-topics.csv
```

Import command:

```bash
python3 scripts/import-weekly-intake.py content-production/weekly-intake/YYYY-MM-DD/topics.csv
```

That command creates the monthly registry and brief stubs for each client.

## Google Drive Handoff

Google Drive is the first upload target.

Build the Drive upload queue:

```bash
python3 scripts/build-google-drive-export.py --month YYYY-MM
```

Output:

```text
reports/google-drive-export/{YYYY-MM}/manifest.json
reports/google-drive-export/{YYYY-MM}/upload-plan.md
reports/google-drive-export/{YYYY-MM}/files/
```

The current system prepares the Drive upload queue. It does not upload to Drive yet unless a Drive connector or credentialed adapter is added.

## When You Finish A Draft

Before marking work ready:

- Confirm the file is in the right client/month folder.
- Confirm the piece uses the client terminology.
- Confirm the offering context matches `service-taxonomy.md`.
- Confirm no banned language slipped in.
- Confirm any specs, medical claims, legal claims, financial claims, prices, timelines, and locations are sourced.
- Update the monthly `registry.json` status if you own that step.

Suggested statuses:

```text
intake
brief-ready
drafting
editorial-review
revision
approved
drive-staged
uploaded
published
blocked
```

## If Something Looks Wrong

Stop and flag it if:

- the client page is missing a service you know exists
- the offering catalog includes junk or page-template text
- the brief conflicts with the style system
- the website crawl missed the client's actual navigation
- a required claim is not sourced
- the Drive export plan is missing your file

Fix source context first. Do not patch the final draft to work around bad client knowledge.

