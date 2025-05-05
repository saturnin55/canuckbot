from datetime import date
from typing import List

from CanuckBot import CanuckBotBase
from CanuckBot.TimeZone import TimeZone
from CanuckBot.types import Handle


class Team(CanuckBotBase):
    team_id: int
    name: str
    shortname = Handle
    tz: TimeZone
    created_at: date
    aliases: List[str]
