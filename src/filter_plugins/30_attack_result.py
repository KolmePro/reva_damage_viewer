FILTERS = [
    {
        "key": "attack_common",
        "label": "Обычные атаки",
        "group": "Результат удара",
        "match_all": [
            {"field": "property2", "value": "Обычный"},
        ],
    },
    {
        "key": "attack_critical",
        "label": "Критические удары",
        "group": "Результат удара",
        "match_all": [
            {"field": "property2", "value": "Критический удар"},
        ],
    },
    {
        "key": "attack_block",
        "label": "Блокирования",
        "group": "Результат удара",
        "match_all": [
            {"field": "property2", "value": "Блокирование"},
        ],
    },
    {
        "key": "attack_combo",
        "label": "Комбо-удары",
        "group": "Результат удара",
        "match_all": [
            {"field": "property2", "value": "Комбо-удар"},
        ],
    },
    {
        "key": "attack_dodge",
        "label": "Уклонения",
        "group": "Результат удара",
        "match_all": [
            {"field": "property2", "operator": "startswith", "value": "Вероятность уклонения"},
        ],
    },
]
