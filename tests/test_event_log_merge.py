import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.parser.event_log import EventLog


def make_record(
    timestamp: datetime,
    origin_string: str,
    record_type: str = "damage_dealt",
):
    return SimpleNamespace(
        timestamp=timestamp,
        time=timestamp.time(),
        origin_string=origin_string,
        type=record_type,
    )


class EventLogMergeTest(unittest.TestCase):
    def test_merge_removes_overlap_but_preserves_real_repeated_records(self):
        start = datetime(2026, 8, 28, 12, 0, 0)
        first = EventLog([
            make_record(start, "A"),
            make_record(start + timedelta(seconds=1), "B"),
            make_record(start + timedelta(seconds=1), "B"),
            make_record(start + timedelta(seconds=2), "C"),
        ])
        second = EventLog([
            make_record(start + timedelta(seconds=1), "B"),
            make_record(start + timedelta(seconds=1), "B"),
            make_record(start + timedelta(seconds=2), "C"),
            make_record(start + timedelta(seconds=3), "D"),
        ])

        merged = EventLog.merge([first, second])

        self.assertEqual([record.origin_string for record in merged], ["A", "B", "B", "C", "D"])

    def test_gap_longer_than_30_seconds_starts_new_combat_segment(self):
        start = datetime(2026, 8, 28, 12, 0, 0)
        log = EventLog([
            make_record(start, "A"),
            make_record(start + timedelta(seconds=30), "B"),
            make_record(start + timedelta(seconds=61), "C"),
            make_record(start + timedelta(seconds=91), "D"),
        ])

        segments = log.combat_segments()

        self.assertEqual([(segment.start_index, segment.end_index) for segment in segments], [(0, 1), (2, 3)])
        self.assertEqual(segments[0].duration, timedelta(seconds=30))
        self.assertEqual(segments[1].start - segments[0].end, timedelta(seconds=31))

    def test_logs_without_overlap_force_combat_break_before_30_seconds(self):
        start = datetime(2026, 8, 28, 12, 0, 0)
        first = EventLog([
            make_record(start, "A"),
            make_record(start + timedelta(seconds=5), "B"),
        ])
        second = EventLog([
            make_record(start + timedelta(seconds=10), "C"),
            make_record(start + timedelta(seconds=15), "D"),
        ])

        segments = EventLog.merge([first, second]).combat_segments()

        self.assertEqual(
            [(segment.start_index, segment.end_index) for segment in segments],
            [(0, 1), (2, 3)],
        )
        self.assertEqual(segments[1].start - segments[0].end, timedelta(seconds=5))

    def test_any_overlapping_record_prevents_forced_combat_break(self):
        start = datetime(2026, 8, 28, 12, 0, 0)
        first = EventLog([
            make_record(start, "A"),
            make_record(start + timedelta(seconds=5), "shared-effect", "effect_applied"),
        ])
        second = EventLog([
            make_record(start + timedelta(seconds=5), "shared-effect", "effect_applied"),
            make_record(start + timedelta(seconds=10), "C"),
        ])

        segments = EventLog.merge([first, second]).combat_segments()

        self.assertEqual(
            [(segment.start_index, segment.end_index) for segment in segments],
            [(0, 2)],
        )

    def test_break_is_carried_across_log_without_damage_records(self):
        start = datetime(2026, 8, 28, 12, 0, 0)
        first = EventLog([make_record(start, "A")])
        effects_only = EventLog([
            make_record(start + timedelta(seconds=5), "shared-effect", "effect_applied")
        ])
        last = EventLog([
            make_record(start + timedelta(seconds=5), "shared-effect", "effect_applied"),
            make_record(start + timedelta(seconds=10), "B"),
        ])

        segments = EventLog.merge([first, effects_only, last]).combat_segments()

        self.assertEqual(
            [(segment.start_index, segment.end_index) for segment in segments],
            [(0, 0), (2, 2)],
        )

    def test_forced_combat_break_survives_later_overlapping_append(self):
        start = datetime(2026, 8, 28, 12, 0, 0)
        first = EventLog([
            make_record(start, "A"),
            make_record(start + timedelta(seconds=5), "B"),
        ])
        second = EventLog([
            make_record(start + timedelta(seconds=10), "C"),
            make_record(start + timedelta(seconds=15), "D"),
        ])
        merged = EventLog.merge([first, second])
        appended = EventLog([
            make_record(start + timedelta(seconds=15), "D"),
            make_record(start + timedelta(seconds=20), "E"),
        ])

        segments = EventLog.merge([merged, appended]).combat_segments()

        self.assertEqual(
            [(segment.start_index, segment.end_index) for segment in segments],
            [(0, 1), (2, 4)],
        )

    def test_effect_records_do_not_extend_combat_segments(self):
        start = datetime(2026, 8, 28, 12, 0, 0)
        log = EventLog([
            make_record(start, "damage-1"),
            make_record(start + timedelta(seconds=20), "effect-1", "effect_applied"),
            make_record(start + timedelta(seconds=40), "effect-2", "effect_removed"),
            make_record(start + timedelta(seconds=50), "damage-2"),
            make_record(start + timedelta(seconds=60), "effect-3", "effect_applied"),
            make_record(start + timedelta(seconds=70), "damage-3"),
        ])

        segments = log.combat_segments()

        self.assertEqual(
            [(segment.start_index, segment.end_index) for segment in segments],
            [(0, 0), (3, 5)],
        )
        self.assertEqual(segments[1].duration, timedelta(seconds=20))

    def test_parser_uses_log_date_and_handles_midnight(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_path = Path(temp_dir) / "chat_2026-08-28.html"
            log_path.write_text(
                EventLog.LOG_MARKER
                + "[23:59:59] Цель: действует эффект Усиление.<br>"
                + EventLog.LOG_MARKER
                + "[00:00:01] Цель: действует эффект Усиление.<br>",
                encoding="utf-8",
            )

            log = EventLog.parse_chat(str(log_path))

        self.assertEqual(log[0].timestamp, datetime(2026, 8, 28, 23, 59, 59))
        self.assertEqual(log[1].timestamp, datetime(2026, 8, 29, 0, 0, 1))
        self.assertEqual(log.combat_segments(), [])


if __name__ == "__main__":
    unittest.main()
