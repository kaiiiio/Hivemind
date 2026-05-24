"""Deterministic free/local agent loop for event triage.

This is not a replacement for the full PDF swarm. It is the first executable
loop that enforces the core rule: no cited evidence, no trade recommendation.
"""

from __future__ import annotations

from dataclasses import dataclass

from events.models import Alert, MarketEvent

from .schemas import ApexOutput, NysaOutput, SentinelOutput, VeraOutput


NEGATIVE_CATALYSTS = {
    "AUDITOR_RESIGNATION",
    "USFDA_ALERT",
    "PLEDGE",
    "PROMOTER_SELL",
    "CREDIT_RATING_DOWNGRADE",
    "MANAGEMENT_CHANGE",
    "REGULATORY_ACTION",
}


@dataclass(slots=True)
class LocalAgentRun:
    sentinel: SentinelOutput
    nysa: NysaOutput
    vera: VeraOutput
    apex: ApexOutput


def run_local_event_loop(
    event: MarketEvent,
    alert: Alert,
    evidence: list[str] | None = None,
    current_price: float | None = None,
) -> LocalAgentRun:
    """Run SENTINEL -> NYSA -> VERA -> APEX without external model calls."""

    evidence = evidence or _event_evidence(event)
    sentinel = run_sentinel(alert)
    nysa = run_nysa(event, evidence)
    vera = run_vera(event, alert, nysa, evidence)
    apex = run_apex(event, alert, nysa, vera, evidence, current_price=current_price)
    return LocalAgentRun(sentinel=sentinel, nysa=nysa, vera=vera, apex=apex)


def run_sentinel(alert: Alert) -> SentinelOutput:
    attention_required = alert.alert_score >= 0.45
    return SentinelOutput(
        attention_required=attention_required,
        alert_level=alert.alert_level,
        priority_score=alert.alert_score,
        reason=alert.reason,
    )


def run_nysa(event: MarketEvent, evidence: list[str]) -> NysaOutput:
    is_negative = event.event_type in NEGATIVE_CATALYSTS or event.sentiment < -0.25
    return NysaOutput(
        sentiment_score=event.sentiment,
        catalyst_tags=[event.event_type],
        red_flag=is_negative,
        red_flag_severity=event.severity if is_negative else 0.0,
        news_summary=_summarize_event(event),
        retrieved_similar_events=evidence[:5],
    )


def run_vera(event: MarketEvent, alert: Alert, nysa: NysaOutput, evidence: list[str]) -> VeraOutput:
    unchecked_risks = []
    if not evidence:
        unchecked_risks.append("No cited evidence attached to the event.")
    if not event.tickers:
        unchecked_risks.append("Ticker could not be resolved.")
    if event.requires_confirmation and alert.alert_score >= 0.65:
        unchecked_risks.append("Non-official source requires confirmation before action.")
    if nysa.red_flag and nysa.red_flag_severity >= 0.75:
        unchecked_risks.append("High-severity negative catalyst needs risk review.")

    veto = bool(unchecked_risks)
    return VeraOutput(
        veto=veto,
        veto_reason="; ".join(unchecked_risks) if veto else None,
        risk_score=min(1.0, event.severity + (0.15 if nysa.red_flag else 0.0)),
        unchecked_risks=unchecked_risks,
        confidence_adjustment=-0.2 if veto else 0.0,
        verification_report=_verification_report(event, unchecked_risks),
    )


def run_apex(
    event: MarketEvent,
    alert: Alert,
    nysa: NysaOutput,
    vera: VeraOutput,
    evidence: list[str],
    current_price: float | None = None,
) -> ApexOutput:
    can_trade = bool(evidence) and not vera.veto and current_price is not None and alert.alert_score >= 0.75
    if not can_trade:
        return ApexOutput(
            decision="SKIP",
            confidence=max(0.05, alert.alert_score + vera.confidence_adjustment),
            final_thesis=_skip_thesis(event, alert, vera),
            agent_agreement_score=_agreement_score(nysa, vera),
            dissenting_agent="VERA" if vera.veto else None,
        )

    stop_price = round(current_price * 0.95, 2)
    target_price = round(current_price * 1.10, 2)
    return ApexOutput(
        decision="PROCEED",
        entry_price=round(current_price, 2),
        stop_price=stop_price,
        target_price=target_price,
        timeframe="event-driven watchlist",
        confidence=min(0.9, alert.alert_score),
        final_thesis=(
            f"{event.tickers[0]} has cited event evidence from {event.source}: {event.headline}. "
            "Risk/reward passes the local 2:1 template, but execution remains paper-only."
        ),
        agent_agreement_score=_agreement_score(nysa, vera),
    )


def _event_evidence(event: MarketEvent) -> list[str]:
    if event.source_url:
        return [event.source_url]
    if event.document_url:
        return [event.document_url]
    return [event.event_id] if event.event_id else []


def _summarize_event(event: MarketEvent) -> str:
    ticker_text = ", ".join(event.tickers) if event.tickers else "unresolved ticker"
    return f"{ticker_text}: {event.event_type} from {event.source}. {event.headline}"


def _verification_report(event: MarketEvent, unchecked_risks: list[str]) -> str:
    if unchecked_risks:
        return f"VERA blocks action on {event.event_type}: " + " ".join(unchecked_risks)
    return f"VERA found no blocking issue for cited {event.event_type} evidence."


def _skip_thesis(event: MarketEvent, alert: Alert, vera: VeraOutput) -> str:
    if vera.veto:
        return f"Skip {event.event_type}: {vera.veto_reason}"
    return f"Skip {event.event_type}: alert score {alert.alert_score:.2f} is not enough for a paper trade."


def _agreement_score(nysa: NysaOutput, vera: VeraOutput) -> float:
    if nysa.red_flag and vera.veto:
        return 0.85
    if not nysa.red_flag and not vera.veto:
        return 0.75
    return 0.45
