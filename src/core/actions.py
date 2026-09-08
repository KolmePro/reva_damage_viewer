def connect_actions(app):
    window = app.window
    ui = window.ui
    table = ui.damage_table_view

    ui.action_set_game_folder.triggered.connect(window.action_set_game_folder)
    ui.action_load_last_log.triggered.connect(window.action_load_last_log)
    ui.action_append_last_log.triggered.connect(window.action_append_last_log)
    ui.action_load_log_file.triggered.connect(window.action_load_log_file)
    ui.action_clear_selection.triggered.connect(window.action_clear_selection)
    ui.action_clear_timeline_selection.triggered.connect(window.reset_time_range)

    ui.le_your_nickname.textChanged.connect(window.on_player_name_changed)
    ui.le_attacker_name.textChanged.connect(window.on_attacker_name_changed)
    ui.le_target_name.textChanged.connect(window.on_target_name_changed)
    ui.le_skill_name.textChanged.connect(window.on_skill_name_changed)
    ui.te_start_time.valueChanged.connect(window.on_time_range_changed)
    ui.te_end_time.valueChanged.connect(window.on_time_range_changed)
    ui.btn_reset_time_range.clicked.connect(window.reset_time_range)
    ui.sb_combat_pause.valueChanged.connect(window.on_combat_pause_changed)
    ui.le_minimum_damage.textChanged.connect(window.on_minimum_damage_changed)
    ui.le_maximum_damage.textChanged.connect(window.on_maximum_damage_changed)
    ui.btn_reset_damage_range.clicked.connect(window.reset_damage_range)

    table.selectionModel().selectionChanged.connect(
        lambda selected, deselected: window.refresh_damage_summary()
    )
