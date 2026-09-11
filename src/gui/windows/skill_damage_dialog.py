from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QHeaderView

from core.parser.event_log import SkillDamageStatistics
from gui.compiled_ui.ui_skill_damage_dialog import Ui_SkillDamageDialog


class SkillDamageDialog(QDialog):
    def __init__(self, statistics: dict[str, SkillDamageStatistics], parent=None):
        super().__init__(parent)
        self.ui = Ui_SkillDamageDialog()
        self.ui.setupUi(self)
        close_button = self.ui.button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setText("Закрыть")
        # Keep Qt from focusing and highlighting the first table cell on opening.
        close_button.setFocus(Qt.FocusReason.OtherFocusReason)
        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels([
            "Умение", "Урон", "Доля урона, %", "Атак", "Криты", "Промахи", "Средний урон",
        ])
        for column, tooltip in {
            3: "Число записей урона, включая промахи. Несколько целей или тиков считаются отдельными атаками.",
            4: "Количество критов и их доля среди всех атак умения. Сортировка по количеству.",
            5: "Количество промахов и их доля среди всех атак умения. Сортировка по количеству. "
               "Промах — результат «Вероятность уклонения» в логе; нулевой урон сам по себе не считается промахом.",
            6: "Суммарный урон / количество всех атак умения, включая промахи. Округлено до целого.",
        }.items():
            self.model.horizontalHeaderItem(column).setToolTip(tooltip)
        self.model.setSortRole(Qt.ItemDataRole.UserRole)
        totals = SkillDamageStatistics(
            damage=sum(stats.damage for stats in statistics.values()),
            attacks=sum(stats.attacks for stats in statistics.values()),
            critical_hits=sum(stats.critical_hits for stats in statistics.values()),
            misses=sum(stats.misses for stats in statistics.values()),
        )
        for skill, stats in sorted(statistics.items()):
            name = skill or "Без указания умения"
            share = stats.damage / totals.damage * 100 if totals.damage else 0.0
            items = []
            for column, (label, value) in enumerate((
                (name, name.casefold()),
                (f"{stats.damage:,}".replace(",", " "), stats.damage),
                (f"{share:.2f}", share),
                (f"{stats.attacks:,}".replace(",", " "), stats.attacks),
                (self._format_count_chance(stats.critical_hits, stats.critical_chance), stats.critical_hits),
                (self._format_count_chance(stats.misses, stats.miss_chance), stats.misses),
                (f"{stats.average_damage:,.0f}".replace(",", " "), stats.average_damage),
            )):
                item = QStandardItem(label)
                item.setData(value, Qt.ItemDataRole.UserRole)
                if column:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                items.append(item)
            self.model.appendRow(items)
        self.ui.damage_table.setModel(self.model)
        header = self.ui.damage_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for column in range(1, self.model.columnCount()):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)
        self.ui.damage_table.sortByColumn(1, Qt.SortOrder.DescendingOrder)
        self.ui.total_damage_value.setText(f"{totals.damage:,}".replace(",", " "))
        self.ui.total_attacks_value.setText(f"{totals.attacks:,}".replace(",", " "))
        self.ui.total_critical_value.setText(f"{totals.critical_hits:,}".replace(",", " "))
        self.ui.total_misses_value.setText(f"{totals.misses:,}".replace(",", " "))
        self.ui.total_average_value.setText(f"{totals.average_damage:,.0f}".replace(",", " "))
        self.ui.total_critical_detail.setText(f"{totals.critical_chance:.1f}% всех атак")
        self.ui.total_misses_detail.setText(f"{totals.miss_chance:.1f}% всех атак")
        if not statistics:
            self.ui.summary_label.setText("Итого по выборке — нет записей о нанесённом уроне")

    @staticmethod
    def _format_count_chance(count: int, chance: float) -> str:
        return f"{count:,} ({chance:.1f}%)".replace(",", " ")
