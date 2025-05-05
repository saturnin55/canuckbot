from datetime import date
from typing import List

from CanuckBot import CanuckBotBase
from CanuckBot.types import TimeZone, Handle


class Team(CanuckBotBase):
    team_id: int
    name: str
    shortname = Handle
    tz: TimeZone
    created_at: date
    aliases: List[str]
