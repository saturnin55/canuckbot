from enum import Enum
from datetime import datetime
from CanuckBot import CanuckBotBase
from CanuckBot.types import Match_Status, TimeZone
from Discord.types import Snowflake


class MATCH_FIELDS_EDITABLE(str, Enum):
    home_id = "home_id"
    away_id = "away_id"
    competition_id = "competition_id"
    status = "status"
    kickoff_at = "kickoff_at"
    tz = "tz"
    venue = "venue"
    description = "description"
    channel_id = "channel_id"
    hours_before_kickoff = "hours_before_kickoff"
    hours_after_kickoff = "hours_after_kickoff"
    watch = "watch"
    stream = "stream"

class Match(CanuckBotBase):
    match_id: int
    home_id: int
    away_id: int
    competition_id: int
    status: Match_Status
    kickoff_at: datetime
    tz: TimeZone
    venue: str
    description: str
    channel_id: Snowflake
    info_msg_id: Snowflake
    hours_before_kickoff: int
    hours_after_kickoff: int
    watch: str
    stream: HttpUrl
    created_by: Snowflake
    created_at: datetime
    lastmodified_by: Snowflake | None
    lastmodified_at: datetime | None

    async def generate_channel_topic:
        pass

    async def generate_channel_name:
        pass
