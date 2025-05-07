from enum import IntEnum
from typing import Annotated, Any
from pydantic import Field

DISCORDCHANNELNAME_PATTERN = r"^[a-z0-9-]{1,100}$"
SnowflakeId = Annotated[int, Field(strict=True, ge=0, lt=2**64 - 1)]
DiscordChannelName: str = Field(..., pattern=r"^[a-z0-9-]{1,100}$")
DiscordRoleId = SnowflakeId
DiscordUserId = SnowflakeId
DiscordCategoryId = SnowflakeId
DiscordChannelId = SnowflakeId
DiscordMessageId = SnowflakeId
DiscordGuildId = SnowflakeId

class Discord_Object_Type(IntEnum):
    User = 0
    Channel = 1
    Category = 2
    Role = 3
    Message = 4
    Guild = 5
    
    def __str__(self):
        return self.name
