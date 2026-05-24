"""Event ingestion pipeline wiring connectors, scoring, and persistence."""

from __future__ import annotations

from dataclasses import dataclass

from .models import Alert, MarketEvent
from .repository import EventRepository
from .rss_connector import RSSConnector
from .scoring import alert_from_event, score_event


@dataclass(slots=True)
class EventIngestionResult:
    fetched: int = 0
    persisted: int = 0
    alerts: list[Alert] | None = None


class EventIngestionPipeline:
    """Fetch events, score alerts, and persist both records."""

    def __init__(self, connector: RSSConnector, repository: EventRepository):
        self.connector = connector
        self.repository = repository

    def run(self) -> EventIngestionResult:
        events = self.connector.fetch_events()
        alerts = [self.build_alert(event) for event in events]
        persisted = 0
        for event, alert in zip(events, alerts):
            if self.repository.upsert_event_and_alert(event, alert):
                persisted += 1
        return EventIngestionResult(fetched=len(events), persisted=persisted, alerts=alerts)

    @staticmethod
    def build_alert(event: MarketEvent) -> Alert:
        return alert_from_event(event, score_event(event))
