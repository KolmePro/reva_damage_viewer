from PySide6.QtCore import QSettings, QTranslator
from PySide6.QtGui import QFontDatabase, QFont, QIcon
from PySide6.QtWidgets import QApplication, QTableView

from core.actions import connect_actions
from core.config import APP_NAME, COMPANY_NAME, RESOURCE_PATH
from core.logger import get_logger
from core.ui import load_ui


class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.logger = get_logger()
        self.logger.info("Запуск приложения.")

        # Стиль
        self.setStyle("Fusion")

        # Перевод
        translator = QTranslator()
        translator.load(str(RESOURCE_PATH / "qtbase_ru.qm"))
        self.installTranslator(translator)

        # Настройки
        self.logger.info("Инициализация настроек.")
        self.settings = QSettings(COMPANY_NAME, APP_NAME)

        # Главное окно
        self.logger.info("Загрузка интерфейса.")
        self.window = load_ui(RESOURCE_PATH / "main_window.ui")
        self.window.setWindowTitle(APP_NAME)

        # Шрифт
        table = self.window.findChild(QTableView, "damage_table_view")
        font_id = QFontDatabase.addApplicationFont(str(RESOURCE_PATH / "roboto.ttf"))
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                font = QFont(families[0], 12)
                self.setFont(font)
        font_id = QFontDatabase.addApplicationFont(str(RESOURCE_PATH / "roboto_mono.ttf"))
        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            if families:
                font = QFont(families[0], 12)
                table.setFont(font)

        # Подключение сигналов
        connect_actions(self)

        # Отображение главного окна
        self.window.showMaximized()
