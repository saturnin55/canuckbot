from pydantic import Field, conint

Handle = Field(
    ..., pattern=r"^[a-zA-Z0-9\-]+$", max_length=24
)  # max_length=23 ensures under 24 characters
HexColor = Field(..., pattern=r"^#(?:[0-9a-fA-F]{3}){1,2}$")
# we'll need to store snowflakeid as TEXT into sqlite
UnixTimestamp = conint(ge=0)
SnowflakeId = conint(ge=0, le=2**64 - 1)
DiscordChannelName = Field(..., pattern=r"^[a-z0-9-]{1,100}$")
