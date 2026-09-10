FILTERS = [
    {
        "key": "your_skills",
        "label": "Ваши умения",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "value": "self_skill_used"},
        ],
    },
    {
        "key": "your_effects",
        "label": "Эффекты на вас",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "operator": "in", "value": ["effect_applied", "effect_removed", "self_effect_applied", "self_effect_removed"]},
            {"field": "target", "value": "$player_name"},
        ],
    },
    {
        "key": "not_your_effects",
        "label": "Эффекты на других",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "operator": "in", "value": ["effect_applied", "effect_removed", "self_effect_applied", "self_effect_removed"]},
            {"field": "target", "operator": "ne", "value": "$player_name"},
        ],
    },
]
