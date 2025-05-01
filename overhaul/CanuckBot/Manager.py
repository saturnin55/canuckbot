import time
from datetime import date
from typing import List, Optional

from . import CanuckBotBase
from .types import SnowflakeId
from .User_Level import User_Level



class Manager(CanuckBotBase):
    user_id = SnowflakeId
    created_at: date
    created_by = SnowflakeId
    level: User_Level
    competitions: List[int]

    def __init__(self, bot):
        super().__init__(bot)
        self.user_id = null
        self.created_at = null
        self.created_by = null
        self.level = User_Level.Public
        self.competitions = []

    @classmethod
    async def create(cls, bot):
        instance = Manager(bot)
        return instance

    async def get(self, user_id: Optional[int] = None) -> bool:
        if user_id is None:
            return False
        else:
            row = await self.database.get_one(
                "SELECT * FROM managers WHERE user_id = ?", [str(user_id)]
            )
            if not row:
                return False
            else:
                self.data["user_id"] = int(row["user_id"])
                self.data["created_at"] = int(row["created_at"])
                self.data["created_by"] = int(row["created_by"])

                return True

    async def add(self, user_id: int, invoking_id: int) -> bool:
        user = await self.database.get_one(
            "SELECT * FROM managers WHERE user_id = ?", [str(user_id)]
        )

        if user:
            # user already exists in managers table
            return False
        else:
            try:
                now = int(time.time())
                await self.database.insert(
                    "INSERT INTO managers(user_id, created_at, created_by) VALUES (?, ?, ?)",
                    (str(user_id), now, str(invoking_id)),
                )
                await self.database.connection.commit()

                self.data["user_id"] = int(user_id)
                self.data["created_at"] = int(now)
                self.data["created_by"] = int(invoking_id)

                return True
            except aiosqlite.Error as e:
                print(f"ERR Manager.add(): {e}")
                return False

        return True

    async def remove(self, user_id: int) -> bool:
        user = await self.database.get_one(
            "SELECT * FROM managers WHERE user_id = ?", [str(user_id)]
        )

        if not user:
            # user doesn't exists in managers table
            return True
        else:
            try:
                await self.database.delete(
                    "DELETE FROM managers WHERE user_id = ?", [str(user_id)]
                )
                await self.database.connection.commit()

                return True
            except aiosqlite.Error as e:
                print(f"ERR Manager.add(): {e}")
                return False

        return True

    async def list(self) -> dict | bool:
        try:
            rows = await self.bot.database.select(
                "SELECT user_id, strftime('%s', created_at) as created_at, created_by \
                                                   FROM managers \
                                                   ORDER BY created_at ASC"
            )
            if not rows:
                return False
            else:
                for row in rows:
                    row["user_id"] = int(row["user_id"])
                    row["created_at"] = int(row["created_at"])
                    row["created_by"] = int(row["created_by"])
                return rows
        except aiosqlite.Error as e:
            print(f"ERR Manager.get_all(): {e}")
            return False
