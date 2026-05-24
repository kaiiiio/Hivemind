"""Market event and alert models."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field


SourceType = Literal["EXCHANGE", "REGULATOR", "NEWS", "COMPANY", "SOCIAL"]
AlertLevel = Literal["INFO", "WATCH", "INVESTIGATE", "HIGH_ALERT", "TRADE_CANDIDATE", "BLOCKED"]


class MarketEvent(BaseModel):
    event_id: str
    source: str
    source_type: SourceType
    source_url: str | None = None
    published_at: datetime
    fetched_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    tickers: list[str] = Field(default_factory=list)
    company_names: list[str] = Field(default_factory=list)
    sector: str | None = None
    event_type: str
    headline: str
    summary: str | None = None
    raw_text: str | None = None
    document_url: str | None = None
    severity: float = Field(ge=0, le=1)
    sentiment: float = Field(default=0, ge=-1, le=1)
    confidence: float = Field(ge=0, le=1)
    requires_confirmation: bool = False
    dedupe_hash: str


class Alert(BaseModel):
    alert_id: str
    event_id: str
    ticker: str | None = None
    alert_level: AlertLevel
    alert_score: float = Field(ge=0, le=1)
    reason: str
    status: Literal["OPEN", "ACKNOWLEDGED", "CLOSED"] = "OPEN"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
