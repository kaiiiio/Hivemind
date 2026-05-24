import asyncio

from agents.local_loop import run_local_event_loop
from agents.schemas import NysaOutput
from events.classifier import classify_event
from events.models import MarketEvent
from events.pipeline import EventIngestionPipeline
from events.repository import EventRepository
from events.rss_connector import RSSConnector, RSSSource, _parse_entries_with_stdlib, _resolve_tickers
from events.scoring import alert_from_event, score_event
from memory.manager import MemoryManager
from retrieval.fusion import RetrievalDocument, rrf_fusion
from retrieval.postgres import PostgresFullTextRetriever
from swarm.validator import should_debate


def test_rrf_fusion_prefers_documents_seen_by_multiple_channels():
    bm25 = [RetrievalDocument("a", "delivery spike", "bm25"), RetrievalDocument("b", "news", "bm25")]
    dense = [RetrievalDocument("a", "delivery spike", "dense"), RetrievalDocument("c", "factor", "dense")]
    fused = rrf_fusion(bm25, dense)
    assert fused[0].id == "a"
    assert set(fused[0].metadata["rrf_sources"]) == {"bm25", "dense"}


def test_nysa_schema_filters_unknown_tags():
    output = NysaOutput(
        sentiment_score=-0.3,
        catalyst_tags=["USFDA_ALERT", "UNKNOWN"],
        red_flag=True,
        red_flag_severity=0.8,
        news_summary="Warning letter reported.",
    )
    assert output.catalyst_tags == ["USFDA_ALERT"]


def test_event_classification_and_scoring():
    event_type, severity, sentiment = classify_event("Company receives USFDA warning letter")
    event = MarketEvent(
        event_id="evt1",
        source="NSE",
        source_type="EXCHANGE",
        published_at="2026-05-20T09:00:00Z",
        tickers=["ABC"],
        event_type=event_type,
        headline="Company receives USFDA warning letter",
        severity=severity,
        sentiment=sentiment,
        confidence=0.9,
        dedupe_hash="abc",
    )
    alert = alert_from_event(event, score_event(event, price_volume_confirmation=0.5))
    assert event.event_type == "USFDA_ALERT"
    assert alert.alert_level in {"INVESTIGATE", "HIGH_ALERT"}


def test_debate_trigger_detects_disagreement():
    assert should_debate(
        {
            "QUANTRA": {"composite_score": 0.85},
            "NYSA": {"sentiment_score": -0.6},
        }
    )


def test_memory_manager_returns_valid_package_without_services():
    package = asyncio.run(MemoryManager("ABC", "PHARMA", "NYSA").assemble_context("USFDA risk"))
    assert package.ticker == "ABC"
    assert package.agent_name == "NYSA"


def test_memory_manager_uses_postgres_retriever_when_available():
    retriever = FakeRetriever([RetrievalDocument("event:evt1", "USFDA warning letter", "postgres:market_events")])
    package = asyncio.run(
        MemoryManager("ABC", "PHARMA", "NYSA", postgres_retriever=retriever).assemble_context("USFDA risk")
    )
    assert package.items[0].tier == "T3"
    assert package.items[0].source == "event:evt1"


def test_postgres_full_text_retriever_builds_cited_documents():
    connection = FakeConnection(
        [
            (
                "evt1",
                "ABC receives USFDA warning letter",
                "Company disclosure summary",
                "NSE",
                "USFDA_ALERT",
                ["ABC"],
                "PHARMA",
                0.95,
            )
        ]
    )
    docs = PostgresFullTextRetriever(connection).search_market_events("USFDA warning", ticker="ABC")
    assert docs[0].id == "event:evt1"
    assert docs[0].source == "postgres:market_events"
    assert docs[0].metadata["event_type"] == "USFDA_ALERT"


def test_rss_ticker_resolution_is_exact_symbol_match():
    assert _resolve_tickers("ABC receives an order win; XYZ not mentioned", ["ABC", "AB", "XYZ"]) == [
        "ABC",
        "XYZ",
    ]


def test_event_pipeline_scores_and_persists_alerts():
    event = MarketEvent(
        event_id="evt1",
        source="NSE",
        source_type="EXCHANGE",
        published_at="2026-05-20T09:00:00Z",
        tickers=["ABC"],
        event_type="USFDA_ALERT",
        headline="Company receives USFDA warning letter",
        severity=0.85,
        sentiment=-0.7,
        confidence=0.9,
        dedupe_hash="abc",
    )
    connector = FakeConnector([event])
    repository = FakeRepository()
    result = EventIngestionPipeline(connector, repository).run()
    assert result.fetched == 1
    assert result.persisted == 1
    assert repository.saved[0][1].alert_level in {"INVESTIGATE", "HIGH_ALERT"}


def test_rss_source_defaults_to_news():
    source = RSSSource(name="Example", url="https://example.com/feed.xml")
    assert source.source_type == "NEWS"


def test_stdlib_rss_parser_handles_basic_feed():
    raw = """<?xml version="1.0"?>
    <rss><channel><item>
      <title>ABC receives USFDA warning letter</title>
      <description>Company disclosure mentions ABC.</description>
      <link>https://example.com/news</link>
      <pubDate>Wed, 20 May 2026 09:00:00 GMT</pubDate>
    </item></channel></rss>
    """
    entries = _parse_entries_with_stdlib(raw)
    assert entries[0]["title"] == "ABC receives USFDA warning letter"
    assert entries[0]["link"] == "https://example.com/news"


def test_rss_connector_can_read_local_feed_file(tmp_path):
    feed = tmp_path / "feed.xml"
    feed.write_text(
        """<rss><channel><item>
        <title>ABC wins order</title>
        <description>ABC receives letter of award.</description>
        <link>https://example.com/order</link>
        </item></channel></rss>""",
        encoding="utf-8",
    )
    events = RSSConnector([RSSSource("Local", str(feed), tickers=["ABC"])]).fetch_events()
    assert events[0].tickers == ["ABC"]
    assert events[0].event_type == "ORDER_WIN"


def test_local_agent_loop_blocks_uncited_trade_recommendations():
    event = MarketEvent(
        event_id="evt1",
        source="Unknown Blog",
        source_type="NEWS",
        published_at="2026-05-20T09:00:00Z",
        tickers=[],
        event_type="ORDER_WIN",
        headline="Company wins a large order",
        severity=0.65,
        sentiment=0.4,
        confidence=0.45,
        requires_confirmation=True,
        dedupe_hash="abc",
    )
    alert = alert_from_event(event, 0.8)
    run = run_local_event_loop(event, alert, evidence=[])
    assert run.vera.veto
    assert run.apex.decision == "SKIP"


def test_local_agent_loop_can_create_paper_proceed_with_evidence_and_price():
    event = MarketEvent(
        event_id="evt1",
        source="NSE",
        source_type="EXCHANGE",
        source_url="https://example.com/disclosure",
        published_at="2026-05-20T09:00:00Z",
        tickers=["ABC"],
        event_type="ORDER_WIN",
        headline="ABC receives a large order win",
        severity=0.7,
        sentiment=0.45,
        confidence=0.9,
        dedupe_hash="abc",
    )
    alert = alert_from_event(event, 0.82)
    run = run_local_event_loop(event, alert, current_price=100)
    assert not run.vera.veto
    assert run.apex.decision == "PROCEED"
    assert run.apex.stop_price == 95
    assert run.apex.target_price == 110


class FakeCursor:
    def __init__(self, rows):
        self.rows = rows
        self.executed = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def execute(self, sql, params):
        self.executed.append((sql, params))

    def fetchall(self):
        return self.rows


class FakeConnection:
    def __init__(self, rows):
        self.cursor_obj = FakeCursor(rows)

    def cursor(self):
        return self.cursor_obj


class FakeConnector:
    def __init__(self, events):
        self.events = events

    def fetch_events(self):
        return self.events


class FakeRetriever:
    def __init__(self, docs):
        self.docs = docs

    def search(self, query, ticker=None, sector=None, limit=10):
        return self.docs[:limit]


class FakeRepository(EventRepository):
    def __init__(self):
        super().__init__(None)
        self.saved = []

    def upsert_event_and_alert(self, event, alert):
        self.saved.append((event, alert))
        return True
