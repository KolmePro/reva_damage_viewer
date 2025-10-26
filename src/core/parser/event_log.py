import codecs
import re
from collections import UserList
from datetime import time
from typing import List, Iterator

from .record import DamageRecord


class EventLog(UserList):
    """
    Лог событий.
    """

    def __init__(self, log: List[DamageRecord]):
        super().__init__()
        self.data: List[DamageRecord] = log.copy()

    def __iter__(self) -> Iterator[DamageRecord]:
        return iter(self.data)

    @staticmethod
    def parse_chat(log_path: str) -> "EventLog":
        """
        Парсит файл по заданному пути, возвращая лог событий.
        """
        line_regex = r'<font color = "#FF0000" \[Бой\]: </font>(.*?)<br>'

        events = []
        with codecs.open(log_path, "r", encoding="utf-8", errors="ignore") as file:
            log_file = file.read()
            combat_log = re.findall(line_regex, log_file)
            for string in combat_log:
                damage_record = DamageRecord.try_to_parse(string)
                if not damage_record:
                    continue
                events.append(damage_record)

        return EventLog(events)

    def get_time_slice(self, start: time, end: time) -> "EventLog":
        """
        Отфильтровывает из списка события по времени.
        """
        filtered_events = []
        for event in self._data:
            if start <= event.time <= end:
                filtered_events.append(event)

        return EventLog(filtered_events)

    def filter(
            self,
            attacker: str = None,
            is_attacker_spirit: bool = None,
            target: str = None,
            is_target_spirit: bool = None,
            skill: str = None,
            damage: int = None,
            property1: str = None,
            property2: str = None,
    ) -> "EventLog":
        """
        Отфильтровывает из списка события по условию.
        """
        filtered_events = []
        for event in self.data:
            if attacker is not None and event.attacker != attacker:
                continue
            if is_attacker_spirit is not None and event.is_attacker_spirit != is_attacker_spirit:
                continue
            if target is not None and event.target != target:
                continue
            if is_target_spirit is not None and event.is_target_spirit != is_target_spirit:
                continue
            if skill is not None and event.skill != skill:
                continue
            if damage is not None and event.damage != damage:
                continue
            if property1 is not None and event.property1 != property1:
                continue
            if property2 is not None and event.property2 != property2:
                continue
            filtered_events.append(event)

        return EventLog(filtered_events)
