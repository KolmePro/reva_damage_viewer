FILTERS = [
    {
        "key": "outgoing_your_damage",
        "label": "Урон от вас",
        "group": "Урон",
        "match_all": [
            {"field": "type", "operator": "in", "value": ["damage_dealt", "damage_dealt_buffed", "damage_to_spirit"]},
            {"field": "attacker", "value": "Вы"},
        ],
    },
    {
        "key": "incoming_your_damage",
        "label": "Урон по вам",
        "group": "Урон",
        "match_all": [
            {"field": "type", "operator": "in", "value": ["damage_dealt", "damage_dealt_buffed", "damage_to_spirit"]},
            {"field": "target", "value": "Вы"},
            {"field": "is_target_spirit", "value": False},
        ],
    },
    {
        "key": "outgoing_spirit_damage",
        "label": "Урон от духов",
        "group": "Урон",
        "match_all": [
            {"field": "type", "operator": "in", "value": ["damage_dealt", "damage_dealt_buffed", "damage_to_spirit"]},
            {"field": "is_attacker_spirit", "value": True},
        ],
    },
    {
        "key": "incoming_spirit_damage",
        "label": "Урон по духам",
        "group": "Урон",
        "match_all": [
            {"field": "type", "operator": "in", "value": ["damage_dealt", "damage_dealt_buffed", "damage_to_spirit"]},
            {"field": "is_target_spirit", "value": True},
        ],
    },
]
