import re
from dataclasses import dataclass, field
from datetime import datetime, time
from typing import List, Optional

LINE_REGEX = re.compile(r"\[(?P<time>.*?)\]\s(?P<message>.*)")
SPIRIT_OWNER_REGEX = re.compile(r"^(?P<owner>.+?):\s*дух\s+(?P<spirit>.+)$")
COUNTER_ATTACK_SUFFIX_REGEX = re.compile(r"\s+\(Counter-attack \d+ layer\)$")

RECORD_TYPES = {
    "resource_restored": re.compile(
        r"^(?P<attacker>[^\r\n]+?): использован прием (?P<skill>[^\r\n]+?)\. "
        r"(?P<target>[^\r\n]+?): восстановлено (?P<restored_amount>\d+) (?:ед\. )?"
        r"(?P<resource>ОМ|ОЗ|Маневры) \((?P<property2>Критический удар|Обычный)\)\.?\s*$"
    ),
    "damage_absorbed": re.compile(
        r"^(?P<target>[^\r\n]+?): поглощение нанесенного противником "
        r"\((?P<attacker>[^\r\n]+?)\) урона в размере (?P<absorbed_damage>\d+) ед\.\s*$"
    ),
    "damage_dealt": re.compile(
        r"(?P<attacker>.*?):?(?! дух ) "
        r"(?:использует|использовано) умение:? \[?(?P<skill>.*?)\]?\. "
        r"(?P<target>.*?):(?! дух ) "
        r"получено (?P<damage>\d*) ед\. урона "
        r"\((?P<property1>.*), (?P<property2>.*)\)\.?\s*$"
    ),
    "damage_to_spirit": re.compile(
        r"^(?P<attacker>[^\r\n]+?): использован прием (?P<skill>[^\r\n]+?)\. "
        r"(?P<target>[^\r\n]+?): получено (?P<damage>\d+) ед\. урона "
        r"\((?P<property1>[^,\r\n]+), (?P<property2>[^\r\n]+)\)\.?\s*$"
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
    "targeted_effect_applied": re.compile(
        r"^(?P<target>[^\r\n]+?): (?P<skill>[^:\r\n]+? \+\d+(?:\.\d+)?%? ед)\. Действует "
        r"(?:постоянно|(?P<duration_seconds>\d+) сек)\.$"
    ),
    "self_effect_applied": re.compile(
        r"^(?P<skill>[^:\r\n]+? \+\d+(?:\.\d+)?%? ед)\. Действует "
        r"(?:постоянно|(?P<duration_seconds>\d+) сек)\.$"
    ),
    "self_effect_removed": re.compile(
        r"^(?P<skill>[^:\r\n]+? \+\d+(?:\.\d+)?%?)\. Эффект не действует\.$"
    ),
    "self_skill_used": re.compile(
        r'^(?P<attacker>Вы): использовано умение "(?P<skill>[^"\r\n]+)"\s*$'
    ),
    "self_skill_used_targeted": re.compile(
        r'^Атакующий: (?P<attacker>Вы)\. Цель: (?P<target>[^\r\n]+?)\. '
        r'Использовано умение: "(?P<skill>[^"\r\n]+)"\s*$'
    ),
    "skill_used_targeted": re.compile(
        r'^Атакующий: (?P<attacker>[^\r\n]+?)\. Цель: (?P<target>[^\r\n]+?)\. '
        r'Использовано умение: "(?P<skill>[^"\r\n]+)"\s*$'
    ),
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
    attacker_server: str
    is_attacker_spirit: bool
    attacker_spirit_owner: str
    attacker_spirit_owner_server: str
    target: str
    target_server: str
    is_target_spirit: bool
    target_spirit_owner: str
    target_spirit_owner_server: str
    skill: str
    damage: int
    property1: str
    property2: str
    effects: List[str]
    timestamp: datetime | None = field(default=None, compare=False)
    duration_seconds: int | None = None  # Длительность, явно указанная в логе.
    absorbed_damage: int | None = None
    restored_amount: int | None = None
    resource: str = ""
    is_dot: bool = False

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
            match = regex.search(record.message)
            if not match:
                continue

            match_dict = match.groupdict()
            attacker = DamageRecord._parse_actor_name(match_dict.get("attacker", ""))
            default_target = "Вы" if record_type in ("self_effect_applied", "self_effect_removed") else ""
            target = DamageRecord._parse_actor_name(match_dict.get("target", default_target))
            is_dot = record_type == "damage_to_spirit"
            if is_dot:
                if match_dict["target"].strip() == "Вы":
                    record_type = "damage_dealt"
                else:
                    target["is_spirit"] = True
                    if not target["spirit_owner"]:
                        target["spirit_owner"] = "Вы"

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
                is_dot=is_dot,
                attacker=attacker["name"],
                attacker_server=attacker["server"],
                is_attacker_spirit=attacker["is_spirit"],
                attacker_spirit_owner=attacker["spirit_owner"],
                attacker_spirit_owner_server=attacker["spirit_owner_server"],
                target=target["name"],
                target_server=target["server"],
                is_target_spirit=target["is_spirit"],
                target_spirit_owner=target["spirit_owner"],
                target_spirit_owner_server=target["spirit_owner_server"],
                skill=match_dict.get("skill", ""),
                damage=int(match_dict.get("damage", 0)),
                property1=match_dict.get("property1", ""),
                property2=match_dict.get("property2", ""),
                effects=effects,
                restored_amount=(
                    int(match_dict["restored_amount"])
                    if match_dict.get("restored_amount") is not None
                    else None
                ),
                resource=match_dict.get("resource", ""),
                absorbed_damage=(
                    int(match_dict["absorbed_damage"])
                    if match_dict.get("absorbed_damage") is not None
                    else None
                ),
                duration_seconds=(
                    int(match_dict["duration_seconds"])
                    if match_dict.get("duration_seconds") is not None
                    else None
                ),
            )
        return None

    @staticmethod
    def _parse_actor_name(raw_name: str) -> dict[str, str | bool]:
        empty_result = {
            "name": "",
            "server": "",
            "is_spirit": False,
            "spirit_owner": "",
            "spirit_owner_server": "",
        }
        if not raw_name:
            return empty_result

        raw_name = DamageRecord._normalize_actor_name(raw_name)

        match = re.match(SPIRIT_OWNER_REGEX, raw_name)
        if match:
            spirit_name, spirit_server = DamageRecord._split_name_and_server(match["spirit"])
            owner_name, owner_server = DamageRecord._split_name_and_server(match["owner"])
            return {
                "name": spirit_name,
                "server": spirit_server,
                "is_spirit": True,
                "spirit_owner": owner_name,
                "spirit_owner_server": owner_server,
            }

        name, server = DamageRecord._split_name_and_server(raw_name)
        return {
            "name": name,
            "server": server,
            "is_spirit": False,
            "spirit_owner": "",
            "spirit_owner_server": "",
        }

    @staticmethod
    def _split_name_and_server(raw_name: str) -> tuple[str, str]:
        if "-" not in raw_name:
            return raw_name, ""
        name, server = raw_name.rsplit("-", 1)
        return name, server

    @staticmethod
    def _normalize_actor_name(raw_name: str) -> str:
        return re.sub(COUNTER_ATTACK_SUFFIX_REGEX, "", raw_name).strip()
