# 5Gstore Company Profile & Data Structure

## 1. Core Company Identification

| Field | Detail |
|---|---|
| Company Name | 5Gstore.com (Parent Company: MDG Connected Solutions) |
| Founder | Michael Ginsberg |
| Current Leadership | Michael and Julia Ginsberg |
| Roots | 1980s/1990s as MDG Computer Services, Inc. |
| First eCommerce Launch | 1998 |
| Mobile Broadband Pivot | Around 2005 |
| Corporate Milestones | Inc. Magazine fastest-growing private companies (2018, 2019, 2021) |
| Acquisition | Acquired by Connected Solutions Group (CSG) on January 27, 2026; founders remain in brand leadership |
| Contact/Sales Phone | 833-5GSTORE (833-547-8673) |

## 2. Market Positioning & Differentiators

**Niche:** Specialized online retailer for 4G/5G networking equipment, enterprise-grade routers, antennas, signal boosters, and connectivity accessories.

**Target Audience:** Dual-focus on:
- Home/Prosumer users: digital nomads, remote workers
- Enterprise/B2B clients: maritime, retail failover, first responders

**The 5Gstore Edge:**

- **Non-Commissioned Experts:** Sales and technical support teams guide users from product selection through complex post-purchase troubleshooting.
- **Government/Enterprise Grade:** GSA-approved contractor with strict online deployment security (EV SSL certificates).
- **Trust Metrics:** A+ rating with the Better Business Bureau (15+ consecutive years), thousands of verified 5-star reviews on Shopper Approved and Google Shopping.

## 3. Product Page Content Framework

When generating content for the directory, use the following standardized layout components:

### Component 1: Product Header & Cart Module

- Title Format: `[Brand] [Model Name] | [Primary Benefit/Core Spec Line]`
- Urgent Warnings / Status Flags: Placed directly beneath the cart module.
  - Example (Software/Licenses): "Please have your device serial number ready at checkout."
  - Example (Special Order Hardware): "This is a special-order item that requires additional lead time."

### Component 2: Core Narrative (The Problem-Solver Pitch)

Avoid reproducing manufacturer manuals verbatim to prevent plagiarism and keyword cannibalization.

Structure:
1. **The Problem:** Identify the vulnerability (e.g., dropped Zoom calls, lost retail revenue from a down internet line).
2. **The Solution:** Explain how this specific hardware or license uses software intelligence (e.g., bonding or failover) to keep data flowing.

### Component 3: Scannable Features & Use Cases

Break features down into specific vertical solutions:

- **Retail/Hospitality:** Focus on Point-of-Sale (PoS) continuity.
- **Remote Work/Power Users:** Focus on bandwidth aggregation, video conferencing without jitter, cloud infrastructure access.
- **Industrial/Mobile:** Focus on rugged/fanless designs, wide temperature operations, emergency priority (FirstNet Band 14 compatibility).

### Component 4: Unified Markdown Technical Tables

Always use clear attribute/value Markdown tables for deep technical metrics (Bands, Input/Output Volts, Ports) to maximize SEO crawling efficiency.

## 4. Reference Product Schemas

```json
{
  "SKU_1": {
    "product_name": "Inseego MiFi X PRO 5G Mobile Hotspot",
    "category": "Mobile Hotspots",
    "key_specs": ["5G Sub-6", "C-Band", "LTE Cat 20", "Wi-Fi 6", "1 Gbps RJ45 Ethernet Port"],
    "battery": "5050 mAh Li-Ion with Quick Charge 3.0",
    "best_for": "Portable multi-device connectivity, field deployment, temporary remote offices"
  },
  "SKU_2": {
    "product_name": "Peplink SpeedFusion Connect - Unlimited Plan (1 Year)",
    "category": "Software Licenses / Cloud Services",
    "key_specs": ["Unlimited Cloud Traffic", "Speeds up to 400 Mbps", "Valid for 1 Year"],
    "firmware_req": "8.1.0 or higher",
    "restrictions": "Does NOT stack with other SFC-CLD plans; Max accumulated validity of 3 years",
    "best_for": "Zero-downtime hot failover and app-specific routing without secondary hardware"
  },
  "SKU_3": {
    "product_name": "Peplink Splitter MAX",
    "category": "Hardware Accessories / Power Management",
    "key_specs": ["PoE Input: 802.3bt 48W", "DC Output: 12V 48W", "2.5 Gbps Ethernet Interface"],
    "build": "Industrial Metal, Fanless, -40°C to +70°C operating temperature",
    "best_for": "Powering non-PoE 12V devices over an existing Ethernet run (e.g., Antenna MAX integration)"
  },
  "SKU_4": {
    "product_name": "Peplink Balance 310 5G Router",
    "category": "Enterprise Routers",
    "key_specs": ["1x Global 5G/Cat 20 Modem", "1x Cat 12 LTE Modem", "1 Gbps Router Throughput"],
    "capacity": "50 to 500 users",
    "included_software": "1-Year PrimeCare (InControl2, SpeedFusion bonding, WAN smoothing)",
    "wireless": "No built-in Wi-Fi (requires external Access Point)"
  },
  "SKU_5": {
    "product_name": "Peplink Balance 310X 5G Router",
    "category": "Industrial/Branch Routers",
    "key_specs": ["Built-in 5G Modem", "2x Ethernet WAN", "2.5 Gbps Router Throughput"],
    "capacity": "Up to 500 users",
    "build": "Fanless design, industrial temperature range, FirstNet Ready (Band 14)",
    "sim_slots": "2x Mini-SIM (2FF) slots (1 active at a time)"
  }
}
```

## 5. Technical SEO Implementation Rules

### Meta Title Format (50–60 characters maximum)

`[Product Name] [Core Feature] | 5Gstore`

Example: `Peplink Balance 310 5G Router with PrimeCare | 5Gstore`

### Meta Description Format (150–160 characters maximum)

Use actionable, distinct problem-solving phrasing. Prevent duplication across product classes by adding dynamic technical differentiators (speed capacity, port configurations, etc.) to avoid search engine cannibalization.

Example: `Deploy the Peplink Balance 310 5G with dual modems (5G/Cat 20 & Cat 12 LTE). Features 1Gbps throughput and SpeedFusion bonding. Order now at 5Gstore.`
