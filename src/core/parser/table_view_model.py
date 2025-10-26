from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QBrush, QColor, QIcon

from core.parser.record import DamageRecord


class DamageTableModel(QAbstractTableModel):
    headers = ["", "Время", "Атакующий", "Цель", "Навык", "Урон", "Свойство 1", "Свойство 2"]

    def __init__(self):
        super().__init__()
        self._all_records = []
        self._filtered_records = []
        self.filters = {
            "outgoing_spirit_damage": True,
            "incoming_spirit_damage": True,
            "cattack_common": True,
            "attack_critical": True,
            "attack_block": True,
            "attack_combo": True,
            "attack_p": True,
            "attack_m": True,
            "attack_o": True,
        }
        self.msg_icon = QIcon.fromTheme("emblem-mail")

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

        if role == Qt.DisplayRole:
            if col == 0:
                return ""  # иконка вместо текста
            elif col == 1:
                return record.time.strftime("%H:%M:%S")
            elif col == 2:
                return record.attacker
            elif col == 3:
                return record.target
            elif col == 4:
                return record.skill
            elif col == 5:
                return str(record.damage)
            elif col == 6:
                return record.property1
            elif col == 7:
                return record.property2
        elif role == Qt.DecorationRole and col == 0:
            return self.msg_icon
        elif role == Qt.ToolTipRole and col == 0:
            return record.origin_string
        elif role == Qt.ForegroundRole and col == 5:
            if record.property1 == "Сила атаки":
                return QBrush(QColor("#FF9999"))
            elif record.property1 == "Сила заклинаний":
                return QBrush(QColor("#99CCFF"))

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
        filtered = self._all_records
        if not self.filters.get("outgoing_spirit_damage"):
            filtered = [r for r in filtered if not r.is_attacker_spirit]
        if not self.filters.get("incoming_spirit_damage"):
            filtered = [r for r in filtered if not r.is_target_spirit]
        if not self.filters.get("cattack_common"):
            filtered = [r for r in filtered if r.property2 != "Обычный"]
        if not self.filters.get("attack_critical"):
            filtered = [r for r in filtered if r.property2 != "Критический удар"]
        if not self.filters.get("attack_block"):
            filtered = [r for r in filtered if r.property2 != "Блокирование"]
        if not self.filters.get("attack_combo"):
            filtered = [r for r in filtered if r.property2 != "Комбо-удар"]
        if not self.filters.get("attack_p"):
            filtered = [r for r in filtered if r.property1 != "Сила атаки"]
        if not self.filters.get("attack_m"):
            filtered = [r for r in filtered if r.property1 != "Сила заклинаний"]
        if not self.filters.get("attack_o"):
            filtered = [r for r in filtered if r.property1 != "Обычный"]

        self._filtered_records = filtered
        self.endResetModel()
