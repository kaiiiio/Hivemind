from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from hivemind.data_foundation.models import RawEvidenceCandidate, RawEvidenceRecord


class SQLiteStore:
    def __init__(self, db_path: str | Path = "data/hivemind.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def initialize(self) -> None:
        self.conn.executescript(
            """
            create table if not exists raw_evidence (
                id integer primary key autoincrement,
                source_name text not null,
                source_type text not null,
                source_url text not null,
                fetched_at text not null,
                published_at text,
                title text not null,
                raw_text text not null,
                content_hash text not null unique,
                metadata_json text not null
            );

            create table if not exists parsed_events (
                id integer primary key autoincrement,
                raw_evidence_id integer not null,
                event_type text not null,
                company_name text,
                summary text not null,
                event_amount_inr_cr real,
                sector_tags_json text not null,
                tailwind_tags_json text not null,
                confidence real not null,
                extraction_method text not null,
                created_at text not null,
                foreign key(raw_evidence_id) references raw_evidence(id)
            );

            create table if not exists alerts (
                id integer primary key autoincrement,
                parsed_event_id integer not null,
                swing_score integer not null,
                reason text not null,
                created_at text not null,
                foreign key(parsed_event_id) references parsed_events(id)
            );
            """
        )
        self.conn.commit()

    def save_raw_evidence(self, candidate: RawEvidenceCandidate) -> RawEvidenceRecord:
        fetched_at = datetime.now(timezone.utc)
        content_hash = self._hash_candidate(candidate)
        published_at = candidate.published_at.isoformat() if candidate.published_at else None

        self.conn.execute(
            """
            insert or ignore into raw_evidence (
                source_name, source_type, source_url, fetched_at, published_at,
                title, raw_text, content_hash, metadata_json
            ) values (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                candidate.source_name,
                candidate.source_type,
                candidate.source_url,
                fetched_at.isoformat(),
                published_at,
                candidate.title,
                candidate.raw_text,
                content_hash,
                json.dumps(candidate.metadata, sort_keys=True),
            ),
        )
        self.conn.commit()

        row = self.conn.execute(
            "select * from raw_evidence where content_hash = ?", (content_hash,)
        ).fetchone()
        return self._row_to_raw_evidence(row)

    def save_event(self, event) -> int:
        cursor = self.conn.execute(
            """
            insert into parsed_events (
                raw_evidence_id, event_type, company_name, summary,
                event_amount_inr_cr, sector_tags_json, tailwind_tags_json,
                confidence, extraction_method, created_at
            ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event.raw_evidence_id,
                event.event_type,
                event.company_name,
                event.summary,
                event.event_amount_inr_cr,
                json.dumps(event.sector_tags),
                json.dumps(event.tailwind_tags),
                event.confidence,
                event.extraction_method,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def save_alert(self, parsed_event_id: int, swing_score: int, reason: str) -> int:
        cursor = self.conn.execute(
            """
            insert into alerts (parsed_event_id, swing_score, reason, created_at)
            values (?, ?, ?, ?)
            """,
            (
                parsed_event_id,
                swing_score,
                reason,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def _hash_candidate(self, candidate: RawEvidenceCandidate) -> str:
        digest = hashlib.sha256()
        digest.update(candidate.source_name.encode("utf-8"))
        digest.update(candidate.source_url.encode("utf-8"))
        digest.update(candidate.title.encode("utf-8"))
        digest.update(candidate.raw_text.encode("utf-8"))
        return digest.hexdigest()

    def _row_to_raw_evidence(self, row: sqlite3.Row) -> RawEvidenceRecord:
        published_at = (
            datetime.fromisoformat(row["published_at"]) if row["published_at"] else None
        )
        return RawEvidenceRecord(
            id=int(row["id"]),
            source_name=row["source_name"],
            source_type=row["source_type"],
            source_url=row["source_url"],
            fetched_at=datetime.fromisoformat(row["fetched_at"]),
            published_at=published_at,
            title=row["title"],
            raw_text=row["raw_text"],
            content_hash=row["content_hash"],
            metadata=json.loads(row["metadata_json"]),
        )

