from pathlib import Path
from statistics import median

from PySide6.QtCore import QSignalBlocker, Qt
from PySide6.QtGui import QAction, QIntValidator
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
    QStyle,
    QTableView,
    QTextEdit,
    QToolButton,
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
        self.ui.btn_reset_damage_range.setIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)
        )
        self.damage_value_validator = QIntValidator(0, 999_999_999, self)
        self.ui.le_minimum_damage.setValidator(self.damage_value_validator)
        self.ui.le_maximum_damage.setValidator(self.damage_value_validator)
        damage_model = DamageTableModel(app.filter_definitions)
        self.ui.damage_table_view.setModel(damage_model)
        damage_model.data_refreshed.connect(self.refresh_table)
        self.settings = app.settings
        self.logger = app.logger
        self.debug_mode = app.debug_mode
        self.last_unparsed_records: list[str] = []
        self.filter_checkboxes: dict[str, QCheckBox] = {}
        self.group_filter_keys: dict[str, list[str]] = {}
        self.filter_key_to_group: dict[str, str] = {}
        self.group_filter_checkboxes: dict[str, QCheckBox] = {}
        self._setup_filter_panel(app.filter_definitions)
        self._setup_debug_actions()

        player_name = self.settings.value("player_name", "")
        self.ui.le_your_nickname.setText(player_name)
        damage_model.player_name = player_name
        attacker_name = self.settings.value("attacker_name", "")
        target_name = self.settings.value("target_name", "")
        skill_name = self.settings.value("skill_name", "")
        minimum_damage = self.settings.value("minimum_damage", 0, type=int)
        maximum_damage = self.settings.value("maximum_damage", 0, type=int)
        self.ui.le_attacker_name.setText(attacker_name)
        self.ui.le_target_name.setText(target_name)
        self.ui.le_skill_name.setText(skill_name)
        self.ui.le_minimum_damage.setText(str(minimum_damage) if minimum_damage else "")
        self.ui.le_maximum_damage.setText(str(maximum_damage) if maximum_damage else "")
        damage_model.attacker_name = attacker_name
        damage_model.target_name = target_name
        damage_model.skill_name = skill_name
        damage_model.minimum_damage = minimum_damage
        damage_model.maximum_damage = maximum_damage

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

        combat_log = EventLog.parse_chat(str(last_log), collect_unparsed=self.debug_mode)
        self.last_unparsed_records = combat_log.unparsed_records
        if self.debug_mode:
            self.action_show_unparsed_log.setEnabled(bool(self.last_unparsed_records))
            self.logger.debug(
                "Loaded %s parsed and %s unparsed combat records from %s",
                len(combat_log),
                len(self.last_unparsed_records),
                last_log,
            )
        table = self.ui.damage_table_view
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.model().set_records(combat_log)
        table.verticalHeader().setVisible(False)
        self.refresh_table()
        if self.debug_mode:
            self.ui.statusbar.showMessage(
                f"Загружено: {len(combat_log)}; не распарсено: {len(self.last_unparsed_records)}",
                5000,
            )

    def on_player_name_changed(self, new_player_name):
        self.ui.damage_table_view.model().player_name = new_player_name
        self.settings.setValue("player_name", new_player_name)
        self.ui.damage_table_view.model().apply_filters()

    def on_attacker_name_changed(self, new_attacker_name):
        self.ui.damage_table_view.model().attacker_name = new_attacker_name
        self.settings.setValue("attacker_name", new_attacker_name)
        self.ui.damage_table_view.model().apply_filters()

    def on_target_name_changed(self, new_target_name):
        self.ui.damage_table_view.model().target_name = new_target_name
        self.settings.setValue("target_name", new_target_name)
        self.ui.damage_table_view.model().apply_filters()

    def on_skill_name_changed(self, new_skill_name):
        self.ui.damage_table_view.model().skill_name = new_skill_name
        self.settings.setValue("skill_name", new_skill_name)
        self.ui.damage_table_view.model().apply_filters()

    def on_minimum_damage_changed(self, text):
        minimum_damage = int(text) if text else 0
        self.ui.damage_table_view.model().minimum_damage = minimum_damage
        self.settings.setValue("minimum_damage", minimum_damage)
        self.ui.damage_table_view.model().apply_filters()

    def on_maximum_damage_changed(self, text):
        maximum_damage = int(text) if text else 0
        self.ui.damage_table_view.model().maximum_damage = maximum_damage
        self.settings.setValue("maximum_damage", maximum_damage)
        self.ui.damage_table_view.model().apply_filters()

    def reset_damage_range(self):
        with QSignalBlocker(self.ui.le_minimum_damage):
            self.ui.le_minimum_damage.clear()
        with QSignalBlocker(self.ui.le_maximum_damage):
            self.ui.le_maximum_damage.clear()

        model = self.ui.damage_table_view.model()
        model.minimum_damage = 0
        model.maximum_damage = 0
        self.settings.setValue("minimum_damage", 0)
        self.settings.setValue("maximum_damage", 0)
        model.apply_filters()

    def refresh_table(self):
        self.apply_row_spans()
        self.auto_resize_columns()
        self.refresh_damage_summary()

    def _setup_debug_actions(self):
        if not self.debug_mode:
            return

        self.action_show_unparsed_log = QAction("Нераспарсенные записи", self)
        self.action_show_unparsed_log.setToolTip("Показать записи боевого лога, которые не удалось распарсить")
        self.action_show_unparsed_log.setEnabled(False)
        self.action_show_unparsed_log.triggered.connect(self.show_unparsed_log_records)
        self.ui.toolbar.addAction(self.action_show_unparsed_log)

    def show_unparsed_log_records(self):
        if not self.last_unparsed_records:
            QMessageBox.information(self, "Debug", "Нераспарсенных записей нет.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Нераспарсенные записи боевого лога")
        dialog.resize(900, 600)

        layout = QVBoxLayout(dialog)
        text_edit = QTextEdit(dialog)
        text_edit.setReadOnly(True)
        text_edit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        text_edit.setPlainText("\n\n".join(self.last_unparsed_records))
        layout.addWidget(text_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, dialog)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec()

    def _setup_filter_panel(self, filter_definitions: list[FilterDefinition]):
        filter_layout = self.ui.gridLayout
        self.filter_checkboxes.clear()
        self.group_filter_keys.clear()
        self.filter_key_to_group.clear()
        self.group_filter_checkboxes.clear()

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

        saved_filter_states: dict[str, bool] = {}

        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(4)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(
            self._create_filter_button(
                "Включить все группы",
                lambda: self.set_all_filters(True),
                QStyle.StandardPixmap.SP_DialogApplyButton,
            )
        )
        toolbar_layout.addWidget(
            self._create_filter_button(
                "Выключить все группы",
                lambda: self.set_all_filters(False),
                QStyle.StandardPixmap.SP_DialogCancelButton,
            )
        )
        container_layout.addLayout(toolbar_layout)

        for group_name, definitions in groups.items():
            self.group_filter_keys[group_name] = [definition.key for definition in definitions]
            for definition in definitions:
                self.filter_key_to_group[definition.key] = group_name

            group_header = QHBoxLayout()
            group_header.setContentsMargins(0, 0, 0, 0)
            group_header.setSpacing(6)

            group_checkbox = self._create_tristate_filter_checkbox(group_name)
            group_checkbox.clicked.connect(lambda checked, group=group_name: self.set_filter_group(group, checked))
            self.group_filter_checkboxes[group_name] = group_checkbox
            group_header.addWidget(group_checkbox)
            group_header.addStretch()
            container_layout.addLayout(group_header)

            grid = QGridLayout()
            grid.setContentsMargins(0, 0, 0, 0)
            grid.setHorizontalSpacing(12)
            grid.setVerticalSpacing(6)

            for index, definition in enumerate(definitions):
                checkbox = QCheckBox(definition.label, container)
                enabled = self._load_filter_enabled(definition)
                saved_filter_states[definition.key] = enabled
                checkbox.setChecked(enabled)
                checkbox.toggled.connect(lambda checked, key=definition.key: self.on_filter_toggled(key, checked))
                self.filter_checkboxes[definition.key] = checkbox
                grid.addWidget(checkbox, index // 2, index % 2)

            container_layout.addLayout(grid)

            divider = QFrame(container)
            divider.setFrameShape(QFrame.Shape.HLine)
            divider.setFrameShadow(QFrame.Shadow.Sunken)
            container_layout.addWidget(divider)

        if groups and container_layout.count():
            last_item = container_layout.takeAt(container_layout.count() - 1)
            if last_item.widget():
                last_item.widget().deleteLater()

        scroll_area = QScrollArea(self.ui.groupBox)
        scroll_area.setObjectName("dynamic_filters_scroll_area")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        scroll_area.setWidget(container)

        self.ui.damage_range_group.setMinimumHeight(self.ui.damage_range_group.sizeHint().height())
        filter_layout.addWidget(scroll_area, 7, 0, 1, 2)
        filter_layout.setRowStretch(7, 1)
        self.ui.damage_table_view.model().set_filters(saved_filter_states)
        self.refresh_filter_group_states()

    def _create_tristate_filter_checkbox(self, text: str):
        checkbox = QCheckBox(text, self.ui.groupBox)
        checkbox.setTristate(True)
        checkbox.setStyleSheet("font-weight: 600;")
        return checkbox

    def _create_filter_button(self, tooltip: str, callback, icon):
        button = QToolButton(self.ui.groupBox)
        button.setIcon(self.style().standardIcon(icon))
        button.setToolTip(tooltip)
        button.setAutoRaise(True)
        button.clicked.connect(callback)
        return button

    def on_filter_toggled(self, key: str, enabled: bool):
        self._save_filter_enabled(key, enabled)
        self.ui.damage_table_view.model().set_filter(key, enabled)
        self.refresh_filter_group_states(self.filter_key_to_group.get(key))

    def set_all_filters(self, enabled: bool):
        self._set_filters(list(self.filter_checkboxes), enabled)

    def set_filter_group(self, group_name: str, enabled: bool):
        self._set_filters(self.group_filter_keys.get(group_name, []), enabled)

    def _set_filters(self, keys: list[str], enabled: bool):
        if not keys:
            return

        for key in keys:
            checkbox = self.filter_checkboxes.get(key)
            if checkbox is None:
                continue
            with QSignalBlocker(checkbox):
                checkbox.setChecked(enabled)

        self.ui.damage_table_view.model().set_filters({key: enabled for key in keys})
        for key in keys:
            self._save_filter_enabled(key, enabled)
        self.refresh_filter_group_states()

    def _filter_settings_key(self, key: str):
        return f"filters/{key}/enabled"

    def _load_filter_enabled(self, definition: FilterDefinition):
        value = self.settings.value(self._filter_settings_key(definition.key), definition.default_enabled)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in {"1", "true", "yes", "on"}
        return bool(value)

    def _save_filter_enabled(self, key: str, enabled: bool):
        self.settings.setValue(self._filter_settings_key(key), enabled)

    def refresh_filter_group_states(self, changed_group_name: str | None = None):
        group_names = [changed_group_name] if changed_group_name else list(self.group_filter_keys)

        for group_name in group_names:
            keys = self.group_filter_keys.get(group_name, [])
            group_checkbox = self.group_filter_checkboxes.get(group_name)
            if not keys or group_checkbox is None:
                continue
            self._set_filter_state_indicator(group_checkbox, keys)

    def _set_filter_state_indicator(self, checkbox: QCheckBox, keys: list[str]):
        enabled_count = sum(1 for key in keys if self.filter_checkboxes[key].isChecked())
        if enabled_count == len(keys):
            state = Qt.CheckState.Checked
        elif enabled_count == 0:
            state = Qt.CheckState.Unchecked
        else:
            state = Qt.CheckState.PartiallyChecked

        with QSignalBlocker(checkbox):
            checkbox.setCheckState(state)

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
