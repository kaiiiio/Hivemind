"""Feedback writer for local episodic and mistake memory."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from agents.local_loop import LocalAgentRun
from events.models import Alert, MarketEvent

from .models import new_run_id
from .redis_store import RedisEpisodicStore


@dataclass(slots=True)
class FeedbackWriteResult:
    episode_key: str | None = None
    mistakes_written: int = 0
    mistake_agents: list[str] = field(default_factory=list)


class FeedbackMemoryWriter:
    """Writes compact T2 memory after deterministic or model-backed runs."""

    def __init__(self, episodic_store: RedisEpisodicStore | None = None):
        self.episodic_store = episodic_store or RedisEpisodicStore()

    def write_event_triage(
        self,
        event: MarketEvent,
        alert: Alert,
        run: LocalAgentRun,
        run_id: str | None = None,
    ) -> FeedbackWriteResult:
        ticker = event.tickers[0] if event.tickers else "UNRESOLVED"
        run_id = run_id or new_run_id()
        episode_key = self.episodic_store.write_episode(
            ticker=ticker,
            run_date=run_id,
            episode=_episode_payload(event, alert, run, run_id),
        )

        mistakes_written = 0
        mistake_agents: list[str] = []
        for agent_name, mistake in _mistake_payloads(event, alert, run, run_id):
            self.episodic_store.append_mistake(agent_name, mistake)
            mistakes_written += 1
            mistake_agents.append(agent_name)

        return FeedbackWriteResult(
            episode_key=episode_key,
            mistakes_written=mistakes_written,
            mistake_agents=mistake_agents,
        )


def _episode_payload(event: MarketEvent, alert: Alert, run: LocalAgentRun, run_id: str) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "ticker": event.tickers[0] if event.tickers else None,
        "event_id": event.event_id,
        "event_type": event.event_type,
        "headline": event.headline,
        "decision": run.apex.decision,
        "confidence": run.apex.confidence,
        "alert_level": alert.alert_level,
        "alert_score": alert.alert_score,
        "news_sentiment": run.nysa.sentiment_score,
        "catalyst_tags": run.nysa.catalyst_tags,
        "agent_agreement_score": run.apex.agent_agreement_score,
        "critic_flags": run.vera.unchecked_risks,
        "thesis_summary": run.apex.final_thesis[:700],
        "source_url": event.source_url or event.document_url,
    }


def _mistake_payloads(
    event: MarketEvent,
    alert: Alert,
    run: LocalAgentRun,
    run_id: str,
) -> list[tuple[str, dict[str, Any]]]:
    payloads: list[tuple[str, dict[str, Any]]] = []
    base = {
        "run_id": run_id,
        "ticker": event.tickers[0] if event.tickers else None,
        "event_id": event.event_id,
        "event_type": event.event_type,
        "headline": event.headline,
        "alert_score": alert.alert_score,
        "created_at": datetime.now(UTC).isoformat(),
    }

    if run.vera.veto:
        payloads.append(
            (
                "VERA",
                {
                    **base,
                    "error_type": "VETOED_RISK",
                    "description": run.vera.veto_reason or "VERA vetoed this setup.",
                    "lesson": "Do not advance this setup without resolving the cited risk first.",
                },
            )
        )

    if run.apex.decision == "SKIP":
        payloads.append(
            (
                "APEX",
                {
                    **base,
                    "error_type": "SKIPPED_SETUP",
                    "description": run.apex.final_thesis,
                    "lesson": "Require cited evidence, sufficient alert score, and VERA clearance before paper trade.",
                },
            )
        )

    return payloads
