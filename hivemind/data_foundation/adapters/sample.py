from __future__ import annotations

from datetime import datetime, timezone

from hivemind.data_foundation.adapters.base import SourceAdapter
from hivemind.data_foundation.models import RawEvidenceCandidate


class SampleAnnouncementAdapter(SourceAdapter):
    name = "sample_exchange_announcement"
    source_type = "exchange_announcement"

    def fetch(self, since: datetime | None = None) -> list[RawEvidenceCandidate]:
        return [
            RawEvidenceCandidate(
                source_name=self.name,
                source_type=self.source_type,
                source_url="sample://dynacons-order-win",
                title="Dynacons Systems wins Rs 750 crore project",
                raw_text=(
                    "Dynacons Systems and Solutions Limited has received a "
                    "project/order worth Rs 750 crore for digital "
                    "infrastructure services."
                ),
                published_at=datetime(2026, 5, 24, tzinfo=timezone.utc),
                metadata={"fixture": True},
            )
        ]

