from datetime import datetime, time

from PySide6.QtCore import QAbstractTableModel, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QIcon

from core.filter_plugins import FilterCondition, FilterDefinition
from core.parser.record import DamageRecord


class DamageTableModel(QAbstractTableModel):
    data_refreshed = Signal()
    headers = ["Событие", "Время", "Атакующий", "Цель", "Навык", "Бафы", "Урон", "Свойство 1", "Свойство 2"]

    def __init__(self, filter_definitions: list[FilterDefinition] | None = None):
        super().__init__()
        self._all_records = []
        self._filtered_records = []
        self.filter_definitions = filter_definitions or []
        self.filters = {definition.key: definition.default_enabled for definition in self.filter_definitions}
        self.player_name = ""
        self.attacker_name = ""
        self.target_name = ""
        self.skill_name = ""
        self.start_time: time | None = None
        self.end_time: time | None = None
        self.start_timestamp: datetime | None = None
        self.end_timestamp: datetime | None = None
        self.include_start_timestamp = True
        self.include_end_timestamp = True
        self.timestamp_ranges: list[tuple[datetime, datetime, bool, bool]] = []
        self.minimum_damage = 0
        self.maximum_damage = 0

    def set_records(self, records: list[DamageRecord]):
        self._all_records = records
        self.apply_filters()

    def rowCount(self, parent=None):
        return len(self._filtered_records)

    def columnCount(self, parent=None):
        return len(self.headers)

    def data(self, index, role):
        if not index.isValid():
            return None

        record = self._filtered_records[index.row()]
        col = index.column()

        event_labels = {
            "vampirism": "Вампиризм",
            "resource_restored": "Восстановление ресурса",
            "damage_absorbed": "Поглощение урона",
            "self_skill_used": "Применение умения",
            "self_skill_used_targeted": "Применение умения",
            "skill_used_targeted": "Применение умения",
            "effect_applied": "Наложение эффекта",
            "targeted_effect_applied": "Наложение эффекта",
            "self_effect_applied": "Наложение эффекта",
            "effect_removed": "Снятие эффекта",
            "self_effect_removed": "Снятие эффекта",
        }
        event_label = event_labels.get(record.type)
        if event_label:
            if role == Qt.ForegroundRole:
                if record.type in ("damage_absorbed", "resource_restored", "vampirism"):
                    color = "#99CCFF"
                elif record.type in ("self_skill_used", "self_skill_used_targeted", "skill_used_targeted"):
                    color = "#CCBBFF"
                elif record.type in ("effect_applied", "self_effect_applied", "targeted_effect_applied"):
                    color = "#AAFFAA"
                else:
                    color = "#FFAAAA"
                return QBrush(QColor(color))
            if role == Qt.DisplayRole:
                if col == 0:
                    if record.duration_seconds is not None:
                        event_label += f" ({record.duration_seconds} сек.)"
                    return event_label
                if col >= 5:
                    if record.type in ("resource_restored", "vampirism"):
                        if col == 6:
                            return str(record.restored_amount)
                        if col == 7:
                            return record.resource
                        if col == 8:
                            return record.property2
                    if col == 6 and record.absorbed_damage is not None:
                        return str(record.absorbed_damage)
                    return None

        if role == Qt.DisplayRole:
            if col == 0:
                return ""
            if col == 1:
                return record.time.strftime("%H:%M:%S")
            if col == 2:
                return self._format_actor_name(
                    record.attacker,
                    record.is_attacker_spirit,
                    record.attacker_spirit_owner,
                    self.player_name,
                )
            if col == 3:
                return self._format_actor_name(
                    record.target,
                    record.is_target_spirit,
                    record.target_spirit_owner,
                    self.player_name,
                )
            if col == 4:
                return record.skill
            if col == 5 and record.effects:
                return str(len(record.effects))
            if col == 6:
                return str(record.damage)
            if col == 7:
                return record.property1
            if col == 8:
                return record.property2

        if role == Qt.DecorationRole:
            if col == 0:
                return QIcon.fromTheme("emblem-mail")
            if col == 5 and record.effects:
                return QIcon.fromTheme("dialog-information")

        if role == Qt.ToolTipRole:
            if col == 6 and record.type in ("resource_restored", "vampirism"):
                return f"Восстановлено {record.restored_amount} {record.resource}."
            if col == 6 and record.type == "damage_absorbed":
                return "Поглощённый урон; не учитывается в статистике нанесённого урона."
            if col == 0:
                return record.origin_string
            if col == 5:
                return "\n".join(record.effects) if record.effects else "Нет бафов."

        if role == Qt.ForegroundRole and col == 6:
            damage_colors = {
                "Сила атаки": "#FF9999",
                "Сила заклинаний": "#99CCFF",
            }
            color = damage_colors.get(record.property1)
            if color:
                return QBrush(QColor(color))

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.headers[section]
        return str(section + 1)

    def set_filter(self, key, value):
        self.filters[key] = value
        self.apply_filters()

    def set_filters(self, filters: dict[str, bool]):
        self.filters.update(filters)
        self.apply_filters()

    def set_time_range(self, start: time | None, end: time | None):
        self.start_time = start
        self.end_time = end
        self.start_timestamp = None
        self.end_timestamp = None
        self.include_start_timestamp = True
        self.include_end_timestamp = True
        self.timestamp_ranges = []
        self.apply_filters()

    def set_timestamp_range(
        self,
        start: datetime,
        end: datetime,
        include_start: bool = True,
        include_end: bool = True,
    ):
        self.set_timestamp_ranges([(start, end, include_start, include_end)])

    def set_timestamp_ranges(
        self,
        ranges: list[tuple[datetime, datetime, bool, bool]],
    ):
        self.start_time = None
        self.end_time = None
        self.timestamp_ranges = list(ranges)
        if len(ranges) == 1:
            start, end, include_start, include_end = ranges[0]
            self.start_timestamp = start
            self.end_timestamp = end
            self.include_start_timestamp = include_start
            self.include_end_timestamp = include_end
        else:
            self.start_timestamp = None
            self.end_timestamp = None
            self.include_start_timestamp = True
            self.include_end_timestamp = True
        self.apply_filters()

    def clear_time_range(self, apply_filters: bool = True):
        self.start_time = None
        self.end_time = None
        self.start_timestamp = None
        self.end_timestamp = None
        self.include_start_timestamp = True
        self.include_end_timestamp = True
        self.timestamp_ranges = []
        if apply_filters:
            self.apply_filters()

    def apply_filters(self):
        self.beginResetModel()
        self._filtered_records = [record for record in self._all_records if self._record_allowed(record)]
        self.endResetModel()
        self.data_refreshed.emit()

    def _match_text(self, query, text):
        invert = query.startswith("-")
        if invert:
            query = query[1:]
        text = text.lower()
        result = all(part in text for part in query.lower().split())
        return not result if invert else result

    def _record_allowed(self, record: DamageRecord):
        if not self._record_in_time_range(record):
            return False

        alternative_matches = {}
        for definition in self.filter_definitions:
            if definition.alternative_group:
                if self._record_matches_definition(record, definition):
                    group = definition.alternative_group
                    alternative_matches[group] = (
                        alternative_matches.get(group, False)
                        or self.filters.get(definition.key, True)
                    )
                continue
            if self.filters.get(definition.key, True):
                continue
            if self._record_matches_definition(record, definition):
                return False
        if any(not enabled for enabled in alternative_matches.values()):
            return False

        if not self._match_text(self.attacker_name, record.attacker):
            return False
        if not self._match_text(self.target_name, record.target):
            return False
        if not self._match_text(self.skill_name, record.skill):
            return False
        if (
            (self.minimum_damage or self.maximum_damage)
            and record.type in ("resource_restored", "vampirism", "damage_absorbed", "effect_applied", "targeted_effect_applied", "effect_removed", "self_effect_applied", "self_effect_removed", "self_skill_used", "self_skill_used_targeted", "skill_used_targeted")
        ):
            return False
        if self.minimum_damage and record.damage <= self.minimum_damage:
            return False
        if self.maximum_damage and record.damage >= self.maximum_damage:
            return False
        return True

    def _record_in_time_range(self, record: DamageRecord) -> bool:
        if self.timestamp_ranges:
            timestamp = getattr(record, "timestamp", None)
            if not isinstance(timestamp, datetime):
                return False
            return any(
                self._timestamp_in_range(
                    timestamp,
                    start,
                    end,
                    include_start,
                    include_end,
                )
                for start, end, include_start, include_end in self.timestamp_ranges
            )

        if self.start_time is None and self.end_time is None:
            return True

        record_time = record.time
        if self.start_time is not None and self.end_time is not None:
            if self.start_time <= self.end_time:
                return self.start_time <= record_time <= self.end_time
            return record_time >= self.start_time or record_time <= self.end_time
        if self.start_time is not None:
            return record_time >= self.start_time
        return record_time <= self.end_time

    @staticmethod
    def _timestamp_in_range(
        timestamp: datetime,
        start: datetime,
        end: datetime,
        include_start: bool,
        include_end: bool,
    ) -> bool:
        if timestamp < start or timestamp > end:
            return False
        if timestamp == start and not include_start:
            return False
        if timestamp == end and not include_end:
            return False
        return True

    def _record_matches_definition(self, record: DamageRecord, definition: FilterDefinition):
        return all(self._match_condition(record, condition) for condition in definition.conditions)

    def _match_condition(self, record: DamageRecord, condition: FilterCondition):
        left_value = getattr(record, condition.field)
        right_value = self._resolve_condition_value(condition.value)

        if (
            condition.value == "$player_name"
            and condition.field in ("attacker", "target")
            and condition.operator in ("eq", "ne")
        ):
            is_player = (
                not getattr(record, f"is_{condition.field}_spirit")
                and (left_value == "Вы" or bool(self.player_name) and left_value == self.player_name)
            )
            return is_player if condition.operator == "eq" else not is_player

        if condition.operator == "eq":
            return left_value == right_value
        if condition.operator == "ne":
            return left_value != right_value
        if condition.operator == "in":
            return left_value in right_value
        if condition.operator == "not_in":
            return left_value not in right_value
        if condition.operator == "startswith":
            return str(left_value).startswith(str(right_value))
        if condition.operator == "not_startswith":
            return not str(left_value).startswith(str(right_value))
        return False

    def _resolve_condition_value(self, value):
        if isinstance(value, str) and value.startswith("$"):
            return getattr(self, value[1:], "")
        return value

    @staticmethod
    def _format_actor_name(name: str, is_spirit: bool, spirit_owner: str = "", player_name: str = "") -> str:
        if name == "Вы" and player_name:
            name = player_name
        if not is_spirit:
            return name
        if spirit_owner:
            if spirit_owner == "Вы" and player_name:
                spirit_owner = player_name
            return f"{name} (дух {spirit_owner})"
        return f"{name} (дух)"
