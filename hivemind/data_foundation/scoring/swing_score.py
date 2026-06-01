from __future__ import annotations

from hivemind.data_foundation.models import Alert, ParsedEvent


def score_event(event: ParsedEvent) -> Alert:
    score = 30
    reasons: list[str] = []

    if event.event_type in {"order_win", "tender_win"}:
        score += 20
        reasons.append("material corporate order event")

    if event.event_amount_inr_cr:
        if event.event_amount_inr_cr >= 500:
            score += 25
            reasons.append("large disclosed order value")
        elif event.event_amount_inr_cr >= 100:
            score += 15
            reasons.append("meaningful disclosed order value")

    if event.tailwind_tags:
        score += 10
        reasons.append("matches tracked macro or policy tailwind")

    if event.sector_tags:
        score += 5
        reasons.append("sector exposure identified")

    score = min(score, 100)
    return Alert(event=event, swing_score=score, reason=", ".join(reasons))

