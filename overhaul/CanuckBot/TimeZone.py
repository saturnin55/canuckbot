import pytz

class TimeZone:
    def __init__(self, tz: str):
        if not self.validate_timezone(tz):
            raise ValueError("Invalid time zone format")
        self.tz = tz

    def __str__(self):
        return self.tz

    def validate_timezone(self, tz: str) -> bool:
        return tz in pytz.all_timezones
