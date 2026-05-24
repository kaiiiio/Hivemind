"""Shared memory models.

The AI layer should pass cited, compact evidence between components. It should
not persist raw chain-of-thought.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(slots=True)
class MemoryItem:
    """A single retrieved memory item from any tier."""

    tier: str
    text: str
    source: str
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ContextPackage:
    """Context assembled for one agent call."""

    ticker: str
    sector: str | None
    agent_name: str
    budget_tokens: int
    items: list[MemoryItem] = field(default_factory=list)
    retrieval_log: list[dict[str, Any]] = field(default_factory=list)

    @property
    def estimated_tokens(self) -> int:
        return sum(estimate_tokens(item.text) for item in self.items)

    def add_items(self, items: list[MemoryItem], max_tokens: int) -> None:
        used = 0
        for item in items:
            item_tokens = estimate_tokens(item.text)
            if item_tokens == 0:
                continue
            if used + item_tokens > max_tokens:
                break
            self.items.append(item)
            used += item_tokens

    def as_prompt_context(self) -> str:
        lines = []
        for item in self.items:
            label = f"[{item.tier}:{item.source}]"
            lines.append(f"{label} {item.text}")
        return "\n".join(lines)


def estimate_tokens(text: str) -> int:
    """Cheap token estimate used before adding tiktoken."""

    if not text:
        return 0
    return max(1, len(text.split()) * 4 // 3)


def new_run_id() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
