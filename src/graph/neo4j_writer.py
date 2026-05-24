"""Neo4j writer for confirmed market events and local decisions."""

from __future__ import annotations

import logging
import os
from datetime import date
from typing import Any, Protocol

from agents.local_loop import LocalAgentRun
from events.models import Alert, MarketEvent

logger = logging.getLogger(__name__)

try:
    from neo4j import GraphDatabase
except ImportError:  # pragma: no cover - depends on local env
    GraphDatabase = None


class Neo4jSession(Protocol):
    def run(self, query: str, **parameters: Any) -> Any:
        ...


class Neo4jDriver(Protocol):
    def session(self) -> Any:
        ...

    def close(self) -> None:
        ...


class KnowledgeGraphWriter:
    """Writes compact event/decision facts to Neo4j Community Edition."""

    def __init__(self, driver: Neo4jDriver | None = None):
        self.driver = driver or _build_driver()

    def close(self) -> None:
        if self.driver:
            self.driver.close()

    def write_event_decision(self, event: MarketEvent, alert: Alert, run: LocalAgentRun) -> bool:
        if not self.driver:
            return False
        ticker = event.tickers[0] if event.tickers else None
        if not ticker:
            logger.info("Skipping graph write for event without ticker: %s", event.event_id)
            return False

        params = {
            "symbol": ticker,
            "sector": event.sector,
            "event_id": event.event_id,
            "event_type": event.event_type,
            "headline": event.headline,
            "source": event.source,
            "source_url": event.source_url or event.document_url,
            "published_at": event.published_at.isoformat(),
            "severity": float(event.severity),
            "sentiment": float(event.sentiment),
            "alert_id": alert.alert_id,
            "alert_level": alert.alert_level,
            "alert_score": float(alert.alert_score),
            "decision": run.apex.decision,
            "confidence": float(run.apex.confidence),
            "veto": run.vera.veto,
            "veto_reason": run.vera.veto_reason,
            "run_date": date.today().isoformat(),
        }
        try:
            with self.driver.session() as session:
                session.run(_event_decision_cypher(), **params)
            return True
        except Exception as exc:
            logger.error("Neo4j graph write failed: %s", exc)
            return False


def _build_driver() -> Neo4jDriver | None:
    if GraphDatabase is None:
        return None
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "hivemind")
    try:
        return GraphDatabase.driver(uri, auth=(user, password))
    except Exception as exc:  # pragma: no cover - requires local service
        logger.warning("Neo4j unavailable: %s", exc)
        return None


def _event_decision_cypher() -> str:
    return """
        MERGE (s:Stock {symbol: $symbol})
        SET s.sector = coalesce($sector, s.sector)
        MERGE (c:Catalyst {event_id: $event_id})
        SET c.type = $event_type,
            c.headline = $headline,
            c.source = $source,
            c.source_url = $source_url,
            c.published_at = $published_at,
            c.severity = $severity,
            c.sentiment = $sentiment
        MERGE (c)-[:TRIGGERED]->(s)
        MERGE (a:Alert {alert_id: $alert_id})
        SET a.level = $alert_level,
            a.score = $alert_score
        MERGE (c)-[:RAISED]->(a)
        MERGE (td:TradeDecision {event_id: $event_id, run_date: $run_date})
        SET td.decision = $decision,
            td.confidence = $confidence,
            td.veto = $veto,
            td.veto_reason = $veto_reason
        MERGE (c)-[:PRECEDED]->(td)
        MERGE (apex:Agent {name: 'APEX'})
        MERGE (td)-[:MADE_BY]->(apex)
    """
