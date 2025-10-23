from pathlib import Path

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMessageBox, QFileDialog, QTableView, QHeaderView, QAbstractItemView, QCheckBox

from core.parser.event_log import EventLog
from core.parser.table_view_model import DamageTableModel


def connect_actions(app):
    action = app.window.findChild(QAction, "action_set_game_folder")
    action.triggered.connect(lambda: handle_set_game_folder(app))

    action = app.window.findChild(QAction, "action_load_last_log")
    action.triggered.connect(lambda: handle_load_last_log(app))

    action = app.window.findChild(QAction, "action_clear_selection")
    action.triggered.connect(lambda: handle_clear_selection(app))

    app.window.findChild(QCheckBox, "cb_outgoing_spirit_damage").toggled.connect(
        lambda checked: handle_set_filter(app, checked, "outgoing_spirit_damage")
    )
    app.window.findChild(QCheckBox, "cb_incoming_spirit_damage").toggled.connect(
        lambda checked: handle_set_filter(app, checked, "incoming_spirit_damage")
    )

    app.window.findChild(QCheckBox, "cb_attack_common").toggled.connect(
        lambda checked: handle_set_filter(app, checked, "cattack_common")
    )
    app.window.findChild(QCheckBox, "cb_attack_critical").toggled.connect(
        lambda checked: handle_set_filter(app, checked, "attack_critical")
    )
    app.window.findChild(QCheckBox, "cb_attack_block").toggled.connect(
        lambda checked: handle_set_filter(app, checked, "attack_block")
    )
    app.window.findChild(QCheckBox, "cb_attack_combo").toggled.connect(
        lambda checked: handle_set_filter(app, checked, "attack_combo")
    )

    app.window.findChild(QCheckBox, "cb_attack_p").toggled.connect(
        lambda checked: handle_set_filter(app, checked, "attack_p")
    )
    app.window.findChild(QCheckBox, "cb_attack_m").toggled.connect(
        lambda checked: handle_set_filter(app, checked, "attack_m")
    )
    app.window.findChild(QCheckBox, "cb_attack_o").toggled.connect(
        lambda checked: handle_set_filter(app, checked, "attack_o")
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
        QMessageBox.warning(app.window, "Ошибка", "Папка с игрой не выбрана!")
        return

    log_files = list(chat_path.glob("chat_*.html"))
    if not log_files:
        QMessageBox.warning(app.window, "Ошибка", "В папке с игрой нет логов боя!")
        return

    last_log = max(log_files, key=lambda f: f.stat().st_mtime)

    combat_log = EventLog.parse_chat(last_log)
    model = DamageTableModel(combat_log)
    table = app.window.findChild(QTableView, "damage_table_view")
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setModel(model)
    table.verticalHeader().setVisible(False)
    auto_resize_columns(table)


def handle_clear_selection(app):
    """Снять выделение со всех строчек урона."""
    table = app.window.findChild(QTableView, "damage_table_view")
    table.clearSelection()


def handle_set_filter(app, checked, filter_name):
    table = app.window.findChild(QTableView, "damage_table_view")
    model = table.model()
    model.set_filter(filter_name, checked)
    model.apply_filters()


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
