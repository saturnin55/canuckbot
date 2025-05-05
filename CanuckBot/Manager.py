import time
from datetime import date
from typing import Any, List, Optional, Type

from aiosqlite import Error as aiosqliteError

from DiscordBot.DiscordBot import DiscordBot

# from User_Level import User_Level
from . import CanuckBotBase
from .types import SnowflakeId, DiscordUserId


class Manager(CanuckBotBase):
    user_id = DiscordUserId
    created_at: date
    created_by = DiscordUserId
    # level: User_Level = User_Level.Public
    competitions: List[int] = []

    def __init__(self, bot: DiscordBot):
        super().__init__(bot)
        self.user_id = None
        # self.created_at = None
        self.created_by = None
        # self.level = User_Level.Public
        self.competitions = []

    @classmethod
    async def create(cls: Type["Manager"], bot: DiscordBot) -> "Manager":
        instance = Manager(bot)
        return instance

    async def get(self, user_id: Optional[int] = None) -> bool:
        if user_id is None:
            return False
        else:
            assert self._bot.database, "ERR Manager.py get(): database not available."
            row = await self._bot.database.get_one(
                "SELECT * FROM managers WHERE user_id = ?", [str(user_id)]
            )
            if not row:
                return False
            else:
                self.user_id = int(row["user_id"])
                self.created_at = date.fromtimestamp(int(row["created_at"]))
                self.created_by = int(row["created_by"])

            try:
                rows = await self._bot.database.select(
                    "SELECT competition_id FROM manager_competitions WHERE user_id = ? ORDER BY competition_id ASC",
                    [str(user_id)],
                )
                if not rows:
                    self.competitions = []
                else:
                    for row in rows:
                        self.competitions.append(int(row["competition_id"]))
            except aiosqliteError as e:
                print(f"ERR Manager.get(): {e}")
                return False

        return True

    async def add(self, user_id: int, invoking_id: int) -> bool:
        assert self._bot.database, "ERR Manager.py add(): database not available."
        user = await self._bot.database.get_one(
            "SELECT * FROM managers WHERE user_id = ?", [str(user_id)]
        )

        if user:
            # user already exists in managers table
            return False
        else:
            try:
                now = int(time.time())
                await self._bot.database.insert(
                    "INSERT INTO managers(user_id, created_at, created_by) VALUES (?, ?, ?)",
                    [str(user_id), now, str(invoking_id)],
                )
                await self._bot.database.connection.commit()

                self.user_id = int(user_id)
                self.created_at = date.fromtimestamp(int(now))
                self.created_by = int(invoking_id)

                # make sure there are no prior entries in manager_competitions
                await self._bot.database.delete(
                    "DELETE FROM manager_competitions WHERE user_id = ?", [str(user_id)]
                )
                await self._bot.database.connection.commit()

                return True
            except aiosqliteError as e:
                print(f"ERR Manager.add(): {e}")
                return False

        return True

    async def remove(self, user_id: int) -> bool:
        assert self._bot.database, "ERR Manager.py remove(): database not available."
        user = await self._bot.database.get_one(
            "SELECT * FROM managers WHERE user_id = ?", [str(user_id)]
        )

        if not user:
            # user doesn't exists in managers table
            return True
        else:
            try:
                await self._bot.database.delete(
                    "DELETE FROM managers WHERE user_id = ?", [str(user_id)]
                )
                await self._bot.database.connection.commit()

                return True
            except aiosqliteError as e:
                print(f"ERR Manager.add(): {e}")
                return False

        return True

    async def list(self) -> list[dict[str, Any]] | bool:
        try:
            assert self._bot.database, "ERR Manager.py list(): database not available."
            rows = await self._bot.database.select(
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
        except aiosqliteError as e:
            print(f"ERR Manager.get_all(): {e}")
            return False
