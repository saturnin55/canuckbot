from typing import List
from datetime import date
from . import CanuckBotBase
from .types import Handle
from .TimeZone import TimeZone


class Team(CanuckBotBase):
    team_id: int
    name: str
    shortname = Handle
    tz: TimeZone
    created_at: date
    aliases: List[str]
