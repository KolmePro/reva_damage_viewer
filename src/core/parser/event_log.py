import re
from collections import Counter, UserList
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Iterator, List

from .record import DamageRecord


@dataclass(frozen=True)
class CombatSegment:
    start_index: int
    end_index: int
    start: datetime
    end: datetime

    @property
    def duration(self) -> timedelta:
        return self.end - self.start


class EventLog(UserList):
    """
    Лог событий.
    """

    LOG_MARKER = '<font color = "#FF0000" [Бой]: </font>'
    CHAT_ENCODINGS = ("utf-8", "utf-8-sig", "cp1251")
    DAMAGE_RECORD_TYPES = ("damage_dealt", "damage_dealt_buffed", "damage_to_spirit")
    STATISTIC_RECORD_TYPES = (*DAMAGE_RECORD_TYPES, "resource_restored")
    DEFAULT_INTERRUPTION_THRESHOLD = timedelta(seconds=30)
    LOG_DATE_REGEX = re.compile(
        r"(?<!\d)(?P<year>20\d{2})[-_.]?(?P<month>\d{1,2})[-_.]?(?P<day>\d{1,2})"
    )

    def __init__(
        self,
        log: List[DamageRecord],
        unparsed_records: List[str] | None = None,
        forced_segment_start_record_ids: set[int] | None = None,
    ):
        super().__init__()
        self.data: List[DamageRecord] = log.copy()
        self.unparsed_records: List[str] = (unparsed_records or []).copy()
        self._forced_segment_start_record_ids = set(
            forced_segment_start_record_ids or ()
        )

    def __iter__(self) -> Iterator[DamageRecord]:
        return iter(self.data)

    @staticmethod
    def parse_chat(log_path: str, collect_unparsed: bool = False) -> "EventLog":
        """
        Парсит файл по заданному пути, возвращая лог событий.
        """
        line_regex = r'<font color = "#FF0000" \[Бой\]: </font>(.*?)<br>'

        log_file = EventLog._read_chat_text(Path(log_path))
        combat_log = re.findall(line_regex, log_file)

        events = []
        unparsed_records = []
        for string in combat_log:
            try:
                damage_record = DamageRecord.try_to_parse(string)
            except (AttributeError, KeyError, TypeError, ValueError):
                damage_record = None
            if not damage_record:
                if collect_unparsed:
                    unparsed_records.append(string)
                    events.append(DamageRecord.unparsed(string, events[-1].time if events else time.min))
                continue
            events.append(damage_record)

        EventLog._assign_timestamps(events, Path(log_path))
        return EventLog(events, unparsed_records)

    @staticmethod
    def merge(logs: List["EventLog"]) -> "EventLog":
        """
        Объединяет логи в хронологическом порядке.

        Если файлы пересекаются, сохраняется максимальное число одинаковых
        записей из одного файла. Благодаря этому реальные повторные атаки не
        теряются, а копии строк из перекрывающихся файлов не дублируются.
        """
        if not logs:
            return EventLog([])

        forced_segment_start_record_ids = {
            record_id
            for log in logs
            for record_id in log._forced_segment_start_record_ids
        }
        chronological_logs = sorted(
            (
                (log_index, log, min(log._resolved_timestamps()))
                for log_index, log in enumerate(logs)
                if log
            ),
            key=lambda item: (item[2], item[0]),
        )
        force_next_damage_segment = False
        for (_, previous_log, _), (_, current_log, _) in zip(
            chronological_logs,
            chronological_logs[1:],
        ):
            previous_fingerprints = {
                EventLog._record_fingerprint(record) for record in previous_log
            }
            current_fingerprints = {
                EventLog._record_fingerprint(record) for record in current_log
            }
            if previous_fingerprints.isdisjoint(current_fingerprints):
                force_next_damage_segment = True
            if not force_next_damage_segment:
                continue

            first_damage_record = next(
                (
                    record
                    for record in current_log
                    if record.type in EventLog.DAMAGE_RECORD_TYPES
                ),
                None,
            )
            if first_damage_record is not None:
                forced_segment_start_record_ids.add(id(first_damage_record))
                force_next_damage_segment = False

        maximum_occurrences = Counter()
        for log in logs:
            occurrences = Counter(EventLog._record_fingerprint(record) for record in log)
            maximum_occurrences |= occurrences

        selected_occurrences = Counter()
        selected_records = []
        for log_index, log in enumerate(logs):
            for record_index, record in enumerate(log):
                fingerprint = EventLog._record_fingerprint(record)
                if selected_occurrences[fingerprint] >= maximum_occurrences[fingerprint]:
                    continue
                selected_occurrences[fingerprint] += 1
                selected_records.append(
                    (getattr(record, "timestamp", None), log_index, record_index, record)
                )

        selected_records.sort(
            key=lambda item: (
                item[0] or datetime.combine(date.min, item[3].time),
                item[1],
                item[2],
            )
        )
        records = [item[3] for item in selected_records]
        unparsed_records = list(
            dict.fromkeys(record for log in logs for record in log.unparsed_records)
        )
        return EventLog(
            records,
            unparsed_records,
            forced_segment_start_record_ids,
        )

    def damage_per_second(self) -> float | None:
        """DPS по атакам лога; None, если длительность равна нулю."""
        damage_records = [record for record in self.data if record.type in self.DAMAGE_RECORD_TYPES]
        return EventLog(damage_records).amount_per_second()

    def amount_per_second(self, *, converted_healing: bool = False) -> float | None:
        """Урон и восстановление в секунду по событиям текущей выборки."""
        record_types = ("damage_converted_to_healing",) if converted_healing else self.STATISTIC_RECORD_TYPES
        records = [record for record in self.data if record.type in record_types]
        if not records:
            return 0.0

        timestamps = EventLog(records)._resolved_timestamps()
        duration = (max(timestamps) - min(timestamps)).total_seconds()
        if duration <= 0:
            return None
        return sum(
            (record.restored_amount or 0) if record.type in ("resource_restored", "damage_converted_to_healing") else record.damage
            for record in records
        ) / duration

    def combat_segments(
        self,
        interruption_threshold: timedelta | None = None,
    ) -> List[CombatSegment]:
        threshold = (
            self.DEFAULT_INTERRUPTION_THRESHOLD
            if interruption_threshold is None
            else interruption_threshold
        )
        damage_indexes = [
            index
            for index, record in enumerate(self.data)
            if record.type in self.DAMAGE_RECORD_TYPES
        ]
        if not damage_indexes:
            return []

        timestamps = self._resolved_timestamps()
        segments = []
        start_index = damage_indexes[0]
        previous_damage_index = damage_indexes[0]
        for damage_index in damage_indexes[1:]:
            forced_interruption = (
                id(self.data[damage_index]) in self._forced_segment_start_record_ids
            )
            if (
                not forced_interruption
                and timestamps[damage_index] - timestamps[previous_damage_index]
                <= threshold
            ):
                previous_damage_index = damage_index
                continue
            segments.append(
                CombatSegment(
                    start_index=start_index,
                    end_index=previous_damage_index,
                    start=timestamps[start_index],
                    end=timestamps[previous_damage_index],
                )
            )
            start_index = damage_index
            previous_damage_index = damage_index

        segments.append(
            CombatSegment(
                start_index=start_index,
                end_index=previous_damage_index,
                start=timestamps[start_index],
                end=timestamps[previous_damage_index],
            )
        )
        return segments

    @staticmethod
    def _read_chat_text(log_path: Path) -> str:
        raw_bytes = log_path.read_bytes()

        for encoding in EventLog.CHAT_ENCODINGS:
            try:
                text = raw_bytes.decode(encoding)
            except UnicodeDecodeError:
                continue

            if EventLog.LOG_MARKER in text:
                return text

        for encoding in EventLog.CHAT_ENCODINGS:
            try:
                return raw_bytes.decode(encoding)
            except UnicodeDecodeError:
                continue

        return raw_bytes.decode("utf-8", errors="replace")

    @staticmethod
    def _infer_log_date(log_path: Path) -> date:
        match = EventLog.LOG_DATE_REGEX.search(log_path.stem)
        if match:
            try:
                return date(
                    int(match["year"]),
                    int(match["month"]),
                    int(match["day"]),
                )
            except ValueError:
                pass
        return datetime.fromtimestamp(log_path.stat().st_mtime).date()

    @staticmethod
    def _assign_timestamps(events: List[DamageRecord], log_path: Path):
        current_date = EventLog._infer_log_date(log_path)
        previous_time = None
        for event in events:
            if previous_time is not None and event.time < previous_time:
                current_date += timedelta(days=1)
            event.timestamp = datetime.combine(current_date, event.time)
            previous_time = event.time

    @staticmethod
    def _record_fingerprint(record: DamageRecord):
        return getattr(record, "timestamp", None), record.origin_string

    def _resolved_timestamps(self) -> List[datetime]:
        timestamps = []
        current_date = date.min
        previous_time = None
        for record in self.data:
            record_timestamp = getattr(record, "timestamp", None)
            if record_timestamp is not None:
                timestamp = record_timestamp
                current_date = timestamp.date()
            else:
                if previous_time is not None and record.time < previous_time:
                    current_date += timedelta(days=1)
                timestamp = datetime.combine(current_date, record.time)
            timestamps.append(timestamp)
            previous_time = record.time
        return timestamps

    def get_time_slice(self, start: time, end: time) -> "EventLog":
        """
        Отфильтровывает из списка события по времени.
        """
        filtered_events = []
        for event in self._data:
            if start <= event.time <= end:
                filtered_events.append(event)

        return EventLog(filtered_events, self.unparsed_records)

    def filter(
        self,
        attacker: str = None,
        is_attacker_spirit: bool = None,
        target: str = None,
        is_target_spirit: bool = None,
        skill: str = None,
        damage: int = None,
        property1: str = None,
        property2: str = None,
    ) -> "EventLog":
        """
        Отфильтровывает из списка события по условию.
        """
        filtered_events = []
        for event in self.data:
            if attacker is not None and event.attacker != attacker:
                continue
            if is_attacker_spirit is not None and event.is_attacker_spirit != is_attacker_spirit:
                continue
            if target is not None and event.target != target:
                continue
            if is_target_spirit is not None and event.is_target_spirit != is_target_spirit:
                continue
            if skill is not None and event.skill != skill:
                continue
            if damage is not None and event.damage != damage:
                continue
            if property1 is not None and event.property1 != property1:
                continue
            if property2 is not None and event.property2 != property2:
                continue
            filtered_events.append(event)

        return EventLog(filtered_events, self.unparsed_records)
