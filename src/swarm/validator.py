"""Debate and validation helpers."""

from __future__ import annotations

from typing import Any


def should_debate(agent_outputs: dict[str, dict[str, Any]], threshold: float = 0.3) -> bool:
    """Trigger debate when directional scores materially disagree."""

    scores = []
    for output in agent_outputs.values():
        for key in ("bullish_score", "composite_score", "confidence", "sentiment_score"):
            if key in output and isinstance(output[key], (int, float)):
                value = float(output[key])
                if key == "sentiment_score":
                    value = (value + 1) / 2
                scores.append(value)
                break
    return bool(scores) and max(scores) - min(scores) > threshold
