"""Command-line utilities for the free/local AI layer."""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from data_ingestion.database_upsert import DatabaseManager
from events.pipeline import EventIngestionPipeline
from events.repository import EventRepository
from events.rss_connector import RSSConnector, RSSSource
from events.scoring import alert_from_event, score_event
from events.source_config import load_rss_sources
from agents.local_loop import run_local_event_loop
from agents.repository import AgentOutputRepository
from graph.neo4j_writer import KnowledgeGraphWriter
from memory.feedback import FeedbackMemoryWriter
from memory.redis_store import RedisEpisodicStore


@dataclass(slots=True)
class AlertRow:
    alert_id: str
    ticker: str | None
    alert_level: str
    alert_score: float
    reason: str
    status: str
    created_at: str


@dataclass(slots=True)
class AgentOutputRow:
    created_at: str
    agent_name: str
    ticker: str | None
    output_type: str
    confidence_score: float | None
    model_used: str | None
    output_data: str


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="HIVEMIND free/local AI layer utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest-rss", help="Fetch RSS feeds, score events, and optionally persist alerts")
    ingest.add_argument("--source", action="append", help="RSS source as NAME=URL. Can be repeated.")
    ingest.add_argument("--source-config", help="Local JSON file with RSS sources, tickers, and company aliases.")
    ingest.add_argument("--source-type", default="NEWS", choices=["EXCHANGE", "REGULATOR", "NEWS", "COMPANY", "SOCIAL"])
    ingest.add_argument("--ticker", action="append", default=[], help="Known ticker symbol for exact matching. Can be repeated.")
    ingest.add_argument("--sector", default=None, help="Optional sector tag applied to all events from this run.")
    ingest.add_argument("--dry-run", action="store_true", help="Print scored events without writing to Postgres.")

    alerts = subparsers.add_parser("alerts", help="List recent alerts from local Postgres")
    alerts.add_argument("--limit", type=int, default=20)
    alerts.add_argument("--status", default="OPEN", choices=["OPEN", "ACKNOWLEDGED", "CLOSED", "ALL"])

    outputs = subparsers.add_parser("agent-outputs", help="List recent persisted agent outputs from local Postgres")
    outputs.add_argument("--limit", type=int, default=20)
    outputs.add_argument("--agent", default=None, help="Optional agent filter, e.g. APEX or VERA.")
    outputs.add_argument("--ticker", default=None, help="Optional ticker filter.")

    mistakes = subparsers.add_parser("mistakes", help="List recent Redis/fallback mistake memory for an agent")
    mistakes.add_argument("--agent", required=True, help="Agent name, e.g. APEX or VERA.")
    mistakes.add_argument("--limit", type=int, default=5)

    triage = subparsers.add_parser("triage-rss", help="Run deterministic SENTINEL/NYSA/VERA/APEX triage on RSS events")
    triage.add_argument("--source", action="append", help="RSS source as NAME=URL. Can be repeated.")
    triage.add_argument("--source-config", help="Local JSON file with RSS sources, tickers, and company aliases.")
    triage.add_argument("--source-type", default="NEWS", choices=["EXCHANGE", "REGULATOR", "NEWS", "COMPANY", "SOCIAL"])
    triage.add_argument("--ticker", action="append", default=[], help="Known ticker symbol for exact matching. Can be repeated.")
    triage.add_argument("--sector", default=None)
    triage.add_argument("--current-price", type=float, default=None, help="Optional current price for paper-only APEX R:R template.")
    triage.add_argument("--persist", action="store_true", help="Persist events, alerts, and agent outputs to local Postgres.")
    triage.add_argument("--remember", action="store_true", help="Write compact episode and mistake memory to Redis when available.")
    triage.add_argument("--graph", action="store_true", help="Write event and decision facts to local Neo4j when available.")

    args = parser.parse_args(argv)
    if args.command == "ingest-rss":
        return ingest_rss(args)
    if args.command == "alerts":
        return list_alerts(args)
    if args.command == "agent-outputs":
        return list_agent_outputs(args)
    if args.command == "mistakes":
        return list_mistakes(args)
    if args.command == "triage-rss":
        return triage_rss(args)
    return 2


def ingest_rss(args: argparse.Namespace) -> int:
    sources = _sources_from_args(args)
    connector = RSSConnector(sources)

    if args.dry_run:
        events = connector.fetch_events()
        print(f"Fetched {len(events)} events")
        for event in events:
            alert = alert_from_event(event, score_event(event))
            print(_format_alert_line(alert.alert_level, alert.alert_score, event.tickers, event.headline))
        return 0

    db = DatabaseManager()
    if not db.connect():
        print("Database connection failed. Start Docker or use --dry-run.", file=sys.stderr)
        return 1
    try:
        result = EventIngestionPipeline(connector, EventRepository(db.connection)).run()
        print(f"Fetched {result.fetched} events, persisted {result.persisted} event/alert pairs")
        return 0
    finally:
        db.disconnect()


def list_alerts(args: argparse.Namespace) -> int:
    db = DatabaseManager()
    if not db.connect():
        print("Database connection failed. Start Docker before listing alerts.", file=sys.stderr)
        return 1

    try:
        rows = _fetch_alerts(db.connection, args.limit, None if args.status == "ALL" else args.status)
    finally:
        db.disconnect()

    if not rows:
        print("No alerts found.")
        return 0

    for row in rows:
        ticker = row.ticker or "-"
        print(f"{row.created_at} | {row.alert_level:<12} | {row.alert_score:.2f} | {ticker:<10} | {row.reason}")
    return 0


def list_agent_outputs(args: argparse.Namespace) -> int:
    db = DatabaseManager()
    if not db.connect():
        print("Database connection failed. Start Docker before listing agent outputs.", file=sys.stderr)
        return 1

    try:
        rows = _fetch_agent_outputs(db.connection, args.limit, args.agent, args.ticker)
    finally:
        db.disconnect()

    if not rows:
        print("No agent outputs found.")
        return 0

    for row in rows:
        ticker = row.ticker or "-"
        confidence = "-" if row.confidence_score is None else f"{row.confidence_score:.2f}"
        summary = row.output_data.replace("\n", " ")[:180]
        print(
            f"{row.created_at} | {row.agent_name:<8} | {ticker:<10} | "
            f"{confidence:<5} | {row.output_type:<12} | {summary}"
        )
    return 0


def list_mistakes(args: argparse.Namespace) -> int:
    store = RedisEpisodicStore()
    mistakes = store.read_mistakes(args.agent.upper(), limit=args.limit)
    if not mistakes:
        print(f"No mistake memory found for {args.agent.upper()}.")
        return 0
    for item in mistakes:
        ticker = item.get("ticker") or "-"
        error_type = item.get("error_type", "UNKNOWN")
        description = item.get("description", "")
        print(f"{args.agent.upper():<8} | {ticker:<10} | {error_type:<16} | {description}")
    return 0


def triage_rss(args: argparse.Namespace) -> int:
    sources = _sources_from_args(args)
    events = RSSConnector(sources).fetch_events()
    print(f"Fetched {len(events)} events")
    db = None
    event_repository = None
    output_repository = None
    memory_writer = FeedbackMemoryWriter() if args.remember else None
    graph_writer = KnowledgeGraphWriter() if args.graph else None
    if args.persist:
        db = DatabaseManager()
        if not db.connect():
            print("Database connection failed. Start Docker or omit --persist.", file=sys.stderr)
            return 1
        event_repository = EventRepository(db.connection)
        output_repository = AgentOutputRepository(db.connection)

    persisted_pairs = 0
    persisted_outputs = 0
    memory_episodes = 0
    memory_mistakes = 0
    graph_writes = 0
    for event in events:
        alert = alert_from_event(event, score_event(event))
        started_at = time.perf_counter()
        run = run_local_event_loop(event, alert, current_price=args.current_price)
        if event_repository and event_repository.upsert_event_and_alert(event, alert):
            persisted_pairs += 1
        if output_repository:
            persisted_outputs += output_repository.insert_local_agent_run(
                run,
                ticker=event.tickers[0] if event.tickers else None,
                started_at=started_at,
            )
        if memory_writer:
            feedback = memory_writer.write_event_triage(event, alert, run)
            if feedback.episode_key:
                memory_episodes += 1
            memory_mistakes += feedback.mistakes_written
        if graph_writer and graph_writer.write_event_decision(event, alert, run):
            graph_writes += 1
        ticker = ",".join(event.tickers) if event.tickers else "-"
        print(
            f"{ticker:<12} | {alert.alert_level:<12} | APEX={run.apex.decision:<7} | "
            f"VERA_VETO={str(run.vera.veto):<5} | {event.headline}"
        )
        if run.vera.veto_reason:
            print(f"  VERA: {run.vera.veto_reason}")
    if db:
        db.disconnect()
        print(f"Persisted {persisted_pairs} event/alert pairs and {persisted_outputs} agent outputs")
    if memory_writer:
        print(f"Wrote {memory_episodes} memory episodes and {memory_mistakes} mistake records")
    if graph_writer:
        graph_writer.close()
        print(f"Wrote {graph_writes} graph event/decision records")
    return 0


def _fetch_alerts(connection, limit: int, status: str | None) -> list[AlertRow]:
    sql = """
        SELECT alert_id, ticker, alert_level, alert_score, reason, status, created_at::text
        FROM alerts
        WHERE (%s IS NULL OR status = %s)
        ORDER BY alert_score DESC, created_at DESC
        LIMIT %s
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, (status, status, limit))
        return [AlertRow(*row) for row in cursor.fetchall()]


def _fetch_agent_outputs(
    connection,
    limit: int,
    agent_name: str | None = None,
    ticker: str | None = None,
) -> list[AgentOutputRow]:
    sql = """
        SELECT created_at::text, agent_name, ticker, output_type, confidence_score, model_used, output_data::text
        FROM agent_outputs
        WHERE (%s IS NULL OR agent_name = upper(%s))
          AND (%s IS NULL OR ticker = upper(%s))
        ORDER BY created_at DESC
        LIMIT %s
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, (agent_name, agent_name, ticker, ticker, limit))
        return [AgentOutputRow(*row) for row in cursor.fetchall()]


def _parse_source(raw: str, source_type: str, sector: str | None, tickers: list[str]) -> RSSSource:
    if "=" not in raw:
        raise SystemExit("--source must be in NAME=URL format")
    name, url = raw.split("=", 1)
    if not name.strip() or not url.strip():
        raise SystemExit("--source must include both NAME and URL")
    return RSSSource(
        name=name.strip(),
        url=url.strip(),
        source_type=source_type,
        default_sector=sector,
        tickers=[ticker.upper() for ticker in tickers],
    )


def _sources_from_args(args: argparse.Namespace) -> list[RSSSource]:
    sources: list[RSSSource] = []
    if getattr(args, "source_config", None):
        sources.extend(load_rss_sources(args.source_config))
    for raw in getattr(args, "source", None) or []:
        sources.append(_parse_source(raw, args.source_type, args.sector, args.ticker))
    if not sources:
        raise SystemExit("Provide --source NAME=URL or --source-config path.json")
    return sources


def _format_alert_line(level: str, score: float, tickers: list[str], headline: str) -> str:
    ticker_text = ",".join(tickers) if tickers else "-"
    return f"{level:<12} {score:.2f} {ticker_text:<12} {headline}"


if __name__ == "__main__":
    raise SystemExit(main())
