from PySide6.QtCore import QSettings, QTimer, QTranslator
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from core.actions import connect_actions
from core.config import (
    APP_NAME,
    COMPANY_NAME,
    FILTER_PLUGIN_PATH,
    RESOURCE_PATH,
)
from core.filter_plugins import load_filter_definitions
from core.logger import setup_logger
from core.ui import setup_font
from gui.windows.main_window import MainWindow


class Application(QApplication):
    def __init__(self, argv, debug_mode: bool = False):
        super().__init__(argv)
        self.debug_mode = debug_mode

        self.setOrganizationName(COMPANY_NAME)
        self.setApplicationName(APP_NAME)

        self.logger = setup_logger(debug_mode=debug_mode)
        if self.debug_mode:
            self.logger.debug("Режим отладки включён.")

        self.logger.info("Инициализация настроек.")
        self.settings = QSettings()

        self.logger.info("Загрузка встроенных фильтров.")
        self.filter_definitions = load_filter_definitions(FILTER_PLUGIN_PATH, self.logger)

        self.logger.info("Инициализация перевода.")
        self.translator = QTranslator(self)
        translation_path = RESOURCE_PATH / "qtbase_ru.qm"
        if self.translator.load(str(translation_path)):
            self.installTranslator(self.translator)
        else:
            self.logger.warning("Не удалось загрузить перевод Qt: %s", translation_path)

        self.logger.info("Загрузка интерфейса.")
        self.window = MainWindow(self)
        self.window.setWindowTitle("Калькулятор урона")
        if self.debug_mode:
            self.window.setWindowTitle(f"{self.window.windowTitle()} [DEBUG]")
        self.window.setWindowIcon(QIcon(str(RESOURCE_PATH / "DamageViewer.ico")))

        self.logger.info("Настройка внешнего вида.")
        self.setStyle("Fusion")
        setup_font(self)

        self.logger.info("Подключение сигналов.")
        connect_actions(self)

        self.logger.info("Отображение главного окна.")
        self.window.showMaximized()
        QTimer.singleShot(0, self.window.auto_resize_columns)
