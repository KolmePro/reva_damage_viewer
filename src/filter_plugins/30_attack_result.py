FILTERS = [
    {
        "key": "attack_common",
        "label": "Обычные атаки",
        "group": "Результат удара",
        "match_all": [
            {"field": "property2", "value": "РћР±С‹С‡РЅС‹Р№"},
        ],
    },
    {
        "key": "attack_critical",
        "label": "Критические удары",
        "group": "Результат удара",
        "match_all": [
            {"field": "property2", "value": "РљСЂРёС‚РёС‡РµСЃРєРёР№ СѓРґР°СЂ"},
        ],
    },
    {
        "key": "attack_block",
        "label": "Блокирования",
        "group": "Результат удара",
        "match_all": [
            {"field": "property2", "value": "Р‘Р»РѕРєРёСЂРѕРІР°РЅРёРµ"},
        ],
    },
    {
        "key": "attack_combo",
        "label": "Комбо-удары",
        "group": "Результат удара",
        "match_all": [
            {"field": "property2", "value": "РљРѕРјР±Рѕ-СѓРґР°СЂ"},
        ],
    },
]
