from pathlib import Path

from PySide6.QtWidgets import QMessageBox, QTableView, QAbstractItemView

from core.parser.event_log import EventLog


def connect_actions(app):
    window = app.window
    ui = window.ui
    model = ui.damage_table_view.model()

    ui.action_set_game_folder.triggered.connect(window.action_set_game_folder)
    ui.action_load_last_log.triggered.connect(window.action_load_last_log)
    ui.action_clear_selection.triggered.connect(window.action_clear_selection)

    ui.cb_outgoing_spirit_damage.toggled.connect(
        lambda checked: model.set_filter("outgoing_spirit_damage", checked)
    )
    ui.cb_incoming_spirit_damage.toggled.connect(
        lambda checked: model.set_filter("incoming_spirit_damage", checked)
    )

    ui.cb_attack_common.toggled.connect(
        lambda checked: model.set_filter("cattack_common", checked)
    )
    ui.cb_attack_critical.toggled.connect(
        lambda checked: model.set_filter("attack_critical", checked)
    )
    ui.cb_attack_block.toggled.connect(
        lambda checked: model.set_filter("attack_block", checked)
    )
    ui.cb_attack_combo.toggled.connect(
        lambda checked: model.set_filter("attack_combo", checked)
    )

    ui.cb_attack_p.toggled.connect(
        lambda checked: model.set_filter("attack_p", checked)
    )
    ui.cb_attack_m.toggled.connect(
        lambda checked: model.set_filter("attack_m", checked)
    )
    ui.cb_attack_o.toggled.connect(
        lambda checked: model.set_filter("attack_o", checked)
    )
