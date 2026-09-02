import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from PySide6.QtCore import QtMsgType, QStandardPaths

from core.config import APP_NAME

logger = logging.getLogger(APP_NAME)


def qt_message_handler(mode, context, message):
    if mode == QtMsgType.QtDebugMsg:
        logger.debug(message)
    elif mode == QtMsgType.QtInfoMsg:
        logger.info(message)
    elif mode == QtMsgType.QtWarningMsg:
        logger.warning(message)
    elif mode == QtMsgType.QtCriticalMsg:
        logger.error(message)
    elif mode == QtMsgType.QtFatalMsg:
        logger.critical(message)


def setup_logger(debug_mode: bool = False):
    # Каталог приложения по стандартам ОС
    app_dir = Path(
        QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    )
    log_dir = app_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    file_path = log_dir / "app.log"

    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)

    if not logger.handlers:
        # Ротация файла (5 МБ, 3 бэкапа)
        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=5*1024*1024,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        logger.addHandler(file_handler)

        # Консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        logger.addHandler(console_handler)

    for handler in logger.handlers:
        handler.setLevel(logging.DEBUG if debug_mode else logging.INFO)

    # qInstallMessageHandler(qt_message_handler)

    # Перехват необработанных исключений
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Позволяем прерывание клавиатурой
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical(
            "Необработанное исключение.",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    sys.excepthook = handle_exception

    return logger
