"""Persistence helpers for market events and alerts."""

from __future__ import annotations

import logging
from typing import Any, Protocol

from .models import Alert, MarketEvent

logger = logging.getLogger(__name__)


class CursorFactory(Protocol):
    def cursor(self) -> Any:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...


class EventRepository:
    """Upsert market events and alerts into Postgres."""

    def __init__(self, connection: CursorFactory | None = None):
        self.connection = connection

    def upsert_market_event(self, event: MarketEvent) -> bool:
        if not self.connection:
            return False

        sql = """
            INSERT INTO market_events (
                event_id, source, source_type, source_url, published_at, fetched_at,
                tickers, company_names, sector, event_type, headline, summary,
                raw_text, document_url, severity, sentiment, confidence,
                requires_confirmation, dedupe_hash
            )
            VALUES (
                %(event_id)s, %(source)s, %(source_type)s, %(source_url)s, %(published_at)s, %(fetched_at)s,
                %(tickers)s, %(company_names)s, %(sector)s, %(event_type)s, %(headline)s, %(summary)s,
                %(raw_text)s, %(document_url)s, %(severity)s, %(sentiment)s, %(confidence)s,
                %(requires_confirmation)s, %(dedupe_hash)s
            )
            ON CONFLICT (dedupe_hash) DO UPDATE SET
                fetched_at = EXCLUDED.fetched_at,
                tickers = EXCLUDED.tickers,
                company_names = EXCLUDED.company_names,
                sector = EXCLUDED.sector,
                severity = EXCLUDED.severity,
                sentiment = EXCLUDED.sentiment,
                confidence = EXCLUDED.confidence
        """
        return self._execute(sql, event.model_dump())

    def upsert_alert(self, alert: Alert) -> bool:
        if not self.connection:
            return False

        sql = """
            INSERT INTO alerts (
                alert_id, event_id, ticker, alert_level, alert_score, reason, status, created_at
            )
            VALUES (
                %(alert_id)s, %(event_id)s, %(ticker)s, %(alert_level)s, %(alert_score)s,
                %(reason)s, %(status)s, %(created_at)s
            )
            ON CONFLICT (alert_id) DO UPDATE SET
                alert_level = EXCLUDED.alert_level,
                alert_score = EXCLUDED.alert_score,
                reason = EXCLUDED.reason,
                status = EXCLUDED.status
        """
        return self._execute(sql, alert.model_dump())

    def upsert_event_and_alert(self, event: MarketEvent, alert: Alert) -> bool:
        if not self.connection:
            return False
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(self._event_sql(), event.model_dump())
                cursor.execute(self._alert_sql(), alert.model_dump())
            self.connection.commit()
            return True
        except Exception as exc:
            logger.error("Failed to persist event and alert: %s", exc)
            self.connection.rollback()
            return False

    def _execute(self, sql: str, params: dict[str, Any]) -> bool:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
            self.connection.commit()
            return True
        except Exception as exc:
            logger.error("Persistence failed: %s", exc)
            self.connection.rollback()
            return False

    @staticmethod
    def _event_sql() -> str:
        return """
            INSERT INTO market_events (
                event_id, source, source_type, source_url, published_at, fetched_at,
                tickers, company_names, sector, event_type, headline, summary,
                raw_text, document_url, severity, sentiment, confidence,
                requires_confirmation, dedupe_hash
            )
            VALUES (
                %(event_id)s, %(source)s, %(source_type)s, %(source_url)s, %(published_at)s, %(fetched_at)s,
                %(tickers)s, %(company_names)s, %(sector)s, %(event_type)s, %(headline)s, %(summary)s,
                %(raw_text)s, %(document_url)s, %(severity)s, %(sentiment)s, %(confidence)s,
                %(requires_confirmation)s, %(dedupe_hash)s
            )
            ON CONFLICT (dedupe_hash) DO NOTHING
        """

    @staticmethod
    def _alert_sql() -> str:
        return """
            INSERT INTO alerts (
                alert_id, event_id, ticker, alert_level, alert_score, reason, status, created_at
            )
            VALUES (
                %(alert_id)s, %(event_id)s, %(ticker)s, %(alert_level)s, %(alert_score)s,
                %(reason)s, %(status)s, %(created_at)s
            )
            ON CONFLICT (alert_id) DO UPDATE SET
                alert_level = EXCLUDED.alert_level,
                alert_score = EXCLUDED.alert_score,
                reason = EXCLUDED.reason,
                status = EXCLUDED.status
        """
