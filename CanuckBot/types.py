from typing import Annotated

from pydantic import Field

HEX_COLOR_PATTERN = r"^#(?:[0-9a-fA-F]{3}){1,2}$"
DISCORDCHANNELNAME_PATTERN = r"^[a-z0-9-]{1,100}$"
HANDLE_PATTERN = r"^[a-zA-Z0-9\-]+$"

Handle: str = Field(
    ..., pattern=r"^[a-zA-Z0-9\-]+$", max_length=24
)  # max_length=23 ensures under 24 characters
HexColor = Annotated[str, Field(pattern=HEX_COLOR_PATTERN)]
# we'll need to store snowflakeid as TEXT into sqlite
UnixTimestamp = Annotated[int, Field(strict=True, gt=0)]
SnowflakeId = Annotated[int, Field(strict=True, gt=0, lt=2**64 - 1)]
DiscordChannelName: str = Field(..., pattern=r"^[a-z0-9-]{1,100}$")
