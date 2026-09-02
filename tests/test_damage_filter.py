import sys
import logging
import tempfile
import unittest
from datetime import datetime, time
from pathlib import Path
from types import SimpleNamespace

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QMainWindow as QtMainWindow, QTimeEdit


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.actions import connect_actions
from core.filter_plugins import load_filter_definitions
from core.parser.table_view_model import DamageTableModel
from gui.compiled_ui.ui_main_window import Ui_MainWindow
from gui.windows.main_window import MainWindow


def make_record(
    damage: int,
    record_type: str = "damage_dealt",
    record_time: time = time(12, 0, 0),
    timestamp: datetime | None = None,
):
    return SimpleNamespace(
        type=record_type,
        attacker="Атакующий",
        is_attacker_spirit=False,
        attacker_spirit_owner="",
        target="Цель",
        is_target_spirit=False,
        target_spirit_owner="",
        skill="Умение",
        effects=[],
        damage=damage,
        property1="Обычный",
        property2="",
        origin_string=f"record-{damage}",
        time=record_time,
        timestamp=timestamp,
    )


class DamageFilterTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_minimum_damage_is_strict(self):
        model = DamageTableModel()
        model.minimum_damage = 10_000
        model.set_records([make_record(10_000), make_record(10_001)])

        self.assertEqual(model.rowCount(), 1)
        self.assertEqual(model._filtered_records[0].damage, 10_001)

    def test_maximum_damage_is_strict(self):
        model = DamageTableModel()
        model.maximum_damage = 20_000
        model.set_records([
            make_record(0, "effect_applied"),
            make_record(19_999),
            make_record(20_000),
        ])

        self.assertEqual(model.rowCount(), 1)
        self.assertEqual(model._filtered_records[0].damage, 19_999)

    def test_damage_range_applies_both_thresholds(self):
        model = DamageTableModel()
        model.minimum_damage = 10_000
        model.maximum_damage = 20_000
        model.set_records([make_record(10_000), make_record(15_000), make_record(20_000)])

        self.assertEqual(model.rowCount(), 1)
        self.assertEqual(model._filtered_records[0].damage, 15_000)

    def test_zero_disables_damage_filter(self):
        model = DamageTableModel()
        model.minimum_damage = 0
        model.set_records([make_record(0, "effect_applied"), make_record(1)])

        self.assertEqual(model.rowCount(), 2)

    def test_manual_time_range_supports_interval_across_midnight(self):
        model = DamageTableModel()
        model.set_records([
            make_record(1, record_time=time(22, 0, 0)),
            make_record(2, record_time=time(23, 30, 0)),
            make_record(3, record_time=time(0, 30, 0)),
            make_record(4, record_time=time(2, 0, 0)),
        ])

        model.set_time_range(time(23, 0, 0), time(1, 0, 0))

        self.assertEqual([record.damage for record in model._filtered_records], [2, 3])

    def test_exact_timestamp_range_can_exclude_pause_boundaries(self):
        model = DamageTableModel()
        start = datetime(2026, 8, 29, 12, 0, 0)
        model.set_records([
            make_record(1, timestamp=start),
            make_record(2, timestamp=start.replace(second=10)),
            make_record(3, timestamp=start.replace(second=20)),
        ])

        model.set_timestamp_range(
            start,
            start.replace(second=20),
            include_start=False,
            include_end=False,
        )

        self.assertEqual([record.damage for record in model._filtered_records], [2])

    def test_multiple_timestamp_ranges_are_combined(self):
        model = DamageTableModel()
        start = datetime(2026, 8, 29, 12, 0, 0)
        model.set_records([
            make_record(1, timestamp=start),
            make_record(2, timestamp=start.replace(second=10)),
            make_record(3, timestamp=start.replace(second=20)),
        ])

        model.set_timestamp_ranges([
            (start, start, True, True),
            (start.replace(second=20), start.replace(second=20), True, True),
        ])

        self.assertEqual([record.damage for record in model._filtered_records], [1, 3])

    def test_damage_filter_control_is_available(self):
        window = QtMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(window)

        self.assertEqual(ui.label_minimum_damage.text(), "От")
        self.assertEqual(ui.label_maximum_damage.text(), "До")
        self.assertEqual(ui.le_minimum_damage.text(), "")
        self.assertEqual(ui.le_maximum_damage.text(), "")

        controls = (
            ui.label_minimum_damage,
            ui.le_minimum_damage,
            ui.label_maximum_damage,
            ui.le_maximum_damage,
            ui.btn_reset_damage_range,
        )
        positions = [
            ui.damage_range_layout.getItemPosition(ui.damage_range_layout.indexOf(control))[:2]
            for control in controls
        ]
        self.assertEqual(positions, [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)])
        self.assertEqual(ui.damage_range_group.title(), "Диапазон урона")
        self.assertEqual(ui.time_range_group.title(), "Временной отрезок")
        self.assertIsInstance(ui.te_start_time, QTimeEdit)
        self.assertIsInstance(ui.te_end_time, QTimeEdit)
        self.assertEqual(ui.te_start_time.displayFormat(), "HH:mm:ss")
        self.assertEqual(ui.te_end_time.displayFormat(), "HH:mm:ss")
        self.assertEqual(ui.te_start_time.lineEdit().placeholderText(), "00:00:00")
        self.assertEqual(ui.te_end_time.lineEdit().placeholderText(), "00:00:00")
        time_row = ui.gridLayout.getItemPosition(ui.gridLayout.indexOf(ui.time_range_group))[0]
        damage_row = ui.gridLayout.getItemPosition(ui.gridLayout.indexOf(ui.damage_range_group))[0]
        self.assertLess(time_row, damage_row)

    def test_damage_controls_are_not_collapsed_by_plugin_filters(self):
        definitions = load_filter_definitions(
            Path(__file__).resolve().parents[1] / "src" / "filter_plugins"
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            settings = QSettings(str(Path(temp_dir) / "settings.ini"), QSettings.Format.IniFormat)
            app = SimpleNamespace(
                filter_definitions=definitions,
                settings=settings,
                logger=logging.getLogger("damage-filter-test"),
                debug_mode=False,
            )
            window = MainWindow(app)
            app.window = window
            connect_actions(app)
            window.resize(1200, 835)
            window.show()
            self.app.processEvents()

            self.assertGreaterEqual(
                window.ui.le_minimum_damage.height(),
                window.ui.le_minimum_damage.minimumSizeHint().height(),
            )
            self.assertGreaterEqual(
                window.ui.le_maximum_damage.height(),
                window.ui.le_maximum_damage.minimumSizeHint().height(),
            )
            self.assertGreaterEqual(
                window.ui.te_start_time.height(),
                window.ui.te_start_time.minimumSizeHint().height(),
            )
            self.assertGreaterEqual(
                window.ui.te_end_time.height(),
                window.ui.te_end_time.minimumSizeHint().height(),
            )
            self.assertIsNotNone(window.ui.le_minimum_damage.validator())
            self.assertIsNotNone(window.ui.le_maximum_damage.validator())
            self.assertEqual(window.ui.te_start_time.displayFormat(), "HH:mm:ss")
            self.assertEqual(window.ui.te_end_time.displayFormat(), "HH:mm:ss")
            self.assertTrue(window.ui.btn_reset_damage_range.autoRaise())
            self.assertFalse(window.ui.btn_reset_damage_range.icon().isNull())
            self.assertEqual(window.ui.btn_reset_damage_range.text(), "")
            self.assertTrue(window.ui.btn_reset_time_range.autoRaise())
            self.assertFalse(window.ui.btn_reset_time_range.icon().isNull())
            self.assertEqual(window.ui.btn_reset_time_range.text(), "")

            window.ui.le_minimum_damage.setText("10000")
            window.ui.le_maximum_damage.setText("20000")
            self.assertEqual(window.ui.damage_table_view.model().minimum_damage, 10_000)
            self.assertEqual(window.ui.damage_table_view.model().maximum_damage, 20_000)

            window.ui.btn_reset_damage_range.click()

            self.assertEqual(window.ui.le_minimum_damage.text(), "")
            self.assertEqual(window.ui.le_maximum_damage.text(), "")
            self.assertEqual(window.ui.damage_table_view.model().minimum_damage, 0)
            self.assertEqual(window.ui.damage_table_view.model().maximum_damage, 0)

            window.ui.te_start_time.setValue(time(12, 0, 0))
            window.ui.te_end_time.setValue(time(12, 30, 0))
            self.assertEqual(window.ui.damage_table_view.model().start_time, time(12, 0, 0))
            self.assertEqual(window.ui.damage_table_view.model().end_time, time(12, 30, 0))

            window.ui.damage_table_view.model().set_records([
                make_record(1, record_time=time(11, 0, 0)),
                make_record(2, record_time=time(12, 15, 0)),
            ])
            self.assertEqual(window.ui.damage_table_view.model().rowCount(), 1)

            window.ui.btn_reset_time_range.click()

            self.assertEqual(window.ui.te_start_time.text(), "—")
            self.assertEqual(window.ui.te_end_time.text(), "—")
            self.assertIsNone(window.ui.te_start_time.value())
            self.assertIsNone(window.ui.te_end_time.value())
            self.assertIsNone(window.ui.damage_table_view.model().start_time)
            self.assertIsNone(window.ui.damage_table_view.model().end_time)
            self.assertEqual(window.ui.damage_table_view.model().rowCount(), 2)

            window.ui.te_start_time.setValue(time(12, 0, 0))
            window.ui.action_clear_timeline_selection.trigger()

            self.assertEqual(window.ui.te_start_time.text(), "—")
            self.assertIsNone(window.ui.te_start_time.value())
            self.assertIsNone(window.ui.damage_table_view.model().start_time)

            window.ui.te_start_time.setValue(time(0, 0, 0))
            self.assertEqual(window.ui.te_start_time.value(), time(0, 0, 0))
            self.assertEqual(window.ui.damage_table_view.model().start_time, time(0, 0, 0))
            window.close()


if __name__ == "__main__":
    unittest.main()
