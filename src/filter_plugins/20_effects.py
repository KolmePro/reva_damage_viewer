FILTERS = [
    {
        "key": "health_restored",
        "label": "Восстановление ОЗ",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "value": "resource_restored"},
            {"field": "resource", "value": "ОЗ"},
        ],
    },
    {
        "key": "mana_restored",  # Сохраняем настройки прежнего фильтра ОМ.
        "label": "Восстановление (прочее)",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "value": "resource_restored"},
            {"field": "resource", "operator": "in", "value": ["ОМ", "Маневры"]},
        ],
    },
    {
        "key": "damage_absorbed",
        "label": "Поглощение урона",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "value": "damage_absorbed"},
        ],
    },
    {
        "key": "your_skills",
        "label": "Ваши умения",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "operator": "in", "value": ["self_skill_used", "self_skill_used_targeted"]},
        ],
    },
    {
        "key": "your_effects",
        "label": "Эффекты на вас",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "operator": "in", "value": ["effect_applied", "targeted_effect_applied", "effect_removed", "self_effect_applied", "self_effect_removed"]},
            {"field": "target", "value": "$player_name"},
        ],
    },
    {
        "key": "not_your_effects",
        "label": "Эффекты на других",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "operator": "in", "value": ["effect_applied", "targeted_effect_applied", "effect_removed", "self_effect_applied", "self_effect_removed"]},
            {"field": "target", "operator": "ne", "value": "$player_name"},
        ],
    },
]
