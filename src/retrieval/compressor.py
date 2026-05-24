"""Simple context compression that preserves cited facts without API calls."""

from __future__ import annotations

import re

from .fusion import RetrievalDocument


class ContextCompressor:
    def compress(self, query: str, docs: list[RetrievalDocument], max_words: int = 600) -> str:
        query_terms = {term.lower() for term in re.findall(r"[A-Za-z0-9%]+", query) if len(term) > 2}
        selected: list[str] = []
        used_words = 0

        for doc in docs:
            sentences = re.split(r"(?<=[.!?])\s+", doc.text)
            ranked = sorted(
                sentences,
                key=lambda sentence: len(query_terms.intersection(sentence.lower().split())),
                reverse=True,
            )
            for sentence in ranked[:2]:
                words = sentence.split()
                if not words:
                    continue
                if used_words + len(words) > max_words:
                    return " ".join(selected)
                selected.append(sentence.strip())
                used_words += len(words)

        return " ".join(selected)
