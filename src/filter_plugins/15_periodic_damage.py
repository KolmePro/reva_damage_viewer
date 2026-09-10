FILTERS = [
    {
        "key": "include_dots",
        "label": "Учитывать доты",
        "group": "Урон",
        "description": (
            "Доты — тикающий урон: Отравление, Кровотечение и т. д. "
            "Отключите, чтобы скрыть эти записи и исключить их из статистики."
        ),
        "default_enabled": True,
        "match_all": [{"field": "is_dot", "value": True}],
    },
]
