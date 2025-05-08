from datetime import date
from typing import List
from CanuckBot import CanuckBotBase
from CanuckBot.types import TimeZone, Handle
from Discord.types import DiscordUserId


class Team(CanuckBotBase):
    team_id: int
    name: str
    shortname = Handle
    tz: TimeZone
    aliases: List[str]
    created_by: DiscordUserId
    created_at: date
    lastmodified_by: DiscordUserId | None
    lastmodified_at: date | None
