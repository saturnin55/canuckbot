import pytz
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

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
        def validate(value: str) -> "TimeZone":
            return cls(value)
        return core_schema.no_info_plain_validator_function(validate)
