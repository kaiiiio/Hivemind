"""Rule-based market event classifier.

This is intentionally cheap and deterministic. LLM classification can be added
after we have source coverage and labeled examples.
"""

from __future__ import annotations


EVENT_KEYWORDS = {
    "AUDITOR_RESIGNATION": ("auditor resign", "resignation of auditor"),
    "ORDER_WIN": ("order win", "letter of award", "contract awarded"),
    "USFDA_ALERT": ("usfda", "import alert", "warning letter"),
    "PLEDGE": ("pledge", "encumbrance"),
    "PROMOTER_SELL": ("promoter sell", "disposal of shares"),
    "PROMOTER_BUY": ("promoter buy", "acquisition of shares"),
    "CREDIT_RATING_DOWNGRADE": ("downgrade", "rating revised downward"),
    "CREDIT_RATING_UPGRADE": ("upgrade", "rating revised upward"),
    "MANAGEMENT_CHANGE": ("resignation of director", "appointment of director", "ceo resign"),
    "RESULTS": ("financial results", "quarter ended", "audited results"),
    "GUIDANCE_CHANGE": ("guidance", "outlook revised"),
    "BUYBACK": ("buyback", "share repurchase"),
    "DIVIDEND": ("dividend",),
    "SPLIT_BONUS": ("stock split", "bonus issue"),
    "REGULATORY_ACTION": ("sebi order", "penalty", "show cause"),
}

NEGATIVE_TYPES = {
    "AUDITOR_RESIGNATION",
    "USFDA_ALERT",
    "PLEDGE",
    "PROMOTER_SELL",
    "CREDIT_RATING_DOWNGRADE",
    "MANAGEMENT_CHANGE",
    "REGULATORY_ACTION",
}


def classify_event(headline: str, body: str = "") -> tuple[str, float, float]:
    text = f"{headline} {body}".lower()
    for event_type, keywords in EVENT_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            severity = 0.85 if event_type in NEGATIVE_TYPES else 0.65
            sentiment = -0.7 if event_type in NEGATIVE_TYPES else 0.4
            return event_type, severity, sentiment
    return "GENERAL_NEWS", 0.25, 0.0
