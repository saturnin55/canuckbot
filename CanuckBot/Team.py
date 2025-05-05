from datetime import date
from typing import List

from . import CanuckBotBase
from .TimeZone import TimeZone
from .types import Handle


class Team(CanuckBotBase):
    team_id: int
    name: str
    shortname = Handle
    tz: TimeZone
    created_at: date
    aliases: List[str]
