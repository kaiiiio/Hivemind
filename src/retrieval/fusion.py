"""Reciprocal Rank Fusion for heterogeneous retrieval channels."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RetrievalDocument:
    id: str
    text: str
    source: str
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


def rrf_fusion(*ranked_lists: list[RetrievalDocument], k: int = 60, limit: int = 100) -> list[RetrievalDocument]:
    """Fuse ranked retrieval lists without normalizing scores."""

    scores: dict[str, float] = defaultdict(float)
    docs: dict[str, RetrievalDocument] = {}
    source_breakdown: dict[str, list[str]] = defaultdict(list)

    for results in ranked_lists:
        for rank, doc in enumerate(results):
            docs[doc.id] = doc
            scores[doc.id] += 1.0 / (k + rank + 1)
            source_breakdown[doc.id].append(doc.source)

    fused = []
    for doc_id, score in sorted(scores.items(), key=lambda item: item[1], reverse=True)[:limit]:
        doc = docs[doc_id]
        metadata = dict(doc.metadata)
        metadata["rrf_sources"] = source_breakdown[doc_id]
        fused.append(RetrievalDocument(doc.id, doc.text, doc.source, score, metadata))
    return fused
