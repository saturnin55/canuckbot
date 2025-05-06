from datetime import date
from CanuckBot import CanuckBotBase
from CanuckBot.types import Match_Status, TimeZone
from Discord.types import DiscordChannelName, SnowflakeId, DiscordChannelName, DiscordChannelId, DiscordMessageId


class Match(CanuckBotBase):
    match_id: int
    home_id: int
    away_id: int
    competition_id: int
    status: Match_Status
    kickoff_at: date
    delete_at: date
    tz: TimeZone
    venue: str
    description: str
    channel_name = DiscordChannelName
    channel_id = SnowflakeId
    channel_topic: str
    is_warned: bool
    welcome_message_id = SnowflakeId
    hours_before_kickoff: int
    hours_after_kickoff: int
    watch: str
    stream: HttpUrl
