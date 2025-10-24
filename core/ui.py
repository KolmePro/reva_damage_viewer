from PySide6.QtCore import QFile
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QTableView

from core.config import RESOURCE_PATH


def load_ui(ui_path):
    """
    Загружает .ui файл и возвращает виджет (QMainWindow, QWidget и т.д.)
    """
    ui_file = QFile(ui_path)
    if not ui_file.open(QFile.OpenModeFlag.ReadOnly):
        raise FileNotFoundError(f"Не удалось открыть UI файл: {ui_path}")

    loader = QUiLoader()
    widget = loader.load(ui_file)
    ui_file.close()

    if widget is None:
        raise RuntimeError(f"Не удалось загрузить UI из файла: {ui_path}")

    return widget


def setup_font(app):
    table = app.window.findChild(QTableView, "damage_table_view")
    font_id = QFontDatabase.addApplicationFont(str(RESOURCE_PATH / "roboto.ttf"))
    if font_id != -1:
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            font = QFont(families[0], 12)
            app.setFont(font)
    font_id = QFontDatabase.addApplicationFont(str(RESOURCE_PATH / "roboto_mono.ttf"))
    if font_id != -1:
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            font = QFont(families[0], 12)
            table.setFont(font)
