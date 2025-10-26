import sys
from pathlib import Path


APP_NAME = "RevaDamageCalculator"
COMPANY_NAME = "KolmePRO"

# Базовый путь для работы в exe и с исходниками.
if getattr(sys, "frozen", False):
    BASE_PATH = Path(sys._MEIPASS)
else:
    BASE_PATH = Path(__file__).parent.parent

# Путь для ресурсов
RESOURCE_PATH = BASE_PATH / 'resources'
