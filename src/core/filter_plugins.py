from __future__ import annotations

import importlib.util
import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any


@dataclass(frozen=True)
class FilterCondition:
    field: str
    operator: str
    value: Any = None


@dataclass(frozen=True)
class FilterDefinition:
    key: str
    label: str
    group: str
    default_enabled: bool
    conditions: tuple[FilterCondition, ...]
    source: str


def ensure_filter_plugin_dir(plugin_dir: Path, default_plugin_dir: Path) -> None:
    plugin_dir.mkdir(parents=True, exist_ok=True)
    if not default_plugin_dir.exists():
        return

    for default_file in default_plugin_dir.glob("*.py"):
        target_file = plugin_dir / default_file.name
        if not target_file.exists():
            shutil.copy2(default_file, target_file)


def load_filter_definitions(plugin_dir: Path, logger: logging.Logger | None = None) -> list[FilterDefinition]:
    definitions: list[FilterDefinition] = []
    seen_keys: set[str] = set()

    if not plugin_dir.exists():
        return definitions

    for plugin_file in sorted(plugin_dir.glob("*.py")):
        if plugin_file.name.startswith("_"):
            continue

        try:
            module = _load_module(plugin_file)
            raw_filters = getattr(module, "FILTERS", [])
            for raw_filter in raw_filters:
                definition = _normalize_filter_definition(raw_filter, plugin_file.name)
                if definition.key in seen_keys:
                    raise ValueError(f"Duplicate filter key: {definition.key}")
                seen_keys.add(definition.key)
                definitions.append(definition)
        except Exception as exc:
            if logger:
                logger.exception("Не удалось загрузить фильтр-плагин %s: %s", plugin_file, exc)

    return definitions


def _load_module(plugin_file: Path) -> ModuleType:
    module_name = f"filter_plugin_{plugin_file.stem}"
    spec = importlib.util.spec_from_file_location(module_name, plugin_file)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot create import spec for {plugin_file}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _normalize_filter_definition(raw_filter: dict[str, Any], source_name: str) -> FilterDefinition:
    key = raw_filter["key"]
    label = raw_filter["label"]
    group = raw_filter.get("group", "Прочее")
    default_enabled = raw_filter.get("default_enabled", True)
    raw_conditions = raw_filter.get("match_all", [])
    if not raw_conditions:
        raise ValueError(f"Filter '{key}' in {source_name} has no match_all conditions")

    conditions = tuple(_normalize_condition(raw_condition) for raw_condition in raw_conditions)
    return FilterDefinition(
        key=key,
        label=label,
        group=group,
        default_enabled=default_enabled,
        conditions=conditions,
        source=source_name,
    )


def _normalize_condition(raw_condition: dict[str, Any]) -> FilterCondition:
    field = raw_condition["field"]
    operator = raw_condition.get("operator", "eq")
    value = raw_condition.get("value")
    if operator not in {"eq", "ne", "in", "not_in", "startswith", "not_startswith"}:
        raise ValueError(f"Unsupported operator: {operator}")
    return FilterCondition(field=field, operator=operator, value=value)
