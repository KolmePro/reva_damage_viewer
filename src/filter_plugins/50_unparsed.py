FILTERS = [
    {
        "key": "show_unparsed",
        "label": "Неразобранные записи",
        "group": "Прочее",
        "default_enabled": False,
        "description": "Показывать исходные строки в выбранном времени независимо от остальных фильтров.",
        "match_all": [{"field": "type", "value": "unparsed"}],
    },
]
