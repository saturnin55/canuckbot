
class Timestamp:
    def __init__(self, ts: int):
        if not self.validate_timestamp(ts):
            raise ValueError("Invalid timestamp format")
        self.ts = ts

    def __str__(self):
        return self.ts

    def validate_timestamp(self, value: int) -> bool:
        if not isinstance(value, int):  # Ensure it's an integer
            return False

        # Define reasonable Unix timestamp range (1970 to 2100)
        min_timestamp = 0  # 1970-01-01 00:00:00 UTC
        max_timestamp = 4102444800  # 2100-01-01 00:00:00 UTC

        return min_timestamp <= value <= max_timestamp
