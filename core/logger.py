import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from core.config import APP_NAME, LOG_DIR


def get_logger():
    log_dir = Path(LOG_DIR)
    log_dir.mkdir(exist_ok=True)

    file_path = log_dir / "app.log"

    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.INFO)

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

    # Перехват необработанных исключений
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Позволяем прерывание клавиатурой
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("ОШИБКА:", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = handle_exception

    return logger
