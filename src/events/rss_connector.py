"""Generic RSS connector for zero-cost market event ingestion."""

from __future__ import annotations

import hashlib
import logging
import re
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Iterable
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree

from .classifier import classify_event
from .models import MarketEvent, SourceType

logger = logging.getLogger(__name__)

try:
    import feedparser
except ImportError:  # pragma: no cover - depends on local env
    feedparser = None

try:
    import requests
except ImportError:  # pragma: no cover - depends on local env
    requests = None


@dataclass(slots=True)
class RSSSource:
    name: str
    url: str
    source_type: SourceType = "NEWS"
    default_sector: str | None = None
    tickers: list[str] = field(default_factory=list)


class RSSConnector:
    """Fetch RSS feeds and normalize entries into MarketEvent objects."""

    def __init__(self, sources: Iterable[RSSSource], timeout_seconds: int = 15):
        self.sources = list(sources)
        self.timeout_seconds = timeout_seconds

    def fetch_events(self) -> list[MarketEvent]:
        events: list[MarketEvent] = []
        for source in self.sources:
            events.extend(self.fetch_source(source))
        return events

    def fetch_source(self, source: RSSSource) -> list[MarketEvent]:
        raw_feed = self._download(source.url)
        entries = _parse_entries(raw_feed or "", source.url)
        events = []
        for entry in entries:
            headline = _clean_text(entry.get("title", ""))
            summary = _clean_text(entry.get("summary", entry.get("description", "")))
            link = entry.get("link")
            if not headline:
                continue
            event_type, severity, sentiment = classify_event(headline, summary)
            tickers = _resolve_tickers(f"{headline} {summary}", source.tickers)
            dedupe_hash = _dedupe_hash(source.name, headline, link)
            events.append(
                MarketEvent(
                    event_id=f"rss:{dedupe_hash[:24]}",
                    source=source.name,
                    source_type=source.source_type,
                    source_url=link,
                    published_at=_parse_published(entry),
                    tickers=tickers,
                    sector=source.default_sector,
                    event_type=event_type,
                    headline=headline,
                    summary=summary or None,
                    raw_text=summary or None,
                    document_url=link,
                    severity=severity,
                    sentiment=sentiment,
                    confidence=0.65 if event_type != "GENERAL_NEWS" else 0.45,
                    requires_confirmation=source.source_type not in {"EXCHANGE", "REGULATOR"},
                    dedupe_hash=dedupe_hash,
                )
            )
        return events

    def _download(self, url: str) -> str | None:
        parsed = urlparse(url)
        is_windows_path = len(parsed.scheme) == 1 and ":\\" in url
        if parsed.scheme in {"", "file"} or is_windows_path:
            path = Path(parsed.path if parsed.scheme == "file" else url)
            try:
                return path.read_text(encoding="utf-8")
            except OSError as exc:
                logger.warning("Local RSS file read failed for %s: %s", url, exc)
                return None

        if requests is None:
            return _download_with_stdlib(url, self.timeout_seconds)
        try:
            response = requests.get(url, timeout=self.timeout_seconds, headers={"User-Agent": "HIVEMIND/0.1"})
            response.raise_for_status()
            return response.text
        except Exception as exc:
            logger.warning("RSS download failed for %s: %s", url, exc)
            return None


def _parse_entries(raw_feed: str, source_url: str) -> list[dict[str, str]]:
    if feedparser is not None:
        parsed = feedparser.parse(raw_feed if raw_feed else source_url)
        return [dict(entry) for entry in parsed.entries]
    if not raw_feed:
        logger.warning("feedparser unavailable and no feed XML downloaded for %s", source_url)
        return []
    return _parse_entries_with_stdlib(raw_feed)


def _parse_entries_with_stdlib(raw_feed: str) -> list[dict[str, str]]:
    try:
        root = ElementTree.fromstring(raw_feed)
    except ElementTree.ParseError as exc:
        logger.warning("RSS XML parse failed: %s", exc)
        return []

    entries = []
    for item in root.findall(".//item"):
        entries.append(
            {
                "title": _xml_child_text(item, "title"),
                "summary": _xml_child_text(item, "description"),
                "description": _xml_child_text(item, "description"),
                "link": _xml_child_text(item, "link"),
                "published": _xml_child_text(item, "pubDate"),
            }
        )

    atom_ns = "{http://www.w3.org/2005/Atom}"
    for entry in root.findall(f".//{atom_ns}entry"):
        link = ""
        link_node = entry.find(f"{atom_ns}link")
        if link_node is not None:
            link = link_node.attrib.get("href", "")
        entries.append(
            {
                "title": _xml_child_text(entry, f"{atom_ns}title"),
                "summary": _xml_child_text(entry, f"{atom_ns}summary") or _xml_child_text(entry, f"{atom_ns}content"),
                "description": _xml_child_text(entry, f"{atom_ns}summary") or _xml_child_text(entry, f"{atom_ns}content"),
                "link": link,
                "published": _xml_child_text(entry, f"{atom_ns}published") or _xml_child_text(entry, f"{atom_ns}updated"),
            }
        )
    return entries


def _xml_child_text(node: ElementTree.Element, tag: str) -> str:
    child = node.find(tag)
    return "".join(child.itertext()).strip() if child is not None else ""


def _download_with_stdlib(url: str, timeout_seconds: int) -> str | None:
    try:
        request = Request(url, headers={"User-Agent": "HIVEMIND/0.1"})
        with urlopen(request, timeout=timeout_seconds) as response:
            return response.read().decode("utf-8", errors="replace")
    except Exception as exc:
        logger.warning("RSS download failed for %s: %s", url, exc)
        return None


def _parse_published(entry) -> datetime:
    for key in ("published", "updated", "created"):
        value = entry.get(key)
        if value:
            try:
                parsed = parsedate_to_datetime(value)
                return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
            except (TypeError, ValueError):
                pass
    return datetime.now(timezone.utc)


def _resolve_tickers(text: str, known_tickers: Iterable[str]) -> list[str]:
    found = []
    for ticker in known_tickers:
        if re.search(rf"\b{re.escape(ticker)}\b", text, flags=re.IGNORECASE):
            found.append(ticker.upper())
    return list(dict.fromkeys(found))


def _dedupe_hash(source: str, headline: str, link: str | None) -> str:
    identity = f"{source}|{headline}|{link or ''}".lower().encode("utf-8")
    return hashlib.sha256(identity).hexdigest()


def _clean_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", text).strip()
