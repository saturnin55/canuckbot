from enum import Enum
from datetime import date
from typing import List
from CanuckBot import CanuckBotBase
from CanuckBot.types import TimeZone, Handle
from Discord.types import Snowflake


class TEAM_FIELDS_EDITABLE(str, Enum):
    name = "name"
    shortname = "shortname"
    tz = "tz"

class Team(CanuckBotBase):
    team_id: int
    name: str
    shortname = Handle
    tz: TimeZone
    aliases: List[str]
    created_by: Snowflake
    created_at: date
    lastmodified_by: Snowflake | None
    lastmodified_at: date | None
