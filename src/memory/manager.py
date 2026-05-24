"""Tiered Memory Manager used by agents.

This is intentionally useful on day one: it returns recent episodes and learned
procedures when services exist, and otherwise returns an empty but valid context
package. Agents never talk to storage directly.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from retrieval.postgres import PostgresFullTextRetriever

from .models import ContextPackage, MemoryItem
from .redis_store import RedisEpisodicStore

logger = logging.getLogger(__name__)


AGENT_CONTEXT_BUDGETS = {
    "VEGA": 8000,
    "NYSA": 6000,
    "QUANTRA": 6000,
    "LEXA": 10000,
    "SECTORA": 6000,
    "VERA": 12000,
    "APEX": 16000,
    "SENTINEL": 4000,
}

SYSTEM_PROMPT_TOKENS = {
    "VEGA": 1500,
    "NYSA": 700,
    "QUANTRA": 500,
    "LEXA": 2500,
    "SECTORA": 500,
    "VERA": 3000,
    "APEX": 5000,
    "SENTINEL": 700,
}


class MemoryManager:
    """Assembles T2/T3/T4/T5 memory into a compact context package."""

    def __init__(
        self,
        ticker: str,
        sector: str | None,
        agent_name: str,
        budget_tokens: int | None = None,
        episodic_store: RedisEpisodicStore | None = None,
        postgres_retriever: PostgresFullTextRetriever | None = None,
    ):
        self.ticker = ticker
        self.sector = sector
        self.agent_name = agent_name.upper()
        self.budget_tokens = budget_tokens or AGENT_CONTEXT_BUDGETS.get(self.agent_name, 6000)
        self.episodic_store = episodic_store or RedisEpisodicStore()
        self.postgres_retriever = postgres_retriever

    async def assemble_context(self, query: str, working_memory: dict[str, Any] | None = None) -> ContextPackage:
        t2, t3, t5, t4 = await asyncio.gather(
            self._fetch_t2_episodes(),
            self._fetch_t3_semantic(query),
            self._fetch_t5_graph(),
            self._fetch_t4_procedures(),
        )

        package = self._assemble_within_budget(t2, t3, t5, t4)
        package.retrieval_log.append(
            {
                "agent": self.agent_name,
                "ticker": self.ticker,
                "query": query,
                "counts": {"t2": len(t2), "t3": len(t3), "t5": len(t5), "t4": len(t4)},
            }
        )
        if working_memory is not None:
            working_memory.setdefault("retrieval_log", []).extend(package.retrieval_log)
        return package

    async def _fetch_t2_episodes(self) -> list[MemoryItem]:
        episodes = self.episodic_store.read_recent_ticker_episodes(self.ticker, limit=5)
        mistakes = self.episodic_store.read_mistakes(self.agent_name, limit=5)
        items = [
            MemoryItem("T2", str(episode), f"episode:{self.ticker}", score=1.0)
            for episode in episodes
        ]
        items.extend(
            MemoryItem("T2", f"Recent mistake to avoid: {mistake}", f"mistake:{self.agent_name}", score=1.0)
            for mistake in mistakes
        )
        return items

    async def _fetch_t3_semantic(self, query: str) -> list[MemoryItem]:
        if not self.postgres_retriever:
            logger.debug("T3 retrieval not configured yet for query: %s", query)
            return []
        docs = self.postgres_retriever.search(query, ticker=self.ticker, sector=self.sector, limit=10)
        return [
            MemoryItem(
                tier="T3",
                text=doc.text,
                source=doc.id,
                score=doc.score,
                metadata={"retrieval_source": doc.source, **doc.metadata},
            )
            for doc in docs
        ]

    async def _fetch_t5_graph(self) -> list[MemoryItem]:
        logger.debug("T5 graph retrieval not configured yet for ticker: %s", self.ticker)
        return []

    async def _fetch_t4_procedures(self) -> list[MemoryItem]:
        logger.debug("T4 procedure retrieval not configured yet for agent: %s", self.agent_name)
        return []

    def _assemble_within_budget(
        self,
        t2: list[MemoryItem],
        t3: list[MemoryItem],
        t5: list[MemoryItem],
        t4: list[MemoryItem],
    ) -> ContextPackage:
        package = ContextPackage(
            ticker=self.ticker,
            sector=self.sector,
            agent_name=self.agent_name,
            budget_tokens=self.budget_tokens,
        )
        available = max(0, self.budget_tokens - SYSTEM_PROMPT_TOKENS.get(self.agent_name, 700))
        for items, weight in ((t2, 0.35), (t3, 0.35), (t5, 0.20), (t4, 0.10)):
            package.add_items(items, int(available * weight))
        return package
