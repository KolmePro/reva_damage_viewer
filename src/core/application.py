from PySide6.QtCore import QSettings, QTimer, QTranslator
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from core.actions import connect_actions
from core.config import (
    APP_NAME,
    COMPANY_NAME,
    DEFAULT_FILTER_PLUGIN_PATH,
    FILTER_PLUGIN_PATH,
    RESOURCE_PATH,
)
from core.filter_plugins import ensure_filter_plugin_dir, load_filter_definitions
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

        self.logger.info("Загрузка фильтр-плагинов.")
        ensure_filter_plugin_dir(FILTER_PLUGIN_PATH, DEFAULT_FILTER_PLUGIN_PATH)
        self.filter_definitions = load_filter_definitions(FILTER_PLUGIN_PATH, self.logger)

        self.logger.info("Инициализация перевода.")
        translator = QTranslator()
        translator.load(str(RESOURCE_PATH / "qtbase_ru.qm"))
        self.installTranslator(translator)

        self.logger.info("Загрузка интерфейса.")
        self.window = MainWindow(self)
        self.window.setWindowTitle("Калькулятор урона")
        self.window.setWindowIcon(QIcon(str(RESOURCE_PATH / "DamageViewer.ico")))

        self.logger.info("Настройка внешнего вида.")
        self.setStyle("Fusion")
        setup_font(self)

        self.logger.info("Подключение сигналов.")
        connect_actions(self)

        self.logger.info("Отображение главного окна.")
        self.window.showMaximized()
        QTimer.singleShot(0, self.window.auto_resize_columns)
