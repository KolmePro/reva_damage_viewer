from datetime import datetime, time

from PySide6.QtCore import QAbstractTableModel, Qt, Signal, QSize
from PySide6.QtGui import QBrush, QColor, QIcon

from core.filter_plugins import FilterCondition, FilterDefinition
from core.parser.record import DamageRecord


class DamageTableModel(QAbstractTableModel):
    data_refreshed = Signal()
    DPS_COLUMN = 0
    EVENT_COLUMN = 1
    TIME_COLUMN = 2
    ATTACKER_COLUMN = 3
    TARGET_COLUMN = 4
    SKILL_COLUMN = 5
    EFFECTS_COLUMN = 6
    DAMAGE_COLUMN = 7
    PROPERTY1_COLUMN = 8
    PROPERTY2_COLUMN = 9
    DAMAGE_RECORD_TYPES = (
        "damage_dealt",
        "damage_dealt_buffed",
        "damage_to_spirit",
        "damage_reflected",
    )
    headers = [
        "DPS", "Событие", "Время", "Атакующий", "Цель", "Навык", "Бафы",
        "Урон", "Свойство 1", "Свойство 2",
    ]
    EVENT_LABELS = {
        "damage_converted_to_healing": "Лечение уроном",
        "damage_reflected": "Отражение урона",
        "player_death": "Смерть",
        "player_revived": "Возвращение в бой",
        "player_kill": "Убийство",
        "position_swap": "Обмен местами",
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
        "targeted_effect_removed": "Снятие эффекта",
        "self_effect_removed": "Снятие эффекта",
    }

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
        self._damage_per_second: dict[datetime | time, int] = {}
        self._maximum_second_damage = 0
        self._sort_column = self.TIME_COLUMN
        self._sort_order = Qt.SortOrder.AscendingOrder

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
        if index.column() == self.DPS_COLUMN:
            return self._dps_cell_data(record, role)
        # The remaining columns preserve the original data mapping.
        col = index.column() - 1

        if record.type == "unparsed":
            if role == Qt.DisplayRole and col == 0:
                return record.origin_string
            if role == Qt.ForegroundRole:
                return QBrush(QColor("#FFA500"))
            if role == Qt.ToolTipRole:
                return record.origin_string
            if role == Qt.SizeHintRole:
                return QSize(0, 0)
            return None

        event_label = self.EVENT_LABELS.get(record.type)
        if event_label:
            if role == Qt.ForegroundRole:
                if record.type in ("player_death", "player_revived", "player_kill", "position_swap"):
                    return None
                if record.type in ("damage_absorbed", "damage_reflected", "resource_restored", "vampirism", "damage_converted_to_healing"):
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
                    if col == 6 and record.type == "damage_reflected":
                        return str(record.damage)
                    if record.type in ("resource_restored", "vampirism", "damage_converted_to_healing"):
                        if col == 6:
                            return str(record.restored_amount)
                        if col == 7:
                            return record.resource
                        if col == 8:
                            if record.drained_amount is not None:
                                return f"Цель теряет {record.drained_amount} {record.drained_resource}"
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
            if col == 8 and record.drained_amount is not None:
                return (
                    f"Неуказанная цель теряет {record.drained_amount} {record.drained_resource}. "
                    "Потеря ресурса не входит в статистику восстановления."
                )
            if col == 6 and record.type in ("resource_restored", "vampirism", "damage_converted_to_healing"):
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
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self.headers[section]
            if role == Qt.ToolTipRole and section == self.DPS_COLUMN:
                return (
                    "Суммарный урон всех отображаемых атак в эту секунду. "
                    "Цвет показывает интенсивность относительно самой сильной секунды в таблице."
                )
            return None
        if role != Qt.DisplayRole:
            return None
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
        self._rebuild_damage_per_second()
        self._sort_filtered_records()
        self.endResetModel()
        self.data_refreshed.emit()

    def sort(self, column, order=Qt.SortOrder.AscendingOrder):
        if not 0 <= column < self.columnCount():
            return
        self._sort_column = column
        self._sort_order = order
        self.beginResetModel()
        self._sort_filtered_records()
        self.endResetModel()

    def _sort_filtered_records(self):
        records_with_values = []
        records_without_values = []
        for record in self._filtered_records:
            value = self._sort_value(record, self._sort_column)
            target = records_without_values if value is None else records_with_values
            target.append((value, record))

        records_with_values.sort(
            key=lambda item: item[0],
            reverse=self._sort_order == Qt.SortOrder.DescendingOrder,
        )
        self._filtered_records = [
            record for _, record in (*records_with_values, *records_without_values)
        ]

    def _sort_value(self, record: DamageRecord, column: int):
        if column == self.DPS_COLUMN:
            return self._damage_per_second.get(self._second_key(record))
        if column == self.EVENT_COLUMN:
            if record.type == "unparsed":
                return record.origin_string.casefold()
            label = self.EVENT_LABELS.get(record.type, "")
            if record.duration_seconds is not None:
                label += f" ({record.duration_seconds} сек.)"
            return label.casefold() or None
        if record.type == "unparsed":
            return None
        if column == self.TIME_COLUMN:
            return record.timestamp or datetime.combine(datetime.min.date(), record.time)
        if column == self.ATTACKER_COLUMN:
            return self._format_actor_name(
                record.attacker,
                record.is_attacker_spirit,
                record.attacker_spirit_owner,
                self.player_name,
            ).casefold() or None
        if column == self.TARGET_COLUMN:
            return self._format_actor_name(
                record.target,
                record.is_target_spirit,
                record.target_spirit_owner,
                self.player_name,
            ).casefold() or None
        if column == self.SKILL_COLUMN:
            return record.skill.casefold() or None
        if column == self.EFFECTS_COLUMN:
            return len(record.effects) if record.effects else None
        if column == self.DAMAGE_COLUMN:
            if record.type in ("resource_restored", "vampirism", "damage_converted_to_healing"):
                return record.restored_amount
            if record.type == "damage_absorbed":
                return record.absorbed_damage
            if record.type in self.DAMAGE_RECORD_TYPES:
                return record.damage
            return None
        if column == self.PROPERTY1_COLUMN:
            if record.type in ("resource_restored", "vampirism", "damage_converted_to_healing"):
                return record.resource.casefold() or None
            if record.type in self.EVENT_LABELS:
                return None
            return record.property1.casefold() or None
        if column == self.PROPERTY2_COLUMN:
            if record.type in self.EVENT_LABELS and record.type not in (
                "resource_restored", "vampirism", "damage_converted_to_healing"
            ):
                return None
            if record.drained_amount is not None:
                return f"цель теряет {record.drained_amount} {record.drained_resource}".casefold()
            return record.property2.casefold() or None
        return None

    def _rebuild_damage_per_second(self):
        totals: dict[datetime | time, int] = {}
        for record in self._filtered_records:
            if record.type not in self.DAMAGE_RECORD_TYPES:
                continue
            key = self._second_key(record)
            totals[key] = totals.get(key, 0) + record.damage
        self._damage_per_second = totals
        self._maximum_second_damage = max(totals.values(), default=0)

    def _dps_cell_data(self, record: DamageRecord, role):
        if record.type == "unparsed":
            return None
        damage = self._damage_per_second.get(self._second_key(record))
        if damage is None:
            return None
        if role == Qt.DisplayRole:
            return f"{damage:,}".replace(",", " ")
        if role == Qt.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        if role == Qt.ForegroundRole:
            return QBrush(QColor("#FFFFFF"))
        if role == Qt.BackgroundRole:
            return QBrush(self._damage_intensity_color(damage))
        if role == Qt.ToolTipRole:
            return (
                f"Урон за эту секунду: {damage:,}.\n"
                "Цвет рассчитан относительно максимального DPS среди отображаемых строк."
            ).replace(",", " ")
        return None

    @staticmethod
    def _second_key(record: DamageRecord) -> datetime | time:
        timestamp = getattr(record, "timestamp", None)
        if isinstance(timestamp, datetime):
            return timestamp.replace(microsecond=0)
        return record.time.replace(microsecond=0)

    def _damage_intensity_color(self, damage: int) -> QColor:
        if self._maximum_second_damage <= 0:
            return QColor("#365A7A")
        intensity = max(0, damage) / self._maximum_second_damage
        if intensity < 0.5:
            return self._blend_color(QColor("#285A8C"), QColor("#9A6700"), intensity * 2)
        return self._blend_color(QColor("#9A6700"), QColor("#B42318"), (intensity - 0.5) * 2)

    @staticmethod
    def _blend_color(start: QColor, end: QColor, amount: float) -> QColor:
        amount = max(0.0, min(1.0, amount))
        return QColor(
            round(start.red() + (end.red() - start.red()) * amount),
            round(start.green() + (end.green() - start.green()) * amount),
            round(start.blue() + (end.blue() - start.blue()) * amount),
        )

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
        if record.type == "unparsed":
            return self.filters.get("show_unparsed", False)

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
            and record.type in ("resource_restored", "damage_converted_to_healing", "vampirism", "damage_absorbed", "effect_applied", "targeted_effect_applied", "effect_removed", "targeted_effect_removed", "self_effect_applied", "self_effect_removed", "self_skill_used", "self_skill_used_targeted", "skill_used_targeted", "player_death", "player_revived", "player_kill", "position_swap")
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
