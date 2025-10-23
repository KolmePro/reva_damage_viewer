import os
import sys
from pathlib import Path


APP_NAME = "Калькулятор урона"
COMPANY_NAME = "KolmePRO"

# Базовый путь для работы в exe и с исходниками.
if getattr(sys, "frozen", False):
    BASE_PATH = Path(sys._MEIPASS)
else:
    BASE_PATH = Path(__file__).parent.parent

# Путь для ресурсов
RESOURCE_PATH = BASE_PATH / 'resources'

# Папка AppData для текущего пользователя
APPDATA_DIR = Path(os.getenv("APPDATA")) / COMPANY_NAME / APP_NAME
APPDATA_DIR.mkdir(parents=True, exist_ok=True)

# Папка для логов
LOG_DIR = APPDATA_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Файл лога
LOG_FILE = LOG_DIR / "app.log"
