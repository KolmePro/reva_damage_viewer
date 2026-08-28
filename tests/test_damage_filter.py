import sys
import logging
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication, QMainWindow as QtMainWindow


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.actions import connect_actions
from core.filter_plugins import load_filter_definitions
from core.parser.table_view_model import DamageTableModel
from gui.compiled_ui.ui_main_window import Ui_MainWindow
from gui.windows.main_window import MainWindow


def make_record(damage: int, record_type: str = "damage_dealt"):
    return SimpleNamespace(
        type=record_type,
        attacker="Атакующий",
        target="Цель",
        skill="Умение",
        damage=damage,
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

    def test_damage_filter_control_is_available(self):
        window = QtMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(window)

        self.assertEqual(ui.label_minimum_damage.text(), "От")
        self.assertEqual(ui.label_maximum_damage.text(), "До")
        self.assertEqual(ui.le_minimum_damage.text(), "")
        self.assertEqual(ui.le_maximum_damage.text(), "")
        self.assertEqual(ui.damage_range_group.title(), "Диапазон урона")

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
            self.assertIsNotNone(window.ui.le_minimum_damage.validator())
            self.assertIsNotNone(window.ui.le_maximum_damage.validator())
            self.assertTrue(window.ui.btn_reset_damage_range.autoRaise())
            self.assertFalse(window.ui.btn_reset_damage_range.icon().isNull())
            self.assertEqual(window.ui.btn_reset_damage_range.text(), "")

            window.ui.le_minimum_damage.setText("10000")
            window.ui.le_maximum_damage.setText("20000")
            self.assertEqual(window.ui.damage_table_view.model().minimum_damage, 10_000)
            self.assertEqual(window.ui.damage_table_view.model().maximum_damage, 20_000)

            window.ui.btn_reset_damage_range.click()

            self.assertEqual(window.ui.le_minimum_damage.text(), "")
            self.assertEqual(window.ui.le_maximum_damage.text(), "")
            self.assertEqual(window.ui.damage_table_view.model().minimum_damage, 0)
            self.assertEqual(window.ui.damage_table_view.model().maximum_damage, 0)
            window.close()


if __name__ == "__main__":
    unittest.main()
