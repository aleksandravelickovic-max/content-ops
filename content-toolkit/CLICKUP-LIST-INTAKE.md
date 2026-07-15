# ClickUp List Intake

The delivery system expects ClickUp list context to be imported as structured data when connector access is available or when a list export is provided.

## Current blocked source

- URL: `https://app.clickup.com/9011399348/v/l/6-901106409002-1?pr=90112087244`
- Status: not accessible from the current Codex session without authenticated ClickUp connector/browser access.

## Import target

Create or update:

```text
dashboard/clickup-delivery-list.json
```

Recommended shape:

```json
{
  "source_url": "https://app.clickup.com/9011399348/v/l/6-901106409002-1?pr=90112087244",
  "exported_at": "2026-07-13T00:00:00Z",
  "tasks": [
    {
      "id": "",
      "name": "",
      "client": "",
      "status": "",
      "assignee": "",
      "due_date": "",
      "url": "",
      "notes": ""
    }
  ]
}
```

## How it should merge

The delivery dashboard should treat this file as operator-owned input:

- match `client` to the slug in `clients/{client}`
- surface task status, owner, due date, and ClickUp URL
- do not overwrite website intelligence or client style systems
- flag unmatched clients instead of guessing

If no ClickUp export is present, the dashboard should continue to work from local client folders and website intelligence files.
