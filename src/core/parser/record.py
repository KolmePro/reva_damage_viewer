import re
from dataclasses import dataclass
from datetime import time, datetime
from typing import Optional

LINE_REGEX = re.compile(r"\[(?P<time>.*?)\]\s(?P<message>.*)")
DAMAGE_DEALT_REGEX = re.compile(
    r"(?P<attacker>.*?):?(?! дух ) (использует|использовано) умение:? \[?(?P<skill>.*?)\]?\. (?P<target>.*?):(?! дух ) получено (?P<damage>\d*) ед\. урона \((?P<property1>.*), (?P<property2>.*)\)\."
)
RECORD_TYPES = {
    "damage_dealt": re.compile(
        r"(?P<attacker>.*?):?(?! дух ) (использует|использовано) умение:? \[?(?P<skill>.*?)\]?\. (?P<target>.*?):(?! дух ) получено (?P<damage>\d*) ед\. урона \((?P<property1>.*), (?P<property2>.*)\)\."
    ),
    "effect_applied": re.compile(r"(?P<target>.*?): действует эффект (?P<skill>.*?)\."),
    "effect_removed": re.compile(r"Эффект \[(?P<skill>.*?)\] больше не действует на объект \"(?P<target>.*?)\"\."),
}


@dataclass
class Record:
    """
    Класс представляет запись в боевом логе.
    """
    origin_string: str
    message: str
    time: time

    @staticmethod
    def from_string(string: str) -> "Record":
        match = re.search(LINE_REGEX, string)
        return Record(
            origin_string=string,
            message=match["message"],
            time=datetime.strptime(match["time"], "%H:%M:%S").time(),
        )


@dataclass
class DamageRecord(Record):
    """
    Класс представляет запись в боевом логе (Нанесение урона).
    """
    attacker: str
    is_attacker_spirit: bool
    target: str
    is_target_spirit: bool
    skill: str
    damage: int
    property1: str
    property2: str

    def __repr__(self):
        return f"[{self.time}: {self.attacker} наносит {self.target} {self.damage} урона ({self.skill}, {self.property1}, {self.property2})]"

    @staticmethod
    def try_to_parse(string: str) -> Optional["DamageRecord"]:
        """
        Пытается распарсить строку в запись Нанесение урона.
        Если не получается, возвращает None.
        """
        record = Record.from_string(string)
        match = re.search(DAMAGE_DEALT_REGEX, record.message)
        if not match:
            return None

        is_attacker_spirit = False
        attacker_name = match["attacker"]
        if attacker_name.startswith("Вы: дух "):
            is_attacker_spirit = True
            attacker_name = attacker_name.replace("Вы: дух ", "")

        is_target_spirit = False
        target_name = match["target"]
        if target_name.startswith("Вы: дух "):
            is_target_spirit = True
            target_name = target_name.replace("Вы: дух ", "")

        return DamageRecord(
            origin_string=record.origin_string,
            message=record.message,
            time=record.time,
            attacker=attacker_name,
            is_attacker_spirit=is_attacker_spirit,
            target=target_name,
            is_target_spirit=is_target_spirit,
            skill=match["skill"],
            damage=int(match["damage"]),
            property1=match["property1"],
            property2=match["property2"],
        )
