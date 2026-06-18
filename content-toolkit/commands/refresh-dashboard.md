Run the dashboard data generator and update dashboard/data.json with fresh metrics from SearchAtlas and ClickUp.

## What this does

1. Calls the SearchAtlas API for ContentGenius articles and platform quota
2. Calls the ClickUp API for content pipeline task counts (if CLICKUP_API_KEY is set)
3. Calls the SearchAtlas GSC endpoint for 28-day organic performance (if GSC is connected)
4. Scans the local /clients directory for client and draft counts
5. Writes everything to dashboard/data.json

## Steps

Run this command to regenerate:

```bash
cd /Users/aleksandravelickovic/content-ops
python dashboard/generate.py
```

If API keys are not in your environment, export them first:

```bash
export SEARCHATLAS_API_KEY="your_key_here"
export CLICKUP_API_KEY="your_key_here"
export GSC_PROPERTY="sc-domain:searchatlas.com"
python dashboard/generate.py
```

For verbose output:

```bash
python dashboard/generate.py --debug
```

## After refreshing

Open dashboard/index.html in a browser to preview. The page auto-refreshes its data every 5 minutes when hosted.

## Hosting options

**Option A — GitHub Pages (recommended for sharing)**
1. Push this repo to GitHub
2. Go to Settings → Pages → Source: main branch, /dashboard folder
3. Add secrets: `SEARCHATLAS_API_KEY`, `CLICKUP_API_KEY`, `GSC_PROPERTY`
4. The GitHub Actions workflow (.github/workflows/refresh-dashboard.yml) will refresh data every 4 hours automatically
5. Share the Pages URL in the marketing channel

**Option B — Local server (preview only)**
```bash
cd /Users/aleksandravelickovic/content-ops/dashboard
python -m http.server 8080
# Open http://localhost:8080
```

Note: Opening index.html directly as a file:// URL will fail due to browser CORS restrictions on local fetch(). Use a local server instead.
