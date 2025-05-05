import time
import discord
from database import DatabaseManager
from CanuckBot.types import SnowflakeId
from typing import Any

class DiscordCache():
    def __init__(self, _db: DatabaseManager = None, expire_offset: int = 3600) -> None:
    self._db = _db

    async def store(self, key: SnowflakeId = None, name: str = None) -> bool:
        now = int(time.time())
        expire = now + expire_offset

        await self._db.insert("INSERT OR REPLACE INTO discord_cache (key, name, timestamp, expiration) VALUES (?, ?, ?, ?, ?)", [str(key), str(name), now, expire])

    async def retreive(self, key: SnowflakeId = None) -> bool | str:
        row = await self._db.get_one("SELECT name FROM discord_cache WHERE key = ? and expire >= ?", [str(key), expire])
        if not row:
            return False
        else:
            return str(row["name"])
