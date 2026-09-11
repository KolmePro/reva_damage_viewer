from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QHeaderView

from gui.compiled_ui.ui_skill_damage_dialog import Ui_SkillDamageDialog


class SkillDamageDialog(QDialog):
    def __init__(self, damage_by_skill: dict[str, int], parent=None):
        super().__init__(parent)
        self.ui = Ui_SkillDamageDialog()
        self.ui.setupUi(self)
        close_button = self.ui.button_box.button(QDialogButtonBox.StandardButton.Close)
        close_button.setText("Закрыть")
        # Keep Qt from focusing and highlighting the first table cell on opening.
        close_button.setFocus(Qt.FocusReason.OtherFocusReason)
        self.model = QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(["Умение", "Урон", "Доля урона, %"])
        self.model.setSortRole(Qt.ItemDataRole.UserRole)
        total = sum(damage_by_skill.values())
        for skill, damage in sorted(damage_by_skill.items()):
            name = skill or "Без указания умения"
            share = damage / total * 100 if total else 0.0
            items = []
            for column, (label, value) in enumerate((
                (name, name.casefold()),
                (f"{damage:,}".replace(",", " "), damage),
                (f"{share:.2f}", share),
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
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.ui.damage_table.sortByColumn(1, Qt.SortOrder.DescendingOrder)
        if damage_by_skill:
            formatted_total = f"{total:,}".replace(",", " ")
            self.ui.summary_label.setText(f"Всего урона: {formatted_total}")
