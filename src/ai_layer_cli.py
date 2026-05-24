"""Command-line utilities for the free/local AI layer."""

from __future__ import annotations

import argparse
import sys
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
from agents.local_loop import run_local_event_loop


@dataclass(slots=True)
class AlertRow:
    alert_id: str
    ticker: str | None
    alert_level: str
    alert_score: float
    reason: str
    status: str
    created_at: str


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="HIVEMIND free/local AI layer utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    ingest = subparsers.add_parser("ingest-rss", help="Fetch RSS feeds, score events, and optionally persist alerts")
    ingest.add_argument("--source", action="append", required=True, help="RSS source as NAME=URL. Can be repeated.")
    ingest.add_argument("--source-type", default="NEWS", choices=["EXCHANGE", "REGULATOR", "NEWS", "COMPANY", "SOCIAL"])
    ingest.add_argument("--ticker", action="append", default=[], help="Known ticker symbol for exact matching. Can be repeated.")
    ingest.add_argument("--sector", default=None, help="Optional sector tag applied to all events from this run.")
    ingest.add_argument("--dry-run", action="store_true", help="Print scored events without writing to Postgres.")

    alerts = subparsers.add_parser("alerts", help="List recent alerts from local Postgres")
    alerts.add_argument("--limit", type=int, default=20)
    alerts.add_argument("--status", default="OPEN", choices=["OPEN", "ACKNOWLEDGED", "CLOSED", "ALL"])

    triage = subparsers.add_parser("triage-rss", help="Run deterministic SENTINEL/NYSA/VERA/APEX triage on RSS events")
    triage.add_argument("--source", action="append", required=True, help="RSS source as NAME=URL. Can be repeated.")
    triage.add_argument("--source-type", default="NEWS", choices=["EXCHANGE", "REGULATOR", "NEWS", "COMPANY", "SOCIAL"])
    triage.add_argument("--ticker", action="append", default=[], help="Known ticker symbol for exact matching. Can be repeated.")
    triage.add_argument("--sector", default=None)
    triage.add_argument("--current-price", type=float, default=None, help="Optional current price for paper-only APEX R:R template.")

    args = parser.parse_args(argv)
    if args.command == "ingest-rss":
        return ingest_rss(args)
    if args.command == "alerts":
        return list_alerts(args)
    if args.command == "triage-rss":
        return triage_rss(args)
    return 2


def ingest_rss(args: argparse.Namespace) -> int:
    sources = [_parse_source(raw, args.source_type, args.sector, args.ticker) for raw in args.source]
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


def triage_rss(args: argparse.Namespace) -> int:
    sources = [_parse_source(raw, args.source_type, args.sector, args.ticker) for raw in args.source]
    events = RSSConnector(sources).fetch_events()
    print(f"Fetched {len(events)} events")
    for event in events:
        alert = alert_from_event(event, score_event(event))
        run = run_local_event_loop(event, alert, current_price=args.current_price)
        ticker = ",".join(event.tickers) if event.tickers else "-"
        print(
            f"{ticker:<12} | {alert.alert_level:<12} | APEX={run.apex.decision:<7} | "
            f"VERA_VETO={str(run.vera.veto):<5} | {event.headline}"
        )
        if run.vera.veto_reason:
            print(f"  VERA: {run.vera.veto_reason}")
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


def _format_alert_line(level: str, score: float, tickers: list[str], headline: str) -> str:
    ticker_text = ",".join(tickers) if tickers else "-"
    return f"{level:<12} {score:.2f} {ticker_text:<12} {headline}"


if __name__ == "__main__":
    raise SystemExit(main())
