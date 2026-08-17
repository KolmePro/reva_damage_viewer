from PySide6.QtCore import QAbstractTableModel, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QIcon

from core.filter_plugins import FilterCondition, FilterDefinition
from core.parser.record import DamageRecord


class DamageTableModel(QAbstractTableModel):
    data_refreshed = Signal()
    headers = ["", "Время", "Атакующий", "Цель", "Навык", "Бафы", "Урон", "Свойство 1", "Свойство 2"]

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

        if role == Qt.ForegroundRole and record.type in ("effect_applied", "effect_removed"):
            color = QColor("#AAFFAA") if record.type == "effect_applied" else QColor("#FFAAAA")
            return QBrush(color)

        if record.type in ("effect_applied", "effect_removed"):
            if role == Qt.DisplayRole and col == 0:
                action = "действует" if record.type == "effect_applied" else "перестал действовать"
                target_name = self._format_actor_name(
                    record.target,
                    record.is_target_spirit,
                    record.target_spirit_owner,
                )
                return f"Эффект '{record.skill}' {action} на цель {target_name}"

            if role == Qt.DecorationRole and col == 0:
                return QIcon.fromTheme("emblem-mail")

            if role == Qt.ToolTipRole and col == 0:
                return record.origin_string

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
                )
            if col == 3:
                return self._format_actor_name(
                    record.target,
                    record.is_target_spirit,
                    record.target_spirit_owner,
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
        for definition in self.filter_definitions:
            if self.filters.get(definition.key, True):
                continue
            if self._record_matches_definition(record, definition):
                return False

        if not self._match_text(self.attacker_name, record.attacker):
            return False
        if not self._match_text(self.target_name, record.target):
            return False
        if not self._match_text(self.skill_name, record.skill):
            return False
        return True

    def _record_matches_definition(self, record: DamageRecord, definition: FilterDefinition):
        return all(self._match_condition(record, condition) for condition in definition.conditions)

    def _match_condition(self, record: DamageRecord, condition: FilterCondition):
        left_value = getattr(record, condition.field)
        right_value = self._resolve_condition_value(condition.value)

        if condition.operator == "eq":
            return left_value == right_value
        if condition.operator == "ne":
            return left_value != right_value
        if condition.operator == "in":
            return left_value in right_value
        if condition.operator == "not_in":
            return left_value not in right_value
        return False

    def _resolve_condition_value(self, value):
        if isinstance(value, str) and value.startswith("$"):
            return getattr(self, value[1:], "")
        return value

    @staticmethod
    def _format_actor_name(name: str, is_spirit: bool, spirit_owner: str = "") -> str:
        if not is_spirit:
            return name
        if spirit_owner:
            return f"{name} (дух {spirit_owner})"
        return f"{name} (дух)"
