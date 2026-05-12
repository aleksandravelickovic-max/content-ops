#!/usr/bin/env python3
"""
annotation-api.py

FastAPI server that serves the Content Navigator and provides
annotation CRUD backed by PostgreSQL.

Usage:
    docker-compose up -d          # start Postgres
    python scripts/annotation-api.py   # start API on :8080
"""

import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import asyncpg
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://contentops:contentops@localhost:5433/contentops",
)
ROOT = Path(__file__).resolve().parent.parent
NAVIGATOR_HTML = ROOT / "reports" / "content-navigator.html"

pool: Optional[asyncpg.Pool] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL, min_size=2, max_size=10)
    yield
    await pool.close()


app = FastAPI(title="Content Ops Annotations", lifespan=lifespan)


# ── Models ──────────────────────────────────────────────────────────

class AnnotationCreate(BaseModel):
    document_key: str
    client: str
    author: str
    comment: str
    anchor_exact: Optional[str] = None
    anchor_prefix: Optional[str] = None
    anchor_suffix: Optional[str] = None
    anchor_start_offset: Optional[int] = None
    anchor_end_offset: Optional[int] = None
    anchor_heading: Optional[str] = None
    anchor_paragraph_index: Optional[int] = None


class AnnotationUpdate(BaseModel):
    comment: Optional[str] = None
    status: Optional[str] = None
    resolved_by: Optional[str] = None


class ReplyCreate(BaseModel):
    author: str
    comment: str


# ── Helpers ─────────────────────────────────────────────────────────

def row_to_dict(row):
    d = dict(row)
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.isoformat()
        elif isinstance(v, uuid.UUID):
            d[k] = str(v)
    return d


# ── Routes ──────────────────────────────────────────────────────────

@app.get("/")
async def serve_navigator():
    if not NAVIGATOR_HTML.exists():
        raise HTTPException(404, "Run build-content-navigator.py first")
    return FileResponse(NAVIGATOR_HTML, media_type="text/html")


@app.get("/api/health")
async def health():
    try:
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return {"status": "ok"}
    except Exception as e:
        return JSONResponse({"status": "error", "detail": str(e)}, status_code=503)


@app.get("/api/annotations")
async def list_annotations(
    document_key: Optional[str] = None,
    client: Optional[str] = None,
    status: Optional[str] = None,
):
    clauses = []
    params = []
    i = 1
    if document_key:
        clauses.append(f"a.document_key = ${i}")
        params.append(document_key)
        i += 1
    if client:
        clauses.append(f"a.client = ${i}")
        params.append(client)
        i += 1
    if status:
        clauses.append(f"a.status = ${i}")
        params.append(status)
        i += 1

    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            f"""
            SELECT a.*,
                   coalesce(json_agg(
                       json_build_object(
                           'id', r.id, 'author', r.author,
                           'comment', r.comment, 'created_at', r.created_at
                       ) ORDER BY r.created_at
                   ) FILTER (WHERE r.id IS NOT NULL), '[]') AS replies
            FROM annotations a
            LEFT JOIN annotation_replies r ON r.annotation_id = a.id
            {where}
            GROUP BY a.id
            ORDER BY a.created_at
            """,
            *params,
        )

    results = []
    for row in rows:
        d = row_to_dict(row)
        if isinstance(d["replies"], str):
            import json
            d["replies"] = json.loads(d["replies"])
        results.append(d)
    return results


@app.post("/api/annotations", status_code=201)
async def create_annotation(body: AnnotationCreate):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO annotations
                (document_key, client, author, comment,
                 anchor_exact, anchor_prefix, anchor_suffix,
                 anchor_start_offset, anchor_end_offset,
                 anchor_heading, anchor_paragraph_index)
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)
            RETURNING *
            """,
            body.document_key,
            body.client,
            body.author,
            body.comment,
            body.anchor_exact,
            body.anchor_prefix,
            body.anchor_suffix,
            body.anchor_start_offset,
            body.anchor_end_offset,
            body.anchor_heading,
            body.anchor_paragraph_index,
        )
    return row_to_dict(row)


@app.patch("/api/annotations/{ann_id}")
async def update_annotation(ann_id: str, body: AnnotationUpdate):
    sets = []
    params = []
    i = 1

    if body.comment is not None:
        sets.append(f"comment = ${i}")
        params.append(body.comment)
        i += 1
    if body.status is not None:
        sets.append(f"status = ${i}")
        params.append(body.status)
        i += 1
        if body.status == "resolved":
            sets.append(f"resolved_at = ${i}")
            params.append(datetime.now(timezone.utc))
            i += 1
            if body.resolved_by:
                sets.append(f"resolved_by = ${i}")
                params.append(body.resolved_by)
                i += 1

    if not sets:
        raise HTTPException(400, "Nothing to update")

    sets.append(f"updated_at = ${i}")
    params.append(datetime.now(timezone.utc))
    i += 1

    params.append(uuid.UUID(ann_id))
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            f"UPDATE annotations SET {', '.join(sets)} WHERE id = ${i} RETURNING *",
            *params,
        )
    if not row:
        raise HTTPException(404, "Annotation not found")
    return row_to_dict(row)


@app.delete("/api/annotations/{ann_id}", status_code=204)
async def delete_annotation(ann_id: str):
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM annotations WHERE id = $1", uuid.UUID(ann_id)
        )
    if result == "DELETE 0":
        raise HTTPException(404, "Annotation not found")


@app.post("/api/annotations/{ann_id}/replies", status_code=201)
async def create_reply(ann_id: str, body: ReplyCreate):
    async with pool.acquire() as conn:
        exists = await conn.fetchval(
            "SELECT 1 FROM annotations WHERE id = $1", uuid.UUID(ann_id)
        )
        if not exists:
            raise HTTPException(404, "Annotation not found")
        row = await conn.fetchrow(
            """
            INSERT INTO annotation_replies (annotation_id, author, comment)
            VALUES ($1, $2, $3) RETURNING *
            """,
            uuid.UUID(ann_id),
            body.author,
            body.comment,
        )
    return row_to_dict(row)


@app.get("/api/stats")
async def annotation_stats():
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT client, status, count(*) as count
            FROM annotations
            GROUP BY client, status
            ORDER BY client, status
            """
        )
    stats = {}
    for row in rows:
        c = row["client"]
        if c not in stats:
            stats[c] = {}
        stats[c][row["status"]] = row["count"]
    return stats


if __name__ == "__main__":
    uvicorn.run(
        "annotation-api:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        reload_dirs=[str(ROOT / "scripts")],
    )
