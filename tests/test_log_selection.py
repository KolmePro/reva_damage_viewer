import logging
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QFileDialog


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from gui.windows.main_window import MainWindow


class LogSelectionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        settings = QSettings(
            str(Path(self.temp_dir.name) / "settings.ini"),
            QSettings.Format.IniFormat,
        )
        app = SimpleNamespace(
            filter_definitions=[],
            settings=settings,
            logger=logging.getLogger("log-selection-test"),
            debug_mode=False,
        )
        self.window = MainWindow(app)

    def tearDown(self):
        self.window.close()
        self.temp_dir.cleanup()

    def test_choose_log_action_is_next_to_latest_log(self):
        actions = self.window.ui.toolbar.actions()
        latest_index = actions.index(self.window.ui.action_load_last_log)

        self.assertIs(actions[latest_index + 1], self.window.ui.action_load_log_file)
        self.assertFalse(self.window.ui.action_load_log_file.icon().isNull())
        self.assertEqual(self.window.ui.action_load_log_file.shortcut().toString(), "Ctrl+O")

    def test_choose_log_opens_game_log_folder_and_loads_selected_file(self):
        game_folder = Path(self.temp_dir.name) / "Revelation Online"
        chat_folder = game_folder / "game" / "chat"
        chat_folder.mkdir(parents=True)
        selected_log = chat_folder / "chat_2026-08-28.html"
        self.window.settings.setValue("game_folder", str(game_folder))
        self.window.settings.setValue("last_log_folder", self.temp_dir.name)

        with (
            patch.object(
                QFileDialog,
                "getOpenFileName",
                return_value=(str(selected_log), "Логи боя Revelation Online (chat_*.html)"),
            ) as file_dialog,
            patch.object(self.window, "_load_combat_log") as load_log,
        ):
            self.window.action_load_log_file()

        self.assertEqual(file_dialog.call_args.args[2], str(chat_folder))
        load_log.assert_called_once_with(selected_log)


if __name__ == "__main__":
    unittest.main()
