from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class RawEvidenceCandidate:
    source_name: str
    source_type: str
    source_url: str
    title: str
    raw_text: str
    published_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RawEvidenceRecord:
    id: int
    source_name: str
    source_type: str
    source_url: str
    fetched_at: datetime
    published_at: datetime | None
    title: str
    raw_text: str
    content_hash: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class ParsedEvent:
    raw_evidence_id: int
    event_type: str
    summary: str
    event_amount_inr_cr: float | None = None
    company_name: str | None = None
    sector_tags: list[str] = field(default_factory=list)
    tailwind_tags: list[str] = field(default_factory=list)
    confidence: float = 0.0
    extraction_method: str = "rules"


@dataclass(frozen=True)
class Alert:
    event: ParsedEvent
    swing_score: int
    reason: str

