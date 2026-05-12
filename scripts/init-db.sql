CREATE TABLE IF NOT EXISTS annotations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_key TEXT NOT NULL,
    client TEXT NOT NULL,
    author TEXT NOT NULL,
    comment TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'open',

    anchor_exact TEXT,
    anchor_prefix TEXT,
    anchor_suffix TEXT,
    anchor_start_offset INTEGER,
    anchor_end_offset INTEGER,
    anchor_heading TEXT,
    anchor_paragraph_index INTEGER,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at TIMESTAMPTZ,
    resolved_by TEXT
);

CREATE INDEX IF NOT EXISTS idx_ann_document ON annotations(document_key);
CREATE INDEX IF NOT EXISTS idx_ann_client ON annotations(client);
CREATE INDEX IF NOT EXISTS idx_ann_status ON annotations(status);

CREATE TABLE IF NOT EXISTS annotation_replies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    annotation_id UUID NOT NULL REFERENCES annotations(id) ON DELETE CASCADE,
    author TEXT NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_reply_annotation ON annotation_replies(annotation_id);
