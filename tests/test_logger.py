import logging
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.logger import logger, setup_logger


class LoggerLocalizationTest(unittest.TestCase):
    def test_log_level_names_remain_standard(self):
        previous_handlers = list(logger.handlers)
        previous_excepthook = sys.excepthook
        for handler in previous_handlers:
            logger.removeHandler(handler)

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    with patch(
                        "core.logger.QStandardPaths.writableLocation",
                        return_value=temp_dir,
                    ):
                        setup_logger(debug_mode=True)

                    self.assertEqual(logging.getLevelName(logging.DEBUG), "DEBUG")
                    self.assertEqual(logging.getLevelName(logging.INFO), "INFO")
                    self.assertEqual(logging.getLevelName(logging.WARNING), "WARNING")
                    self.assertEqual(logging.getLevelName(logging.ERROR), "ERROR")
                    self.assertEqual(logging.getLevelName(logging.CRITICAL), "CRITICAL")
                finally:
                    for handler in list(logger.handlers):
                        logger.removeHandler(handler)
                        handler.close()
        finally:
            sys.excepthook = previous_excepthook
            for handler in previous_handlers:
                logger.addHandler(handler)


if __name__ == "__main__":
    unittest.main()
