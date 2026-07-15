# LinkGraph Dashboard Completion Gaps

This is ready for a directional review, but it is still a prototype. The current version proves the workflow shape: client context, weekly intake, monthly queues, and Drive export. The missing work is mostly around live data, permissions, and production polish.

## Missing For A Complete Dashboard

- Live intake upload: right now the weekly intake starts from a CSV template and a command. The complete version needs an upload surface where a manager can add topics, keywords, client, month, due date, and content type without touching the terminal.
- Editable records in the browser: status, owner, next action, blocker, Drive folder, and review link still live in JSON or generated files. The dashboard needs inline editing with save state.
- Real monthly queue data: the dashboard is ready for monthly deliverables, but no live weekly intake has been imported yet. Once intake is imported, each client should show drafts by month, week, writer, editor, due date, and status.
- Google Drive connection: the current export creates Drive-ready folders locally. The complete version should create or update the actual Google Drive folders and write the final links back into the dashboard.
- Platform upload step: we still need to define the final destination platform, fields required for upload, auth method, and what counts as a successful upload.
- Writer production workspace: writers need a direct draft flow from client context to deliverable brief to draft file. The dashboard should open the exact brief, source docs, client style guide, and deliverable folder.
- Review workflow: editor review, client review, revision, approved, delivered, and published need clear state transitions. Each transition should leave a timestamp and owner.
- QA checks: the dashboard should show no-slop checks, banned phrase checks, missing client offering checks, missing source checks, link checks, and duplicated meta/title warnings.
- Client service coverage: service taxonomy now appears in the cards, but each client still needs a final pass to confirm offerings, service descriptions, product categories, exclusions, and terminology rules.
- Source confidence: website crawl data and local research need source labels. Writers should be able to see what came from the client site, a sitemap, supplied docs, or manual research.
- SearchAtlas/SA separation: SearchAtlas is excluded from the client-facing delivery dashboard, but the full system should make this explicit so internal content never leaks into LinkGraph client views.
- Permissions and sharing: Henry can review the local HTML package, but a complete dashboard needs a hosted review URL, role-based access, and a clean sharing path for directors, CSMs, editors, and writers.
- Archive and history: completed months should stay browsable by client and month. The dashboard should show prior deliverables, published URLs, final docs, and performance follow-up fields.
- Error handling: failed crawls, missing folders, bad CSV rows, duplicate topics, invalid client names, and broken Drive exports should show clear messages in the UI.
- Reporting layer: the director view should summarize client coverage, monthly volume, overdue work, blocked deliverables, review bottlenecks, and handoff completion.

## Strongest Next Build

Build the next version around four tabs: Intake, Client Context, Monthly Production, and Handoff. Keep the current HTML as the review artifact, but move the working system toward a small editable app backed by the repo files and Google Drive.
