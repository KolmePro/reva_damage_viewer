from pathlib import Path

from PySide6.QtWidgets import QMessageBox, QFileDialog, QTableView, QAbstractItemView

from core.parser.event_log import EventLog


def connect_actions(app):
    ui = app.window.ui
    model = ui.damage_table_view.model()

    ui.action_set_game_folder.triggered.connect(lambda: handle_set_game_folder(app))
    ui.action_load_last_log.triggered.connect(lambda: handle_load_last_log(app))
    ui.action_clear_selection.triggered.connect(lambda: handle_clear_selection(app))

    ui.cb_outgoing_spirit_damage.toggled.connect(
        lambda checked: model.set_filter("outgoing_spirit_damage", checked)
    )
    ui.cb_incoming_spirit_damage.toggled.connect(
        lambda checked: model.set_filter("incoming_spirit_damage", checked)
    )

    ui.cb_attack_common.toggled.connect(
        lambda checked: model.set_filter("cattack_common", checked)
    )
    ui.cb_attack_critical.toggled.connect(
        lambda checked: model.set_filter("attack_critical", checked)
    )
    ui.cb_attack_block.toggled.connect(
        lambda checked: model.set_filter("attack_block", checked)
    )
    ui.cb_attack_combo.toggled.connect(
        lambda checked: model.set_filter("attack_combo", checked)
    )

    ui.cb_attack_p.toggled.connect(
        lambda checked: model.set_filter("attack_p", checked)
    )
    ui.cb_attack_m.toggled.connect(
        lambda checked: model.set_filter("attack_m", checked)
    )
    ui.cb_attack_o.toggled.connect(
        lambda checked: model.set_filter("attack_o", checked)
    )


def handle_set_game_folder(app):
    start_dir = app.settings.value("game_folder", "")

    folder = QFileDialog.getExistingDirectory(
        app.window,
        "Выберите папку с игрой",
        start_dir,
        QFileDialog.Option.ShowDirsOnly
    )
    if folder:
        app.settings.setValue("game_folder", folder)
        app.window.statusBar().showMessage(f"Папка игры установлена: {folder}", 5000)


def handle_load_last_log(app):
    """Загрузка последнего лога боя."""
    game_folder = app.settings.value("game_folder", "")
    chat_path = Path(game_folder) / "game" / "chat"

    if not chat_path.exists() or not chat_path.is_dir():
        QMessageBox.warning(app.window, "Ошибка", "Папка с игрой не выбрана или в ней нет логов!")
        return

    log_files = list(chat_path.glob("chat_*.html"))
    if not log_files:
        QMessageBox.warning(app.window, "Ошибка", "В папке с игрой нет логов боя!")
        return

    last_log = max(log_files, key=lambda f: f.stat().st_mtime)

    combat_log = EventLog.parse_chat(last_log)
    table = app.window.ui.damage_table_view
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.model().set_records(combat_log)
    table.verticalHeader().setVisible(False)
    auto_resize_columns(table)


def handle_clear_selection(app):
    """Снять выделение со всех строчек урона."""
    table = app.window.ui.damage_table_view
    table.clearSelection()


def auto_resize_columns(tv: QTableView):
    model = tv.model()
    n_cols = model.columnCount()
    header = tv.horizontalHeader()

    # Подгоняем под содержимое
    header.setStretchLastSection(False)
    tv.resizeColumnsToContents()

    # Вычисляем лишнее место
    total_width = tv.viewport().width()
    used_width = sum(tv.columnWidth(col) for col in range(n_cols))
    extra = max(0, total_width - used_width)

    # Равномерно распределяем лишнее место
    if extra > 0:
        extra_per_col = extra // (n_cols - 1)
        for col in range(1, n_cols - 1):
            tv.setColumnWidth(col, tv.columnWidth(col) + extra_per_col)

    header.setStretchLastSection(True)
