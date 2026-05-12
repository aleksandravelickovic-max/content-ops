---
name: Site Auditor
type: product
source: pasted by user on 2026-04-22
last_verified: 2026-04-22
---

## Definition
Site Auditor is a technical SEO crawler that performs full-domain analysis to identify, classify, and quantify on-page and structural issues across web properties.

## How it works
Executes recursive crawling that captures indexability status, Core Web Vitals data, link structure hierarchy, and content markup validation for each URL. Calculates a site health score on a 0 to 1000 scale.

## Crawl configuration
- Parameters: user agent configuration, crawl depth, page limit, scan frequency
- Default crawl speed: 20 pages per second
- Crawl range: 100 to 1,000,000 URLs depending on site size
- Automated re-crawl at 7-day default frequency

## Audit scope
- Metadata: title tags, meta descriptions, H1 structure, canonical signals, hreflang attributes
- Indexability: blocked pages, redirect chains, orphaned URLs, canonical conflicts
- Domain-level: sitemap accessibility, robots.txt configuration, SSL implementation, structured data deployment

## Dashboard views
- Overview
- Page Explorer: individual URLs with health scores, depth values, schema type classifications, status codes 200 to 500
- Domain Level: cross-page issues consolidated

## How-to-Fix system
- Each issue links to prescriptive resolution steps
- Error definition
- Impact assessment
- Correction procedures

## Export formats
- XLS
- Google Docs
- CSV

## Integrations
- Report Builder
- Google Search Console (GSC)
- Google Analytics 4 (GA4)
