import logging
import pytz
from enum import IntEnum
from typing import Annotated, Any
from pydantic import Field
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

HEX_COLOR_PATTERN = r"^#(?:[0-9a-fA-F]{3}){1,2}$"
HANDLE_PATTERN = r"^[a-zA-Z0-9\-]+$"

Handle = Annotated[str, Field(pattern=HANDLE_PATTERN, max_length=24)]
HexColor = Annotated[str, Field(pattern=HEX_COLOR_PATTERN)]
# we'll need to store snowflakeid as TEXT into sqlite
UnixTimestamp = Annotated[int, Field(strict=True, ge=0)]

class Log_Level(IntEnum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __str__(self):
        return self.name

class User_Level(IntEnum):
    Superadmin = 0
    Full = 10
    Comp = 20
    Trusted = 30
    Disabled = 99

    def __str__(self):
        return self.name

class Competition_Type(IntEnum):
    Men = 0
    Women = 1

    def __str__(self):
        return self.name

class Match_Status(IntEnum):
    TBD = 0         # Some info about the match is yet TBD (kickoff, venue, home, away)
    Pending = 1     # Match in scheduled but not yet reached match's hours_before_kickoff
    Ready = 2       # We reached match's hours_before_kickoff, channel should be created
    Active = 3      # Match in progress or channel not yet deleted
    Completed = 4   # Match reached match's hours_after_kickoff, time to cleanup

    def __str__(self):
        return self.name

class TimeZone:
    def __init__(self, tz: str):
        if not self.validate_timezone(tz):
            raise ValueError(f"Invalid time zone: {tz}")
        self.tz = tz

    def __str__(self):
        return self.tz

    def validate_timezone(self, tz: str) -> bool:
        return tz in pytz.all_timezones

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        def validate(value: Any) -> "TimeZone":
            if isinstance(value, TimeZone):
                return value
            if isinstance(value, str):
                return cls(value)
            raise TypeError("TimeZone must be a string or TimeZone instance")
        return core_schema.no_info_plain_validator_function(validate)

    def __eq__(self, other):
        return isinstance(other, TimeZone) and self.tz == other.tz
