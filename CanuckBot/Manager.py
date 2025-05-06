import time
from datetime import date
from typing import Any, List, Optional, Type
from aiosqlite import Error as aiosqliteError
from Discord.DiscordBot import DiscordBot
from CanuckBot import CanuckBotBase
from CanuckBot.types import DiscordUserId, User_Level


class Manager(CanuckBotBase):
    user_id: DiscordUserId = 0
    created_at: date = 0
    created_by: DiscordUserId = 0
    level: User_Level = User_Level.Public
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
                self.user_id = DiscordUserId(row["user_id"])
                self.created_at = date.fromtimestamp(int(row["created_at"]))
                self.created_by = DiscordUserId(row["created_by"])
                self.level = row["level"]

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

    async def add(self, user_id: DiscordUserId, invoking_id: DiscordUserId, level: User_Level) -> bool:
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
                print("a1")

                self.user_id = DiscordUserId(user_id)
                self.created_at = date.fromtimestamp(int(now))
                self.created_by = DiscordUserId(invoking_id)
                self.level = level.value

                # make sure there are no prior entries in manager_competitions
                await self._bot.database.delete(
                    "DELETE FROM manager_competitions WHERE user_id = ?", [str(user_id)]
                )
                print("a2")

                for competition_id in self.competitions:
                    await self._bot.database.insert(
                        "INSERT INTO manager_competitions (user_id, competition_id) VALUES (?, ?)", 
                        [str(user_id), str(competition_id)]
                    )
                print("a3")

                await self._bot.database.connection.commit()
                print("a4")

                return True
            except aiosqliteError as e:
                print(f"ERR Manager.add(): {e}")
                return False

        return True

    async def remove(self, user_id: DiscordUserId) -> bool:
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
            assert self._bot.database, "ERR Manager.py list(): database not available."

            data = []

            rows = await self._bot.database.select(
                "SELECT user_id, strftime('%s', created_at) as created_at, created_by \
                                                   FROM managers \
                                                   ORDER BY created_at ASC"
            )
            if not rows:
                return False
            else:
                for row in rows:
                    row["user_id"] = DiscordUserId(row["user_id"])
                    row["created_at"] = date.fromtimestamp(int(row["created_at"]))
                    row["created_by"] = DiscordUserId(row["created_by"])
                    row["competitions"] = []

                crows = await self._bot.database.select(
                    "SELECT competition_id FROM manager_competitions WHERE user_id = ? ORDER BY competition_id ASC",
                    [row["user_id"]],
                )
                if crows:
                    for row in crows:
                        row["competitions"].append(int(row["competition_id"]))

            return rows
        except aiosqliteError as e:
            print(f"ERR Manager.get_all(): {e}")
            return False
