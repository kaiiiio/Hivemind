"""Zero-cost query expansion.

LLM query rewriting can be added later, but this rule-based path keeps the
retrieval layer useful without spending API calls.
"""

from __future__ import annotations


FINANCIAL_SYNONYMS = {
    "delivery spike": ["delivery ratio surge", "institutional accumulation", "volume delivery breakout"],
    "earnings beat": ["profit exceeds estimate", "results beat", "margin expansion"],
    "red flag": ["governance concern", "pledge risk", "auditor resignation"],
    "momentum": ["relative strength", "price breakout", "trend continuation"],
    "risk off": ["vix spike", "fii outflow", "market stress"],
}


class QueryRewriter:
    def rewrite(self, query: str, ticker: str | None = None, sector: str | None = None, limit: int = 4) -> list[str]:
        base = " ".join(part for part in [ticker, sector, query] if part)
        variants = [base.strip()]
        lowered = query.lower()
        for term, synonyms in FINANCIAL_SYNONYMS.items():
            if term in lowered:
                variants.extend(f"{ticker or ''} {sector or ''} {synonym}".strip() for synonym in synonyms)
        if len(variants) == 1:
            variants.extend(
                [
                    f"{ticker or ''} {sector or ''} catalyst historical outcome".strip(),
                    f"{ticker or ''} {sector or ''} similar setup trade thesis".strip(),
                    f"{ticker or ''} {sector or ''} risk flags".strip(),
                ]
            )
        return list(dict.fromkeys(variants))[:limit]
