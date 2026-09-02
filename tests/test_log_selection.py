import logging
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from PySide6.QtCore import QSettings, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QFileDialog


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.parser.event_log import EventLog
from gui.windows.main_window import MainWindow
from gui.widgets.combat_timeline import TimelineSection


def make_record(timestamp, origin_string, record_type="damage_dealt"):
    return SimpleNamespace(
        timestamp=timestamp,
        time=timestamp.time(),
        origin_string=origin_string,
        type=record_type,
        attacker="Атакующий",
        is_attacker_spirit=False,
        attacker_spirit_owner="",
        target="Цель",
        is_target_spirit=False,
        target_spirit_owner="",
        skill="Умение",
        effects=[],
        damage=100,
        property1="Обычный",
        property2="",
    )


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

    def test_log_actions_have_separate_load_and_append_modes(self):
        actions = self.window.ui.toolbar.actions()
        latest_index = actions.index(self.window.ui.action_load_last_log)

        self.assertIs(actions[latest_index + 1], self.window.ui.action_append_last_log)
        self.assertIs(actions[latest_index + 2], self.window.ui.action_load_log_file)
        self.assertIs(actions[latest_index + 3], self.window.ui.action_set_game_folder)
        self.assertNotIn(self.window.ui.action_clear_timeline_selection, actions)
        self.assertIs(
            self.window.timeline_reset_button.defaultAction(),
            self.window.ui.action_clear_timeline_selection,
        )
        self.assertFalse(self.window.ui.action_load_log_file.icon().isNull())
        self.assertFalse(self.window.ui.action_clear_timeline_selection.icon().isNull())
        self.assertEqual(
            self.window.ui.action_clear_timeline_selection.icon().cacheKey(),
            self.window.ui.btn_reset_damage_range.icon().cacheKey(),
        )
        self.assertEqual(self.window.ui.action_load_log_file.shortcut().toString(), "Ctrl+O")
        self.assertEqual(self.window.ui.action_append_last_log.shortcut().toString(), "Shift+F5")

    def test_choose_log_opens_game_log_folder_and_loads_selected_files(self):
        game_folder = Path(self.temp_dir.name) / "Revelation Online"
        chat_folder = game_folder / "game" / "chat"
        chat_folder.mkdir(parents=True)
        selected_logs = [
            chat_folder / "chat_2026-08-28.html",
            chat_folder / "chat_2026-08-29.html",
        ]
        self.window.settings.setValue("game_folder", str(game_folder))
        self.window.settings.setValue("last_log_folder", self.temp_dir.name)

        with (
            patch.object(
                QFileDialog,
                "getOpenFileNames",
                return_value=(
                    [str(log_path) for log_path in selected_logs],
                    "Логи боя Revelation Online (chat_*.html)",
                ),
            ) as file_dialog,
            patch.object(self.window, "_load_combat_logs") as load_logs,
        ):
            self.window.action_load_log_file()

        self.assertEqual(file_dialog.call_args.args[2], str(chat_folder))
        load_logs.assert_called_once_with(selected_logs)

    def test_append_latest_log_uses_append_mode(self):
        latest_log = Path(self.temp_dir.name) / "chat_2026-08-29.html"
        with (
            patch.object(self.window, "_find_latest_log", return_value=latest_log),
            patch.object(self.window, "_append_combat_logs") as append_logs,
        ):
            self.window.action_append_last_log()

        append_logs.assert_called_once_with([latest_log])

    def test_appending_log_adds_only_non_overlapping_records(self):
        from datetime import datetime, timedelta

        start = datetime(2026, 8, 28, 12, 0, 0)
        first_records = [
            make_record(start, "record-1"),
            make_record(start + timedelta(seconds=1), "record-2"),
        ]
        second_records = [
            make_record(start + timedelta(seconds=1), "record-2"),
            make_record(start + timedelta(seconds=2), "record-3"),
        ]
        first_path = Path(self.temp_dir.name) / "chat_2026-08-28.html"
        second_path = Path(self.temp_dir.name) / "chat_2026-08-29.html"

        with patch(
            "gui.windows.main_window.EventLog.parse_chat",
            return_value=EventLog(first_records),
        ):
            self.window._load_combat_logs([first_path])
        with patch(
            "gui.windows.main_window.EventLog.parse_chat",
            return_value=EventLog(second_records),
        ):
            self.window._append_combat_logs([second_path])

        self.assertEqual(
            [record.origin_string for record in self.window.combat_log],
            ["record-1", "record-2", "record-3"],
        )
        self.assertEqual(self.window.ui.damage_table_view.model().rowCount(), 3)

    def test_selecting_combat_section_filters_rows_and_populates_time_range(self):
        from datetime import datetime, timedelta

        start = datetime(2026, 8, 28, 12, 0, 0)
        records = [
            make_record(start + timedelta(seconds=index), f"record-{index}")
            for index in range(4)
        ]
        self.window.combat_log = EventLog(records)
        self.window.ui.damage_table_view.model().set_records(records)

        self.window.filter_timeline_sections([
            TimelineSection(
                "combat",
                start + timedelta(seconds=1),
                start + timedelta(seconds=2),
                0,
            )
        ])

        model = self.window.ui.damage_table_view.model()
        self.assertEqual(
            [record.origin_string for record in model._filtered_records],
            ["record-1", "record-2"],
        )
        self.assertEqual(self.window.ui.te_start_time.text(), "12:00:01")
        self.assertEqual(self.window.ui.te_end_time.text(), "12:00:02")
        self.assertEqual(self.window.ui.damage_table_view.selectionModel().selectedRows(), [])

    def test_selecting_pause_section_filters_out_neighboring_damage_records(self):
        from datetime import datetime, timedelta

        start = datetime(2026, 8, 28, 12, 0, 0)
        records = [
            make_record(start, "damage-1"),
            make_record(start + timedelta(seconds=10), "effect-1", "effect_applied"),
            make_record(start + timedelta(seconds=20), "effect-2", "effect_removed"),
            make_record(start + timedelta(seconds=40), "damage-2"),
        ]
        self.window.combat_log = EventLog(records)
        self.window.ui.damage_table_view.model().set_records(records)

        self.window.filter_timeline_sections([
            TimelineSection("gap", start, start + timedelta(seconds=40))
        ])

        model = self.window.ui.damage_table_view.model()
        self.assertEqual(
            [record.origin_string for record in model._filtered_records],
            ["effect-1", "effect-2"],
        )
        self.assertEqual(self.window.ui.te_start_time.text(), "12:00:00")
        self.assertEqual(self.window.ui.te_end_time.text(), "12:00:40")

    def test_clicking_pause_on_timeline_applies_pause_filter(self):
        from datetime import datetime, timedelta

        start = datetime(2026, 8, 28, 12, 0, 0)
        records = [
            make_record(start, "damage-1"),
            make_record(start + timedelta(seconds=10), "effect", "effect_applied"),
            make_record(start + timedelta(seconds=40), "damage-2"),
        ]
        log = EventLog(records)
        self.window.combat_log = log
        self.window.ui.damage_table_view.model().set_records(records)
        self.window.combat_timeline.set_segments(log.combat_segments())
        self.window.resize(1200, 835)
        self.window.show()
        self.app.processEvents()

        gap_rect = self.window.combat_timeline._hit_areas[1][0]
        QTest.mouseClick(
            self.window.combat_timeline,
            Qt.MouseButton.LeftButton,
            pos=gap_rect.center(),
        )

        model = self.window.ui.damage_table_view.model()
        self.assertEqual(
            [record.origin_string for record in model._filtered_records],
            ["effect"],
        )

    def test_timeline_supports_multiple_selection_and_toggle(self):
        from datetime import datetime, timedelta

        start = datetime(2026, 8, 28, 12, 0, 0)
        records = [
            make_record(start, "damage-1"),
            make_record(start + timedelta(seconds=10), "effect", "effect_applied"),
            make_record(start + timedelta(seconds=40), "damage-2"),
        ]
        log = EventLog(records)
        self.window.combat_log = log
        self.window.ui.damage_table_view.model().set_records(records)
        self.window.combat_timeline.set_segments(log.combat_segments())
        self.window.resize(1200, 835)
        self.window.show()
        self.app.processEvents()

        first_combat = self.window.combat_timeline._hit_areas[0][0].center()
        second_combat = self.window.combat_timeline._hit_areas[2][0].center()

        QTest.mouseClick(
            self.window.combat_timeline,
            Qt.MouseButton.LeftButton,
            pos=first_combat,
        )
        QTest.mouseClick(
            self.window.combat_timeline,
            Qt.MouseButton.LeftButton,
            pos=second_combat,
        )

        model = self.window.ui.damage_table_view.model()
        self.assertEqual(
            [record.origin_string for record in model._filtered_records],
            ["damage-1", "damage-2"],
        )
        self.assertEqual(self.window.ui.time_range_group.title(), "Временные отрезки: 2")
        self.assertEqual(self.window.ui.te_start_time.text(), "—")
        self.assertEqual(self.window.ui.te_end_time.text(), "—")
        self.assertIsNone(self.window.ui.te_start_time.value())
        self.assertIsNone(self.window.ui.te_end_time.value())

        QTest.mouseClick(
            self.window.combat_timeline,
            Qt.MouseButton.LeftButton,
            pos=first_combat,
        )

        self.assertEqual(
            [record.origin_string for record in model._filtered_records],
            ["damage-2"],
        )
        self.assertEqual(self.window.ui.te_start_time.text(), "12:00:40")

        QTest.mouseClick(
            self.window.combat_timeline,
            Qt.MouseButton.LeftButton,
            pos=second_combat,
        )

        self.assertEqual(model.rowCount(), 3)
        self.assertEqual(self.window.combat_timeline.selected_sections(), [])


if __name__ == "__main__":
    unittest.main()
