import time
from enum import Enum
from datetime import date, datetime
from typing import Any, List, Optional, Type
from aiosqlite import Error as aiosqliteError
from Discord.DiscordBot import DiscordBot
from CanuckBot import CanuckBotBase
from CanuckBot.types import User_Level
from Discord.types import Snowflake

class MANAGER_FIELDS_INFO(str, Enum):
    user_id = "user_id"
    created_at = "created_at"
    created_by = "created_by"
    level = "level"
    competitions = "competitions"

class MANAGER_FIELDS_EDITABLE(str, Enum):
    level = "level"

class Manager(CanuckBotBase):
    user_id: Snowflake = 0
    created_at: date = 0
    created_by: Snowflake = 0
    level: User_Level = User_Level.Disabled
    competitions: List[int] = []

    class Manager:
        arbitrary_types_allowed = True

    def __init__(self, bot: DiscordBot, **kwargs):
        super().__init__(bot, **kwargs)

    @classmethod
    async def create(cls: Type["Manager"], bot: DiscordBot) -> "Manager":
        instance = cls(bot)
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
                self.created_at = datetime.fromtimestamp(int(row["created_at"]))
                self.created_by = int(row["created_by"])
                self.level = User_Level(row["level"])

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

    async def add(self, user_id: int, invoking_id: int, level: User_Level) -> bool:
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
                    "INSERT INTO managers(user_id, created_at, created_by, level) VALUES (?, ?, ?, ?)",
                    [str(user_id), now, str(invoking_id), str(level.value)]
                )

                self.user_id = int(user_id)
                self.created_at = datetime.fromtimestamp(int(now))
                self.created_by = int(invoking_id)
                self.level = level.value

                # make sure there are no prior entries in manager_competitions
                await self._bot.database.delete(
                    "DELETE FROM manager_competitions WHERE user_id = ?", [str(user_id)]
                )

                for competition_id in self.competitions:
                    await self._bot.database.insert(
                        "INSERT INTO manager_competitions (user_id, competition_id) VALUES (?, ?)", 
                        [str(user_id), str(competition_id)]
                    )

                await self._bot.database.connection.commit()

                return True
            except aiosqliteError as e:
                print(f"ERR Manager.add(): {e}")
                return False

        return True

    async def remove(self, user_id: int) -> bool:
        assert self._bot.database, "ERR Manager.remove(): database not available."
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

                await self._bot.database.delete(
                    "DELETE FROM manager_competitions WHERE user_id = ?", [str(user_id)]
                )

                await self._bot.database.connection.commit()

                return True
            except aiosqliteError as e:
                print(f"ERR Manager.add(): {e}")
                return False

        return True

    async def list(self) -> list[dict[str, Any]] | bool:
        try:
            assert self._bot.database, "ERR Manager.list(): database not available."

            data = []

            rows = await self._bot.database.select(
                "SELECT user_id, created_at, created_by, level FROM managers ORDER BY level ASC, created_at ASC"
            )
            if not rows:
                return data
            else:
                for row in rows:
                    row["user_id"] = int(row["user_id"])
                    row["created_at"] = datetime.fromtimestamp(int(row["created_at"]))
                    row["created_by"] = int(row["created_by"])
                    row["level"] = User_Level(int(row["level"]))
                    row["competitions"] = []

                crows = await self._bot.database.select(
                    "SELECT competition_id FROM manager_competitions WHERE user_id = ? ORDER BY competition_id ASC",
                    [row["user_id"]],
                )
                if crows:
                    row["competitions"] = []
                    for crow in crows:
                        row["competitions"].append(int(crow["competition_id"]))

            return rows
        except aiosqliteError as e:
            print(f"ERR Manager.list(): {e}")
            return False

    async def addcomp(self, competition_id: int = None) -> bool:
        assert self._bot.database, "ERR Manager.addcomp(): database not available."
            
        if self.user_id is None or competition_id is None:
            return False

        try:
            await self._bot.database.delete(
                "INSERT INTO manager_competitions (user_id, competition_id) VALUES (?, ?)", [int(self.user_id), int(competition_id)]
            )
            await self._bot.database.connection.commit()
        except:
            return False

        return True

    async def delcomp(self, competition_id: int = None) -> bool:
        assert self._bot.database, "ERR Manager.delcomp(): database not available."
        
        if self.user_id is None or competition_id is None:
            return False

        try:
            await self._bot.database.delete(
                "DELETE FROM manager_competitions WHERE user_id = ? AND competition_id = ?", [int(self.user_id), int(competition_id)]
            )
            await self._bot.database.connection.commit()
        except:
            return False

        return True

    async def update(self, field: str = None, value: Any = None) -> bool:
        if not field:
            return False

        assert self._bot.database, "ERR Manager.update(): database not available."

        cast_value = self.cast_value(field, value)
        setattr(self, field, cast_value)

        await self._bot.database.update(
            f"UPDATE managers SET {field} = ? WHERE user_id = ?", [cast_value, self.user_id]
        )
        return True

    def is_loaded(self) -> bool:
        if self.user_id == 0:
            return False
        else:
            return True

    async def clear_competitions(self) -> bool:
        try:
            await self._bot.database.delete(
                "DELETE FROM manager_competitions WHERE user_id = ?", [int(self.user_id)]
            )
            await self._bot.database.connection.commit()
            return True
        except:
            return False

