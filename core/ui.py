from PySide6.QtGui import QPainter
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QRect
from PySide6.QtWidgets import QStyledItemDelegate


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
