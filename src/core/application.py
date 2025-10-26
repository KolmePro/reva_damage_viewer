from PySide6.QtCore import QSettings, QTranslator
from PySide6.QtWidgets import QApplication

from core.actions import connect_actions
from core.config import APP_NAME, COMPANY_NAME, RESOURCE_PATH
from core.logger import setup_logger
from core.ui import setup_font
from gui.windows.main_window import MainWindow


class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.setOrganizationName(COMPANY_NAME)
        self.setApplicationName(APP_NAME)

        self.logger = setup_logger()

        self.logger.info("Инициализация настроек.")
        self.settings = QSettings()

        self.logger.info("Инициализация перевода.")
        translator = QTranslator()
        translator.load(str(RESOURCE_PATH / "qtbase_ru.qm"))
        self.installTranslator(translator)

        self.logger.info("Загрузка интерфейса.")
        self.window = MainWindow(self)
        self.window.setWindowTitle("Калькулятор урона")

        self.logger.info("Настройка внешнего вида.")
        self.setStyle("Fusion")
        setup_font(self)

        self.logger.info("Подключение сигналов.")
        connect_actions(self)

        self.logger.info("Отображение главного окна.")
        self.window.showMaximized()
