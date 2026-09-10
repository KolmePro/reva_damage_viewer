FILTERS = [
    {
        "key": "incoming_healing",
        "label": "Входящее лечение",
        "group": "Эффекты",
        "alternative_group": "healing_direction",
        "match_all": [
            {"field": "type", "value": "resource_restored"},
            {"field": "resource", "value": "ОЗ"},
            {"field": "target", "value": "$player_name"},
        ],
    },
    {
        "key": "outgoing_healing",
        "label": "Исходящее лечение",
        "group": "Эффекты",
        "alternative_group": "healing_direction",
        "match_all": [
            {"field": "type", "value": "resource_restored"},
            {"field": "resource", "value": "ОЗ"},
            {"field": "attacker", "value": "$player_name"},
        ],
    },
    {
        "key": "other_healing",
        "label": "Лечение других",
        "group": "Эффекты",
        "alternative_group": "healing_direction",
        "match_all": [
            {"field": "type", "value": "resource_restored"},
            {"field": "resource", "value": "ОЗ"},
            {"field": "attacker", "operator": "ne", "value": "$player_name"},
            {"field": "target", "operator": "ne", "value": "$player_name"},
        ],
    },
    {
        "key": "mana_restored",  # Сохраняем настройки прежнего фильтра ОМ.
        "label": "Восстановление (прочее)",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "value": "resource_restored"},
            {"field": "resource", "operator": "ne", "value": "ОЗ"},
        ],
    },
    {
        "key": "your_skills",
        "label": "Ваши умения",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "operator": "in", "value": ["self_skill_used", "self_skill_used_targeted", "skill_used_targeted"]},
            {"field": "attacker", "value": "$player_name"},
        ],
    },
    {
        "key": "other_skills",
        "label": "Умения других",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "value": "skill_used_targeted"},
            {"field": "attacker", "operator": "ne", "value": "$player_name"},
        ],
    },
    {
        "key": "your_effects",
        "label": "Эффекты на вас",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "operator": "in", "value": ["effect_applied", "targeted_effect_applied", "effect_removed", "targeted_effect_removed", "self_effect_applied", "self_effect_removed"]},
            {"field": "target", "value": "$player_name"},
        ],
    },
    {
        "key": "not_your_effects",
        "label": "Эффекты на других",
        "group": "Эффекты",
        "match_all": [
            {"field": "type", "operator": "in", "value": ["effect_applied", "targeted_effect_applied", "effect_removed", "targeted_effect_removed", "self_effect_applied", "self_effect_removed"]},
            {"field": "target", "operator": "ne", "value": "$player_name"},
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
        "key": "vampirism",
        "label": "Вампиризм",
        "group": "Эффекты",
        "match_all": [{"field": "type", "value": "vampirism"}],
    },
    {
        "key": "combat_events",
        "label": "События боя",
        "group": "Эффекты",
        "description": "Смерть, возвращение в бой, убийство игрока и обмен местами.",
        "match_all": [
            {"field": "type", "operator": "in", "value": ["player_death", "player_revived", "player_kill", "position_swap"]},
        ],
    },
    {
        "key": "damage_reflected",
        "label": "Отражение урона",
        "group": "Эффекты",
        "match_all": [{"field": "type", "value": "damage_reflected"}],
    },
    {
        "key": "damage_converted_to_healing",
        "label": "Урон → лечение",
        "group": "Эффекты",
        "description": (
            "Атаки, превращённые в лечение изменённым эффектом, например призмой. "
            "Для отдельной статистики выделите эти записи или оставьте только их."
        ),
        "match_all": [{"field": "type", "value": "damage_converted_to_healing"}],
    },
]
