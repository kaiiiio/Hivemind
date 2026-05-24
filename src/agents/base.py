"""Base agent wrapper with memory-manager wiring."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from memory.manager import MemoryManager
from memory.models import ContextPackage


class BaseAgent(ABC):
    name = "BASE"

    async def build_context(
        self,
        ticker: str,
        sector: str | None,
        query: str,
        working_memory: dict[str, Any] | None = None,
    ) -> ContextPackage:
        manager = MemoryManager(ticker=ticker, sector=sector, agent_name=self.name)
        return await manager.assemble_context(query=query, working_memory=working_memory)

    @abstractmethod
    async def run(self, ticker: str, sector: str | None, inputs: dict[str, Any]) -> Any:
        """Run the agent and return a schema-validated output."""
