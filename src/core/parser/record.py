import re
from dataclasses import dataclass, field
from datetime import datetime, time
from typing import List, Optional

LINE_REGEX = re.compile(r"\[(?P<time>.*?)\]\s(?P<message>.*)")
SPIRIT_OWNER_REGEX = re.compile(r"^(?P<owner>.+?):\s*дух\s+(?P<spirit>.+)$")
COUNTER_ATTACK_SUFFIX_REGEX = re.compile(r"\s+\(Counter-attack \d+ layer\)$")

RECORD_TYPES = {
    "own_spirit_damage_short": re.compile(
        r"^(?P<attacker_owner>Вы) (?P<attacker>[^\s:]+) "
        r"(?P<target>[^\r\n]+?) (?P<damage>\d+)\s*$"
    ),
    "spirit_resource_transfer": re.compile(
        r"^(?P<attacker_owner>\S+) (?P<attacker>[^\r\n]+?) из-за (?P<skill>[^\r\n]+?) "
        r"получает (?P<restored_amount>\d+) оч\.\s+маневров, "
        r"а цель теряет (?P<drained_amount>\d+) оч\. (?P<drained_resource>ОМ)\.?\s*$"
    ),
    "turret_damage": re.compile(
        r'^\((?P<attacker>[^()\r\n]+)\) Турель использует прием "(?P<skill>[^"\r\n]+)"\. '
        r'(?P<target>[^\r\n]+?) получает (?P<damage>\d+) ед\. '
        r'\((?P<property1>[^()\r\n]+)\) урона \((?P<property2>[^()\r\n]+)\)\.?\s*$'
    ),
    "damage_reflected_to_player": re.compile(
        r"^(?P<attacker>[^\r\n]+?) отражает (?P<damage>\d+) ед\. урона игроку "
        r"(?P<target>[^\r\n]+?)\.\s*$"
    ),
    "damage_converted_to_healing": re.compile(
        r'^Измененный эффект: (?P<attacker>[^\r\n]+?) использует прием '
        r'"(?P<skill>[^"\r\n]+)" и восстанавливает '
        r'(?P<target>[^\r\n]+?)(?P<restored_amount>\d+) ед\. (?P<resource>ОЗ) '
        r'\((?P<property2>Критический удар|Обычный)\)\.?\s*$'
    ),
    "damage_reflected": re.compile(
        r"^(?P<attacker>\S+) отразили (?P<damage>\d+) пунктов повреждения на "
        r"(?P<target_owner>\S+) (?P<target>[^\r\n]+?)\.\s*$"
    ),
    "spirit_target_healing_localized": re.compile(
        r"^(?P<attacker>\S+) (?P<skill>[^\r\n]+?) "
        r"(?P<target_owner>Вы|[^\s:]+-[^\s:]+) (?P<target>[^:\r\n]+?)(?P<restored_amount>\d+) "
        r"(?P<resource>ОЗ) \((?P<property2>Критический удар|Обычный)\)\.?\s*$"
    ),
    "rage_restored": re.compile(
        r"^Уровень ярости повышается на (?P<restored_amount>\d+) ед\. "
        r"\((?P<resource>[^\r\n]+)\)\.?\s*$"
    ),
    "targeted_effect_removed": re.compile(
        r"^(?P<target>[^\r\n]+?): (?P<skill>[^:\r\n]+? \+\d+(?:\.\d+)?%?)\. "
        r"Эффект не действует\.\s*$"
    ),
    "player_death": re.compile(r"^(?P<target>Вы) погибаете\.\s*$"),
    "player_revived": re.compile(r"^(?P<target>Вы) снова в строю\.?\s*$"),
    "player_kill": re.compile(
        r"^(?P<attacker>Вы) убиваете игрока: (?P<target>[^\r\n]+?)\.?\s*$"
    ),
    "position_swap": re.compile(
        r'^(?P<attacker>[^\r\n]+?) применяет к цели \((?P<target>[^()\r\n]+)\) '
        r'умение "(?P<skill>[^"\r\n]+)"\. '
        r'(?P=attacker) и (?P=target) меняются местами\.\s*$'
    ),
    "vampirism_skill": re.compile(
        r"^(?P<attacker>[^\r\n]+?) использует: \[(?P<skill>[^\]\r\n]+)\] "
        r"и поглощает у \((?P<target>[^()\r\n]+)\) "
        r"(?P<restored_amount>\d+) ед\. здоровья\.?\s*$"
    ),
    "vampirism": re.compile(
        r"^(?P<attacker_owner>\S+) (?P<attacker>[^\r\n]+?) поглощенных "
        r"(?P<restored_amount>\d+) пунктов HP\.\s*$"
    ),
    "resource_restored": re.compile(
        r"^(?P<attacker>[^\r\n]+?): использован прием (?P<skill>[^\r\n]+?)\. "
        r"(?P<target>[^\r\n]+?): восстановлено (?P<restored_amount>\d+) (?:ед\. )?"
        r"(?P<resource>ОМ|ОЗ|Маневры) \((?P<property2>Критический удар|Обычный)\)\.?\s*$"
    ),
    "damage_absorbed": re.compile(
        r"^(?P<target>[^\r\n]+?): поглощение нанесенного противником "
        r"\((?P<attacker>[^\r\n]+?)\) урона в размере (?P<absorbed_damage>\d+) ед\.\s*$"
    ),
    "spirit_resource_restored_localized": re.compile(
        r"^(?P<attacker_owner>\S+) (?P<attacker>[^\r\n]+?) использовали "
        r"(?P<skill>[^\r\n]*?) для исцеления (?P<target>[^\r\n]+?) "
        r"(?P<restored_amount>\d+) очков\s+(?P<resource>ОЗ|ОМ|Маневры|маневров) "
        r"\((?P<property2>Критический удар|Обычный)\)\.?\s*$"
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
    "damage_dealt_buffed_localized": re.compile(
        r"^(?P<attacker>[^\[\r\n]+?)\[(?P<effects>[^\]\r\n]*)\]"
        r"\s*использовать(?P<skill>[^\r\n]+?)Вызвано\s*"
        r"(?P<target>[^\r\n]+?)(?P<damage>\d+)Очко\s*"
        r"\((?P<property1>[^()\r\n]+)\)\s*Урон\s*"
        r"\((?P<property2>[^()\r\n]+)\)\.?\s*$"
    ),
    "spirit_damage_localized": re.compile(
        r"^(?P<attacker_owner>\S+) (?P<attacker>[^\r\n]+?) использовал "
        r"(?P<skill>[^\r\n]+?) на (?P<target_owner>\S+) (?P<target>[^\r\n]+?) "
        r"для нанесения (?P<damage>\d+) пунктов "
        r"\((?P<property1>[^()\r\n]+)\) урона "
        r"\((?P<property2>[^()\r\n]+)\)\.?\s*$"
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
    drained_amount: int | None = None
    drained_resource: str = ""
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
            if record_type == "own_spirit_damage_short":
                record_type = "damage_dealt"
                match_dict["attacker"] = f"{match_dict['attacker_owner']}: дух {match_dict['attacker']}"
                match_dict["property1"] = "Обычный"
                match_dict["property2"] = "Обычный"
            if record_type == "spirit_resource_transfer":
                record_type = "resource_restored"
                match_dict["attacker"] = f"{match_dict['attacker_owner']}: дух {match_dict['attacker']}"
                match_dict["resource"] = "Маневры"
            if record_type == "turret_damage":
                record_type = "damage_dealt"
            if record_type == "damage_reflected":
                match_dict["target"] = f"{match_dict['target_owner']}: дух {match_dict['target']}"
            elif record_type == "damage_reflected_to_player":
                record_type = "damage_reflected"
            if record_type == "spirit_target_healing_localized":
                record_type = "resource_restored"
                match_dict["target"] = f"{match_dict['target_owner']}: дух {match_dict['target']}"
            if record_type == "rage_restored":
                record_type = "resource_restored"
                match_dict["target"] = "Вы"
            if record_type == "vampirism":
                match_dict["attacker"] = f"{match_dict['attacker_owner']}: дух {match_dict['attacker']}"
                match_dict["resource"] = "ОЗ"
            elif record_type == "vampirism_skill":
                record_type = "vampirism"
                match_dict["resource"] = "ОЗ"
            if record_type == "damage_dealt_buffed_localized":
                record_type = "damage_dealt_buffed"
            if record_type == "spirit_resource_restored_localized":
                record_type = "resource_restored"
                match_dict["attacker"] = f"{match_dict['attacker_owner']}: дух {match_dict['attacker']}"
                if match_dict["resource"] == "маневров":
                    match_dict["resource"] = "Маневры"
            if record_type == "spirit_damage_localized":
                record_type = "damage_dealt"
                for actor in ("attacker", "target"):
                    match_dict[actor] = f"{match_dict[f'{actor}_owner']}: дух {match_dict[actor]}"
            attacker = DamageRecord._parse_actor_name(match_dict.get("attacker", ""))
            default_target = "Вы" if record_type in ("self_effect_applied", "self_effect_removed") else ""
            target = DamageRecord._parse_actor_name(match_dict.get("target", default_target))
            if record_type in ("targeted_effect_applied", "targeted_effect_removed") and match_dict["target"].strip() != "Вы":
                target["is_spirit"] = True
                if not target["spirit_owner"]:
                    target["spirit_owner"] = "Вы"
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
                drained_amount=int(match_dict["drained_amount"]) if match_dict.get("drained_amount") is not None else None,
                drained_resource=match_dict.get("drained_resource", ""),
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
