"""Persistence helpers for agent outputs."""

from __future__ import annotations

import json
import logging
import time
from datetime import UTC, date, datetime
from typing import Any, Protocol

from pydantic import BaseModel

from .local_loop import LocalAgentRun

logger = logging.getLogger(__name__)


class CursorFactory(Protocol):
    def cursor(self) -> Any:
        ...

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...


class AgentOutputRepository:
    """Write schema-validated agent outputs to Postgres."""

    def __init__(self, connection: CursorFactory | None = None):
        self.connection = connection

    def insert_agent_output(
        self,
        agent_name: str,
        output_data: BaseModel | dict[str, Any],
        ticker: str | None = None,
        output_type: str = "EVENT_TRIAGE",
        confidence_score: float | None = None,
        model_used: str = "deterministic-local",
        processing_time_ms: int | None = None,
        run_date: date | None = None,
    ) -> bool:
        if not self.connection:
            return False

        payload = _json_payload(output_data)
        params = {
            "run_date": run_date or datetime.now(UTC).date(),
            "agent_name": agent_name.upper(),
            "ticker": ticker,
            "output_type": output_type,
            "output_data": payload,
            "confidence_score": confidence_score,
            "processing_time_ms": processing_time_ms,
            "model_used": model_used,
        }
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(_insert_sql(), params)
            self.connection.commit()
            return True
        except Exception as exc:
            logger.error("Failed to persist agent output: %s", exc)
            self.connection.rollback()
            return False

    def insert_local_agent_run(
        self,
        run: LocalAgentRun,
        ticker: str | None,
        output_type: str = "EVENT_TRIAGE",
        started_at: float | None = None,
    ) -> int:
        if not self.connection:
            return 0

        processing_time_ms = None
        if started_at is not None:
            processing_time_ms = max(0, int((time.perf_counter() - started_at) * 1000))

        rows = [
            ("SENTINEL", run.sentinel, run.sentinel.priority_score),
            ("NYSA", run.nysa, abs(run.nysa.sentiment_score)),
            ("VERA", run.vera, run.vera.risk_score),
            ("APEX", run.apex, run.apex.confidence),
        ]
        try:
            with self.connection.cursor() as cursor:
                for agent_name, output, confidence in rows:
                    cursor.execute(
                        _insert_sql(),
                        {
                            "run_date": datetime.now(UTC).date(),
                            "agent_name": agent_name,
                            "ticker": ticker,
                            "output_type": output_type,
                            "output_data": _json_payload(output),
                            "confidence_score": confidence,
                            "processing_time_ms": processing_time_ms,
                            "model_used": "deterministic-local",
                        },
                    )
            self.connection.commit()
            return len(rows)
        except Exception as exc:
            logger.error("Failed to persist local agent run: %s", exc)
            self.connection.rollback()
            return 0


def _json_payload(output_data: BaseModel | dict[str, Any]) -> str:
    if isinstance(output_data, BaseModel):
        return output_data.model_dump_json()
    return json.dumps(output_data, default=str)


def _insert_sql() -> str:
    return """
        INSERT INTO agent_outputs (
            run_date, agent_name, ticker, output_type, output_data,
            confidence_score, processing_time_ms, model_used
        )
        VALUES (
            %(run_date)s, %(agent_name)s, %(ticker)s, %(output_type)s,
            %(output_data)s::jsonb, %(confidence_score)s, %(processing_time_ms)s,
            %(model_used)s
        )
    """
