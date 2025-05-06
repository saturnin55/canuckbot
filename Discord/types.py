from datetime import date
from typing import Annotated, Any
from pydantic import Field, GetCoreSchemaHandler, HttpUrl
from pydantic_core import core_schema

DISCORDCHANNELNAME_PATTERN = r"^[a-z0-9-]{1,100}$"
SnowflakeId = Annotated[int, Field(strict=True, ge=0, lt=2**64 - 1)]
DiscordChannelName: str = Field(..., pattern=r"^[a-z0-9-]{1,100}$")
DiscordRoleId = SnowflakeId
DiscordUserId = SnowflakeId
DiscordCategoryId = SnowflakeId
DiscordChannelId = SnowflakeId
DiscordMessageId = SnowflakeId
DiscordGuildId = SnowflakeId

class DiscordGuild:
    id: DiscordGuildId
    name: str

class DiscordRole:
    id: DiscordRoleId
    name: str
    guild: DiscordGuild
    mention: str

class DiscordChannel:
    id: DiscordChannelId
    name: str
    guild: DiscordGuild
    mention: str

class DiscordUser:
    id: DiscordUserId
    name: str
    discriminator: str
    display_name: str
    global_name: str
    avatar_url: HttpUrl
    mention: str
    bot: bool

class DiscordCategory:
    id: DiscordCategoryId
    name: str
    guild: DiscordGuild
    mention: str

class DiscordMessage:
    id: DiscordMessageId
    content: str
    author: DiscordUser
    channel: DiscordChannel
    guild: DiscordGuild
    created_at: date
    edited_at: date
