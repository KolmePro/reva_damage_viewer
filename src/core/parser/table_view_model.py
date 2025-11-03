from PySide6.QtCore import QAbstractTableModel, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QIcon

from core.parser.record import DamageRecord


class DamageTableModel(QAbstractTableModel):
    data_refreshed = Signal()
    headers = ["", "Время", "Атакующий", "Цель", "Навык", "Бафы", "Урон", "Свойство 1", "Свойство 2"]

    def __init__(self):
        super().__init__()
        self._all_records = []
        self._filtered_records = []
        self.filters = {
            "outgoing_spirit_damage": True,
            "incoming_spirit_damage": True,
            "attack_common": True,
            "attack_critical": True,
            "attack_block": True,
            "attack_combo": True,
            "attack_p": True,
            "attack_m": True,
            "attack_o": True,
        }

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

        # --- Цвет фона для эффектов ---
        if role == Qt.ForegroundRole and record.type in ("effect_applied", "effect_removed"):
            color = QColor("#AAFFAA") if record.type == "effect_applied" else QColor("#FFAAAA")
            return QBrush(color)

        # --- Обработка строк с эффектами ---
        if record.type in ("effect_applied", "effect_removed"):
            # Текст в первой колонке
            if role == Qt.DisplayRole and col == 0:
                action = "действует" if record.type == "effect_applied" else "перестал действовать"
                return f"Эффект '{record.skill}' {action} на цель {record.target}"

            # Иконка в первой колонке
            if role == Qt.DecorationRole and col == 0:
                return QIcon.fromTheme("emblem-mail")

            # Tooltip с исходной строкой лога
            if role == Qt.ToolTipRole and col == 0:
                return record.origin_string

            # Остальные ячейки — пустые
            return None

        # --- Обычные записи урона ---
        if role == Qt.DisplayRole:
            if col == 0:
                return ""
            elif col == 1:
                return record.time.strftime("%H:%M:%S")
            elif col == 2:
                return record.attacker
            elif col == 3:
                return record.target
            elif col == 4:
                return record.skill
            elif col == 5:
                if record.effects:
                    return str(len(record.effects))
            elif col == 6:
                return str(record.damage)
            elif col == 7:
                return record.property1
            elif col == 8:
                return record.property2

        elif role == Qt.DecorationRole:
            if col == 0:
                return QIcon.fromTheme("emblem-mail")
            elif col == 5 and record.effects:
                return QIcon.fromTheme("dialog-information")

        elif role == Qt.ToolTipRole:
            if col == 0:
                return record.origin_string
            elif col == 5:
                return "\n".join(record.effects) if record.effects else "Нет бафов."

        elif role == Qt.ForegroundRole and col == 6:
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
        filtered = [r for r in self._all_records if self._record_allowed(r)]
        self._filtered_records = filtered
        self.endResetModel()

        self.data_refreshed.emit()

    def _record_allowed(self, r):
        if not self.filters.get("outgoing_spirit_damage") and r.is_attacker_spirit:
            return False
        if not self.filters.get("incoming_spirit_damage") and r.is_target_spirit:
            return False
        if not self.filters.get("attack_common") and r.property2 == "Обычный":
            return False
        if not self.filters.get("attack_critical") and r.property2 == "Критический удар":
            return False
        if not self.filters.get("attack_block") and r.property2 == "Блокирование":
            return False
        if not self.filters.get("attack_combo") and r.property2 == "Комбо-удар":
            return False
        if not self.filters.get("attack_p") and r.property1 == "Сила атаки":
            return False
        if not self.filters.get("attack_m") and r.property1 == "Сила заклинаний":
            return False
        if not self.filters.get("attack_o") and r.property1 == "Обычный":
            return False
        return True
