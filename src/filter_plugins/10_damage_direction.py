FILTERS = [
    {
        "key": "outgoing_your_damage",
        "label": "Урон от вас",
        "group": "Урон",
        "match_all": [
            {"field": "attacker", "value": "Вы"},
        ],
    },
    {
        "key": "incoming_your_damage",
        "label": "Урон по вам",
        "group": "Урон",
        "match_all": [
            {"field": "target", "value": "Вы"},
        ],
    },
    {
        "key": "outgoing_spirit_damage",
        "label": "Урон от духов",
        "group": "Урон",
        "match_all": [
            {"field": "is_attacker_spirit", "value": True},
        ],
    },
    {
        "key": "incoming_spirit_damage",
        "label": "Урон по духам",
        "group": "Урон",
        "match_all": [
            {"field": "is_target_spirit", "value": True},
        ],
    },
]
