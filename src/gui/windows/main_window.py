from pathlib import Path
from statistics import median

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from core.filter_plugins import FilterDefinition
from core.parser.event_log import EventLog
from core.parser.table_view_model import DamageTableModel
from gui.compiled_ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    STATIC_FILTER_WIDGETS = [
        "cb_outgoing_your_damage",
        "cb_incoming_your_damage",
        "cb_outgoing_spirit_damage",
        "cb_incoming_spirit_damage",
        "cb_your_effects",
        "cb_not_your_effects",
        "cb_attack_common",
        "cb_attack_critical",
        "cb_attack_block",
        "cb_attack_combo",
        "cb_attack_p",
        "cb_attack_m",
        "cb_attack_o",
        "line_2",
        "line_3",
        "line_4",
        "line_7",
    ]

    def __init__(self, app):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        damage_model = DamageTableModel(app.filter_definitions)
        self.ui.damage_table_view.setModel(damage_model)
        damage_model.data_refreshed.connect(self.refresh_table)
        self.settings = app.settings
        self.filter_checkboxes: dict[str, QCheckBox] = {}
        self._setup_filter_panel(app.filter_definitions)

        player_name = self.settings.value("player_name", "")
        self.ui.le_your_nickname.setText(player_name)
        damage_model.player_name = player_name

    def action_set_game_folder(self):
        start_dir = self.settings.value("game_folder", "")

        folder = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку с игрой",
            start_dir,
            QFileDialog.Option.ShowDirsOnly,
        )
        if folder:
            self.settings.setValue("game_folder", folder)
            self.ui.statusbar.showMessage(f"Папка игры установлена: {folder}", 5000)

    def action_load_last_log(self):
        game_folder = self.settings.value("game_folder", "")
        chat_path = Path(game_folder) / "game" / "chat"

        if not chat_path.exists() or not chat_path.is_dir():
            QMessageBox.warning(self, "Ошибка", "Папка с игрой не выбрана или в ней нет логов!")
            return

        log_files = list(chat_path.glob("chat_*.html"))
        if not log_files:
            QMessageBox.warning(self, "Ошибка", "В папке с игрой нет логов боя!")
            return

        last_log = max(log_files, key=lambda file: file.stat().st_mtime)

        combat_log = EventLog.parse_chat(str(last_log))
        table = self.ui.damage_table_view
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.model().set_records(combat_log)
        table.verticalHeader().setVisible(False)
        self.refresh_table()

    def on_player_name_changed(self, new_player_name):
        self.ui.damage_table_view.model().player_name = new_player_name
        self.settings.setValue("player_name", new_player_name)
        self.ui.damage_table_view.model().apply_filters()

    def on_attacker_name_changed(self, new_attacker_name):
        self.ui.damage_table_view.model().attacker_name = new_attacker_name
        self.ui.damage_table_view.model().apply_filters()

    def on_target_name_changed(self, new_target_name):
        self.ui.damage_table_view.model().target_name = new_target_name
        self.ui.damage_table_view.model().apply_filters()

    def on_skill_name_changed(self, new_skill_name):
        self.ui.damage_table_view.model().skill_name = new_skill_name
        self.ui.damage_table_view.model().apply_filters()

    def refresh_table(self):
        self.apply_row_spans()
        self.auto_resize_columns()
        self.refresh_damage_summary()

    def _setup_filter_panel(self, filter_definitions: list[FilterDefinition]):
        filter_layout = self.ui.gridLayout

        for widget_name in self.STATIC_FILTER_WIDGETS:
            widget = getattr(self.ui, widget_name, None)
            if widget is None:
                continue
            filter_layout.removeWidget(widget)
            widget.hide()

        container = QWidget(self.ui.groupBox)
        container.setObjectName("dynamic_filters_container")
        container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(10)

        groups: dict[str, list[FilterDefinition]] = {}
        for definition in filter_definitions:
            groups.setdefault(definition.group, []).append(definition)

        for group_name, definitions in groups.items():
            title = QLabel(group_name, container)
            title.setStyleSheet("font-weight: 600;")
            container_layout.addWidget(title)

            grid = QGridLayout()
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(12)
            grid.setVerticalSpacing(6)

            for index, definition in enumerate(definitions):
                checkbox = QCheckBox(definition.label, container)
                checkbox.setChecked(definition.default_enabled)
                checkbox.toggled.connect(
                    lambda checked, key=definition.key: self.ui.damage_table_view.model().set_filter(key, checked)
                )
                self.filter_checkboxes[definition.key] = checkbox
                grid.addWidget(checkbox, index // 2, index % 2)

            container_layout.addLayout(grid)

            divider = QFrame(container)
            divider.setFrameShape(QFrame.Shape.HLine)
            divider.setFrameShadow(QFrame.Shadow.Sunken)
            container_layout.addWidget(divider)

        if container_layout.count():
            last_item = container_layout.takeAt(container_layout.count() - 1)
            if last_item.widget():
                last_item.widget().deleteLater()

        filter_layout.addWidget(container, 6, 0, 10, 2)

    def auto_resize_columns(self):
        table = self.ui.damage_table_view
        model = table.model()
        n_cols = model.columnCount()
        header = table.horizontalHeader()

        header.setStretchLastSection(False)
        table.resizeColumnsToContents()

        total_width = table.viewport().width()
        used_width = sum(table.columnWidth(col) for col in range(n_cols))
        extra = max(0, total_width - used_width)

        if extra > 0 and n_cols > 1:
            extra_per_col = extra // (n_cols - 1)
            for col in range(1, n_cols - 1):
                table.setColumnWidth(col, table.columnWidth(col) + extra_per_col)

        header.setStretchLastSection(True)

    def apply_row_spans(self):
        table: QTableView = self.ui.damage_table_view
        model = table.model()
        if not model:
            return

        for row in range(model.rowCount()):
            for col in range(model.columnCount()):
                table.setSpan(row, col, 1, 1)

        for row in range(model.rowCount()):
            record = model._filtered_records[row]
            if record.type in ("effect_applied", "effect_removed"):
                table.setSpan(row, 0, 1, model.columnCount())

    def action_clear_selection(self):
        self.ui.damage_table_view.clearSelection()

    def refresh_damage_summary(self):
        table = self.ui.damage_table_view
        model = table.model()

        indexes = table.selectionModel().selectedRows()
        if not indexes:
            indexes = [model.index(row, 0) for row in range(model.rowCount())]

        damages = []
        p_damages = []
        m_damages = []
        common_damages = []
        crit_damages = []
        for index in indexes:
            damage_index = model.index(index.row(), 6)
            property1 = model.index(index.row(), 7)
            property2 = model.index(index.row(), 8)
            value = model.data(damage_index, role=Qt.DisplayRole)
            damage_type_1 = model.data(property1, role=Qt.DisplayRole)
            damage_type_2 = model.data(property2, role=Qt.DisplayRole)
            if value is not None:
                damages.append(int(value))
                if damage_type_1 == "Сила атаки":
                    p_damages.append(int(value))
                elif damage_type_1 == "Сила заклинаний":
                    m_damages.append(int(value))
                elif damage_type_1 == "Обычный":
                    common_damages.append(int(value))

                if damage_type_2 == "Критический удар":
                    crit_damages.append(int(value))

        total_attacks = len(damages)
        critical_hits = len(crit_damages)
        crit_chance = (critical_hits / total_attacks * 100) if total_attacks else 0
        all_damage = sum(damages)
        avg = round(all_damage / total_attacks) if total_attacks else 0
        min_damage = min(damages) if damages else 0
        max_damage = max(damages) if damages else 0
        median_damage = round(median(damages)) if damages else 0

        self.ui.label_10.setText(f"{total_attacks:,}".replace(",", " "))
        self.ui.label_24.setText(f"{critical_hits} ({crit_chance:.1f}%)".replace(",", " "))
        self.ui.label_13.setText(f"{all_damage:,}".replace(",", " "))

        self.ui.label_15.setText(f"{sum(p_damages):,}".replace(",", " "))
        self.ui.label_18.setText(f"{sum(m_damages):,}".replace(",", " "))
        self.ui.label_19.setText(f"{sum(common_damages):,}".replace(",", " "))

        self.ui.label_4.setText(f"{min_damage:,}".replace(",", " "))
        self.ui.label_2.setText(f"{max_damage:,}".replace(",", " "))

        self.ui.label_6.setText(f"{avg:,}".replace(",", " "))
        self.ui.label_8.setText(f"{median_damage:,}".replace(",", " "))
