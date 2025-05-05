import time
from database import DatabaseManager
from CanuckBot.types import SnowflakeId

class DiscordCache():
    def __init__(self, db: DatabaseManager = None, expire_offset: int = 3600) -> None:
        self._db = db
        self.expire_offset = expire_offset

    async def store(self, key: SnowflakeId = None, name: str = None) -> bool:
        now = int(time.time())
        expire = now + self.expire_offset

        await self._db.insert("INSERT OR REPLACE INTO discord_cache (key, name, timestamp, expiration) VALUES (?, ?, ?, ?)", [str(key), str(name), now, expire])

    async def retrieve(self, key: SnowflakeId = None) -> bool | str:
        row = await self._db.get_one("SELECT name FROM discord_cache WHERE key = ? and expiration >= CURRENT_TIMESTAMP", [str(key)])
        if not row:
            return False
        else:
            return str(row["name"])
