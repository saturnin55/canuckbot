from typing import Annotated

from pydantic import Field

HEX_COLOR_PATTERN = r"^#(?:[0-9a-fA-F]{3}){1,2}$"
DISCORDCHANNELNAME_PATTERN = r"^[a-z0-9-]{1,100}$"
HANDLE_PATTERN = r"^[a-zA-Z0-9\-]+$"

Handle = Annotated[str, Field(pattern=HANDLE_PATTERN, max_length=24)]
HexColor = Annotated[str, Field(pattern=HEX_COLOR_PATTERN)]
# we'll need to store snowflakeid as TEXT into sqlite
UnixTimestamp = Annotated[int, Field(strict=True, gt=0)]
SnowflakeId = Annotated[int, Field(strict=True, gt=0, lt=2**64 - 1)]
DiscordChannelName: str = Field(..., pattern=r"^[a-z0-9-]{1,100}$")
DiscordRoleId = SnowflakeId
DiscordUserId = SnowflakeId
DiscordCategoryId = SnowflakeId
DiscordChannelId = SnowflakeId
