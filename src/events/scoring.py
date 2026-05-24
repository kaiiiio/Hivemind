"""Alert scoring for market events."""

from __future__ import annotations

from .models import Alert, MarketEvent


SOURCE_TRUST = {
    "EXCHANGE": 1.0,
    "REGULATOR": 1.0,
    "COMPANY": 0.8,
    "NEWS": 0.55,
    "SOCIAL": 0.25,
}


def score_event(
    event: MarketEvent,
    ticker_relevance: float = 1.0,
    price_volume_confirmation: float = 0.0,
    novelty_score: float = 0.5,
    agent_interest_score: float = 0.0,
) -> float:
    source_trust_score = SOURCE_TRUST.get(event.source_type, 0.4)
    score = (
        source_trust_score * 0.30
        + event.severity * 0.25
        + ticker_relevance * 0.15
        + price_volume_confirmation * 0.15
        + novelty_score * 0.10
        + agent_interest_score * 0.05
    )
    return round(max(0.0, min(1.0, score)), 4)


def alert_from_event(event: MarketEvent, alert_score: float) -> Alert:
    if alert_score >= 0.8:
        level = "HIGH_ALERT"
    elif alert_score >= 0.65:
        level = "INVESTIGATE"
    elif alert_score >= 0.45:
        level = "WATCH"
    else:
        level = "INFO"

    ticker = event.tickers[0] if event.tickers else None
    return Alert(
        alert_id=f"alert:{event.event_id}",
        event_id=event.event_id,
        ticker=ticker,
        alert_level=level,
        alert_score=alert_score,
        reason=f"{event.source_type} {event.event_type}: {event.headline}",
    )
