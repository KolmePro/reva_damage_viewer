from pathlib import Path
from statistics import median

from PySide6.QtCore import QItemSelection, Qt
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QAbstractItemView, QTableView

from core.parser.event_log import EventLog
from core.parser.table_view_model import DamageTableModel
from gui.compiled_ui.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.damage_table_view.setModel(DamageTableModel())
        self.settings = app.settings

    def action_set_game_folder(self):
        """Выбор папки с игрой."""
        start_dir = self.settings.value("game_folder", "")

        folder = QFileDialog.getExistingDirectory(
            self,
            "Выберите папку с игрой",
            start_dir,
            QFileDialog.Option.ShowDirsOnly
        )
        if folder:
            self.settings.setValue("game_folder", folder)
            self.ui.statusbar.showMessage(f"Папка игры установлена: {folder}", 5000)

    def action_load_last_log(self):
        """Загрузка последнего лога боя."""
        game_folder = self.settings.value("game_folder", "")
        chat_path = Path(game_folder) / "game" / "chat"

        if not chat_path.exists() or not chat_path.is_dir():
            QMessageBox.warning(self, "Ошибка", "Папка с игрой не выбрана или в ней нет логов!")
            return

        log_files = list(chat_path.glob("chat_*.html"))
        if not log_files:
            QMessageBox.warning(self, "Ошибка", "В папке с игрой нет логов боя!")
            return

        last_log = max(log_files, key=lambda f: f.stat().st_mtime)

        combat_log = EventLog.parse_chat(str(last_log))
        table = self.ui.damage_table_view
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.model().set_records(combat_log)
        table.verticalHeader().setVisible(False)
        self.auto_resize_columns()

    def auto_resize_columns(self):
        table = self.ui.damage_table_view
        model = table.model()
        n_cols = model.columnCount()
        header = table.horizontalHeader()

        # Подгоняем под содержимое
        header.setStretchLastSection(False)
        table.resizeColumnsToContents()

        # Вычисляем лишнее место
        total_width = table.viewport().width()
        used_width = sum(table.columnWidth(col) for col in range(n_cols))
        extra = max(0, total_width - used_width)

        # Равномерно распределяем лишнее место
        if extra > 0:
            extra_per_col = extra // (n_cols - 1)
            for col in range(1, n_cols - 1):
                table.setColumnWidth(col, table.columnWidth(col) + extra_per_col)

        header.setStretchLastSection(True)

    def action_clear_selection(self):
        """Снять выделение со всех строчек урона."""
        self.ui.damage_table_view.clearSelection()

    def refresh_damage_summary(self, selected: QItemSelection, deselected: QItemSelection):
        """Отобразить сводную информацию о выделенных записях."""
        indexes = self.ui.damage_table_view.selectionModel().selectedRows()  # получаем только строки
        model = self.ui.damage_table_view.model()

        damages = []
        for index in indexes:
            damage_index = model.index(index.row(), 6)  # колонка "Урон"
            value = model.data(damage_index, role=Qt.DisplayRole)
            if value is not None:
                try:
                    damages.append(int(value))
                except ValueError:
                    continue

        count = len(damages)
        avg = round(sum(damages) / count)
        min_damage = min(damages)
        max_damage = max(damages)
        median_damage = round(median(damages))

        self.ui.label_6.setText(f"{avg:,}".replace(",", " "))
        self.ui.label_10.setText(f"{count:,}".replace(",", " "))
        self.ui.label_4.setText(f"{min_damage:,}".replace(",", " "))
        self.ui.label_2.setText(f"{max_damage:,}".replace(",", " "))
        self.ui.label_8.setText(f"{median_damage:,}".replace(",", " "))