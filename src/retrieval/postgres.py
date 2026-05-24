"""Postgres full-text retrieval for the free/local retrieval path."""

from __future__ import annotations

import logging
from typing import Any, Protocol

from .fusion import RetrievalDocument

logger = logging.getLogger(__name__)


class CursorFactory(Protocol):
    def cursor(self) -> Any:
        ...


class PostgresFullTextRetriever:
    """Search market events and agent outputs with PostgreSQL full-text search."""

    def __init__(self, connection: CursorFactory | None = None):
        self.connection = connection

    def search(
        self,
        query: str,
        ticker: str | None = None,
        sector: str | None = None,
        limit: int = 20,
    ) -> list[RetrievalDocument]:
        if not self.connection:
            return []

        return [
            *self.search_market_events(query, ticker=ticker, sector=sector, limit=limit),
            *self.search_agent_outputs(query, ticker=ticker, limit=limit),
        ][:limit]

    def search_market_events(
        self,
        query: str,
        ticker: str | None = None,
        sector: str | None = None,
        limit: int = 20,
    ) -> list[RetrievalDocument]:
        sql = """
            SELECT
                event_id,
                headline,
                coalesce(summary, ''),
                source,
                event_type,
                tickers,
                sector,
                ts_rank(
                    to_tsvector('english', headline || ' ' || coalesce(summary, '') || ' ' || coalesce(raw_text, '')),
                    plainto_tsquery('english', %s)
                ) AS rank
            FROM market_events
            WHERE to_tsvector('english', headline || ' ' || coalesce(summary, '') || ' ' || coalesce(raw_text, ''))
                  @@ plainto_tsquery('english', %s)
              AND (%s IS NULL OR %s = ANY(tickers))
              AND (%s IS NULL OR sector = %s)
            ORDER BY rank DESC, published_at DESC
            LIMIT %s
        """
        rows = self._fetchall(sql, (query, query, ticker, ticker, sector, sector, limit))
        docs = []
        for row in rows:
            event_id, headline, summary, source, event_type, tickers, row_sector, rank = row
            text = f"{headline}. {summary}".strip()
            docs.append(
                RetrievalDocument(
                    id=f"event:{event_id}",
                    text=text,
                    source="postgres:market_events",
                    score=float(rank or 0),
                    metadata={
                        "source": source,
                        "event_type": event_type,
                        "tickers": list(tickers or []),
                        "sector": row_sector,
                    },
                )
            )
        return docs

    def search_agent_outputs(
        self,
        query: str,
        ticker: str | None = None,
        limit: int = 20,
    ) -> list[RetrievalDocument]:
        sql = """
            SELECT
                id,
                agent_name,
                ticker,
                output_type,
                output_data::text,
                ts_rank(
                    to_tsvector('english', coalesce(output_data::text, '')),
                    plainto_tsquery('english', %s)
                ) AS rank
            FROM agent_outputs
            WHERE to_tsvector('english', coalesce(output_data::text, '')) @@ plainto_tsquery('english', %s)
              AND (%s IS NULL OR ticker = %s)
            ORDER BY rank DESC, created_at DESC
            LIMIT %s
        """
        rows = self._fetchall(sql, (query, query, ticker, ticker, limit))
        docs = []
        for row in rows:
            output_id, agent_name, row_ticker, output_type, output_text, rank = row
            docs.append(
                RetrievalDocument(
                    id=f"agent_output:{output_id}",
                    text=output_text or "",
                    source="postgres:agent_outputs",
                    score=float(rank or 0),
                    metadata={
                        "agent_name": agent_name,
                        "ticker": row_ticker,
                        "output_type": output_type,
                    },
                )
            )
        return docs

    def _fetchall(self, sql: str, params: tuple[Any, ...]) -> list[tuple[Any, ...]]:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        except Exception as exc:
            logger.warning("Postgres retrieval failed: %s", exc)
            return []
