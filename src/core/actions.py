from pathlib import Path

from PySide6.QtWidgets import QMessageBox, QTableView, QAbstractItemView

from core.parser.event_log import EventLog


def connect_actions(app):
    window = app.window
    ui = window.ui
    table = ui.damage_table_view
    model = table.model()

    ui.action_set_game_folder.triggered.connect(window.action_set_game_folder)
    ui.action_load_last_log.triggered.connect(window.action_load_last_log)
    ui.action_clear_selection.triggered.connect(window.action_clear_selection)

    ui.le_your_nickname.textChanged.connect(window.on_player_name_changed)
    ui.le_attacker_name.textChanged.connect(window.on_attacker_name_changed)
    ui.le_target_name.textChanged.connect(window.on_target_name_changed)
    ui.le_skill_name.textChanged.connect(window.on_skill_name_changed)

    ui.cb_outgoing_your_damage.toggled.connect(
        lambda checked: model.set_filter("outgoing_your_damage", checked)
    )
    ui.cb_incoming_your_damage.toggled.connect(
        lambda checked: model.set_filter("incoming_your_damage", checked)
    )
    ui.cb_outgoing_spirit_damage.toggled.connect(
        lambda checked: model.set_filter("outgoing_spirit_damage", checked)
    )
    ui.cb_incoming_spirit_damage.toggled.connect(
        lambda checked: model.set_filter("incoming_spirit_damage", checked)
    )

    ui.cb_your_effects.toggled.connect(
        lambda checked: model.set_filter("your_effects", checked)
    )
    ui.cb_not_your_effects.toggled.connect(
        lambda checked: model.set_filter("not_your_effects", checked)
    )

    ui.cb_attack_common.toggled.connect(
        lambda checked: model.set_filter("attack_common", checked)
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

    table.selectionModel().selectionChanged.connect(
        lambda selected, deselected: window.refresh_damage_summary()
    )
