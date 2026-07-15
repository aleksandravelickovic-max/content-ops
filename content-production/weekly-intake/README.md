# Weekly Intake

Drop weekly LinkGraph topic and keyword CSVs here.

Suggested folder pattern:

```text
content-production/weekly-intake/YYYY-MM-DD/topics.csv
```

Required columns:

```text
client,month,type,topic,primary_keyword
```

Recommended full header:

```text
client,month,type,topic,primary_keyword,secondary_keywords,notes,priority,due_date,status
```

Import command:

```bash
python3 scripts/import-weekly-intake.py content-production/weekly-intake/YYYY-MM-DD/topics.csv
```

Then refresh:

```bash
python3 scripts/build-delivery-dashboard.py
python3 scripts/build-client-context-dashboard.py
```

Build the Google Drive export queue:

```bash
python3 scripts/build-google-drive-export.py --month YYYY-MM
```

