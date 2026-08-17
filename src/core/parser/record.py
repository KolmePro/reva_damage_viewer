import re
from dataclasses import dataclass
from datetime import datetime, time
from typing import List, Optional

LINE_REGEX = re.compile(r"\[(?P<time>.*?)\]\s(?P<message>.*)")
SPIRIT_OWNER_REGEX = re.compile(r"^(?P<owner>.+?):\s*дух\s+(?P<spirit>.+)$")

RECORD_TYPES = {
    "damage_dealt": re.compile(
        r"(?P<attacker>.*?):?(?! дух ) (использует|использовано) "
        r"умение:? \[?(?P<skill>.*?)\]?\. "
        r"(?P<target>.*?):(?! дух ) "
        r"получено (?P<damage>\d*) ед\. урона "
        r"\((?P<property1>.*), (?P<property2>.*)\)\."
    ),
    "damage_dealt_buffed": re.compile(
        r"^(?P<attacker>[^\[]*?)"
        r"(?:\[(?P<effects>.*?)\])?"
        r"\s*Использовать(?P<skill>.*?)для"
        r"(?P<target>.*?)(?:Вызванный|нанесено)"
        r"(?P<damage>\d+)Очко.*?\("
        r"(?P<property1>.*?)\)\s*Урон\s*\((?P<property2>.*?)\)"
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
    Класс представляет запись в боевом логе (нанесение урона / эффекты).
    """

    type: str
    attacker: str
    is_attacker_spirit: bool
    target: str
    is_target_spirit: bool
    skill: str
    damage: int
    property1: str
    property2: str
    effects: List[str]
    attacker_spirit_owner: str = ""
    target_spirit_owner: str = ""

    def __repr__(self):
        return (
            f"[{self.time}: {self.attacker} наносит {self.target} "
            f"{self.damage} урона ({self.skill}, {self.property1}, {self.property2})]"
        )

    @staticmethod
    def try_to_parse(string: str) -> Optional["DamageRecord"]:
        """
        Пытается распарсить строку в запись нанесения урона.
        Если не получается, возвращает None.
        """

        record = Record.from_string(string)
        for record_type, regex in RECORD_TYPES.items():
            match = re.search(regex, record.message)
            if not match:
                continue

            match_dict = match.groupdict()
            attacker_name, is_attacker_spirit, attacker_spirit_owner = DamageRecord._parse_actor_name(
                match_dict.get("attacker", "")
            )
            target_name, is_target_spirit, target_spirit_owner = DamageRecord._parse_actor_name(
                match_dict.get("target", "")
            )

            effects = []
            effects_str = match_dict.get("effects", "")
            if effects_str:
                effects_str = effects_str.strip("\"")
                effects = effects_str.split("\", \"")

            return DamageRecord(
                origin_string=record.origin_string,
                message=record.message,
                time=record.time,
                type=record_type,
                attacker=attacker_name,
                is_attacker_spirit=is_attacker_spirit,
                target=target_name,
                is_target_spirit=is_target_spirit,
                skill=match_dict.get("skill", ""),
                damage=int(match_dict.get("damage", 0)),
                property1=match_dict.get("property1", ""),
                property2=match_dict.get("property2", ""),
                effects=effects,
                attacker_spirit_owner=attacker_spirit_owner,
                target_spirit_owner=target_spirit_owner,
            )
        return None

    @staticmethod
    def _parse_actor_name(raw_name: str) -> tuple[str, bool, str]:
        if not raw_name:
            return "", False, ""

        match = re.match(SPIRIT_OWNER_REGEX, raw_name)
        if match:
            return match["spirit"], True, match["owner"]

        return raw_name, False, ""
