FILTERS = [
    {
        "key": "attack_p",
        "label": "Сила атаки",
        "group": "Тип урона",
        "match_all": [
            {"field": "property1", "value": "Сила атаки"},
        ],
    },
    {
        "key": "attack_m",
        "label": "Сила заклинаний",
        "group": "Тип урона",
        "match_all": [
            {"field": "property1", "value": "Сила заклинаний"},
        ],
    },
    {
        "key": "attack_o",
        "label": "Обычный",
        "group": "Тип урона",
        "match_all": [
            {"field": "property1", "value": "Обычный"},
        ],
    },
]
