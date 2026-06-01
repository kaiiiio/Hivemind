from __future__ import annotations

import re

from hivemind.data_foundation.models import ParsedEvent, RawEvidenceRecord


ORDER_WORDS = ("order", "project", "contract", "work order", "letter of award")


def parse_event(record: RawEvidenceRecord) -> ParsedEvent | None:
    text = f"{record.title}\n{record.raw_text}"
    lowered = text.lower()

    if any(word in lowered for word in ORDER_WORDS):
        return ParsedEvent(
            raw_evidence_id=record.id,
            event_type="order_win",
            company_name=extract_company_name(text),
            summary=record.title,
            event_amount_inr_cr=extract_amount_inr_cr(text),
            sector_tags=infer_sector_tags(text),
            tailwind_tags=infer_tailwind_tags(text),
            confidence=0.72,
            extraction_method="rules",
        )

    return None


def extract_amount_inr_cr(text: str) -> float | None:
    match = re.search(
        r"(?:rs\.?|inr|₹)?\s*([0-9]+(?:\.[0-9]+)?)\s*(?:crore|cr)\b",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return None
    return float(match.group(1))


def extract_company_name(text: str) -> str | None:
    first_sentence = re.split(r"[.\n]", text.strip(), maxsplit=1)[0]
    if " wins " in first_sentence.lower():
        return re.split(r"\bwins\b", first_sentence, flags=re.IGNORECASE)[0].strip()
    return None


def infer_sector_tags(text: str) -> list[str]:
    lowered = text.lower()
    tags: list[str] = []
    if any(word in lowered for word in ("digital", "cloud", "data center", "it")):
        tags.append("it_infrastructure")
    if any(word in lowered for word in ("railway", "metro", "signalling")):
        tags.append("railways")
    if any(word in lowered for word in ("defence", "aerospace", "drone")):
        tags.append("defence")
    return tags


def infer_tailwind_tags(text: str) -> list[str]:
    lowered = text.lower()
    tags: list[str] = []
    if any(word in lowered for word in ("digital", "infrastructure", "cloud")):
        tags.append("digital_infrastructure")
    if any(word in lowered for word in ("government", "psu", "ministry")):
        tags.append("government_capex")
    return tags

