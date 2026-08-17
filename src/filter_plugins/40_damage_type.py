FILTERS = [
    {
        "key": "attack_p",
        "label": "Сила атаки",
        "group": "Тип урона",
        "match_all": [
            {"field": "property1", "value": "РЎРёР»Р° Р°С‚Р°РєРё"},
        ],
    },
    {
        "key": "attack_m",
        "label": "Сила заклинаний",
        "group": "Тип урона",
        "match_all": [
            {"field": "property1", "value": "РЎРёР»Р° Р·Р°РєР»РёРЅР°РЅРёР№"},
        ],
    },
    {
        "key": "attack_o",
        "label": "Обычный",
        "group": "Тип урона",
        "match_all": [
            {"field": "property1", "value": "РћР±С‹С‡РЅС‹Р№"},
        ],
    },
]
