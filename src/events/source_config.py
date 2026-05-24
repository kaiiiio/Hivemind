"""Load RSS source configuration from JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .rss_connector import RSSSource


def load_rss_sources(path: str | Path) -> list[RSSSource]:
    """Load source definitions from a local JSON file."""

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    source_rows = data.get("sources", data if isinstance(data, list) else [])
    if not isinstance(source_rows, list):
        raise ValueError("source config must contain a list or a top-level 'sources' list")
    return [_source_from_row(row) for row in source_rows]


def _source_from_row(row: dict[str, Any]) -> RSSSource:
    if not row.get("name") or not row.get("url"):
        raise ValueError("each source config row requires 'name' and 'url'")
    return RSSSource(
        name=str(row["name"]),
        url=str(row["url"]),
        source_type=row.get("source_type", "NEWS"),
        default_sector=row.get("sector"),
        tickers=[str(ticker).upper() for ticker in row.get("tickers", [])],
        company_aliases=_normalize_company_aliases(row.get("company_aliases", {})),
    )


def _normalize_company_aliases(raw: dict[str, Any]) -> dict[str, list[str]]:
    aliases: dict[str, list[str]] = {}
    for ticker, values in raw.items():
        if isinstance(values, str):
            aliases[str(ticker).upper()] = [values]
        else:
            aliases[str(ticker).upper()] = [str(value) for value in values]
    return aliases
