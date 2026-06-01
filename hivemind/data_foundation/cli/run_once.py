from __future__ import annotations

from hivemind.data_foundation.adapters.sample import SampleAnnouncementAdapter
from hivemind.data_foundation.parsing.events import parse_event
from hivemind.data_foundation.scoring.swing_score import score_event
from hivemind.data_foundation.storage.sqlite_store import SQLiteStore


def main() -> None:
    store = SQLiteStore()
    store.initialize()

    adapter = SampleAnnouncementAdapter()
    for candidate in adapter.fetch():
        raw_record = store.save_raw_evidence(candidate)
        event = parse_event(raw_record)
        if event is None:
            continue

        parsed_event_id = store.save_event(event)
        alert = score_event(event)
        store.save_alert(parsed_event_id, alert.swing_score, alert.reason)
        print(
            f"{event.event_type}: {event.summary} | "
            f"score={alert.swing_score} | {alert.reason}"
        )


if __name__ == "__main__":
    main()

