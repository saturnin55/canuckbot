import time
from database import DatabaseManager


class Cache():
    def __init__(self, db: DatabaseManager = None, expire_offset: int = 86400) -> None:
        self._db = db
        self.expire_offset = expire_offset

    async def store(self, key: str = None, data: str = None) -> bool:
        if not key or not data:
            return False

        now = int(time.time())
        expire = now + self.expire_offset

        await self._db.insert("INSERT OR REPLACE INTO canuckbot_cache (key, data, timestamp, expiration) VALUES (?, ?, ?, ?)", [str(key), str(data), now, expire])

    async def retrieve(self, key: str = None) -> bool | str:
        if not key:
            return False

        row = await self._db.get_one("SELECT data FROM canuckbot_cache WHERE key = ? and expiration >= strftime('%s','now')", [str(key)])
        if not row:
            return False
        else:
            return str(row["data"])
