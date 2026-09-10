import sys
from pathlib import Path


APP_NAME = "RevaDamageCalculator"
COMPANY_NAME = "KolmePRO"

if getattr(sys, "frozen", False):
    BUNDLED_PATH = Path(sys._MEIPASS)
    BASE_PATH = Path(sys.executable).resolve().parent
else:
    BUNDLED_PATH = Path(__file__).parent.parent
    BASE_PATH = Path(__file__).parent.parent

RESOURCE_PATH = BUNDLED_PATH / "resources"
FILTER_PLUGIN_PATH = BUNDLED_PATH / "filter_plugins"
