from enum import Enum
from datetime import date
from CanuckBot import CanuckBotBase
from CanuckBot.types import Match_Status, TimeZone
from Discord.types import DiscordChannelName, DiscordChannelId, DiscordMessageId, DiscordUserId


class MATCH_FIELDS_EDITABLE(str, Enum):
    home_id = "home_id"
    away_id = "away_id"
    competition_id = "competition_id"
    status = "status"
    kickoff_at = "kickoff_at"
    tz = "tz"
    venue = "venue"
    description = "description"
    channel_name = "description"
    channel_id = "channel_id"
    is_warned = "is_warned"
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
    kickoff_at: date
    tz: TimeZone
    venue: str
    description: str
    channel_name: DiscordChannelName
    channel_id: DiscordChannelId
    channel_topic: str
    is_warned: bool
    welcome_msg_id: DiscordMessageId
    hours_before_kickoff: int
    hours_after_kickoff: int
    watch: str
    stream: HttpUrl
    created_by: DiscordUserId
    created_at: date
    lastmodified_by: DiscordUserId | None
    lastmodified_at: date | None

