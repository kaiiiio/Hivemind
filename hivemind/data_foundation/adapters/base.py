from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from hivemind.data_foundation.models import RawEvidenceCandidate


class SourceAdapter(ABC):
    name: str
    source_type: str

    @abstractmethod
    def fetch(self, since: datetime | None = None) -> list[RawEvidenceCandidate]:
        """Fetch raw candidates without parsing them into market events."""

