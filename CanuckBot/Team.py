import time
from enum import Enum
from datetime import date, datetime
from typing import List, Type, Any, Optional
from CanuckBot import CanuckBotBase
from CanuckBot.types import TimeZone, Handle
from Discord.types import Snowflake
from CanuckBot.utils import is_valid_handle
from Discord.DiscordBot import DiscordBot


class TEAM_FIELDS_INFO(str, Enum):
    team_id = "team_id" 
    name = "name"
    shortname = "shortname"
    tz = "tz"
    aliases = "aliases"
    created_by = "created_by"
    created_at = "created_at"
    lastmodified_by = "lastmodified_by"
    lastmodified_at = "lastmodified_at"

class TEAM_FIELDS_EDITABLE(str, Enum):
    name = "name"
    shortname = "shortname"
    tz = "tz"

class Team(CanuckBotBase):
    team_id: int = 0
    name: str = None
    shortname: Handle = None
    tz: TimeZone = None
    aliases: List[str] = []
    created_by: Snowflake | None = None
    created_at: date = 0
    lastmodified_by: Snowflake | None = None
    lastmodified_at: date | None = None

    class Team:
        arbitrary_types_allowed = True

    def __init__(self, bot: DiscordBot, **kwargs):
        super().__init__(bot, **kwargs)

    @classmethod
    async def create(cls: Type["Team"], bot: DiscordBot) -> "Team":
        instance = cls(bot)
        return instance

    async def get(self, team_id: Optional[int] = None) -> bool:
        if team_id is None:
            return False
        else:
            assert self._bot.database, "ERR Team.py get(): database not available."
            row = await self._bot.database.get_one(
                "SELECT * FROM teams WHERE team_id = ?", [str(team_id)]
            )

            if not row:
                return False
            else:
                self.team_id = int(row["team_id"])
                self.name = str(row["name"])
                self.shortname = str(row["shortname"])
                self.tz = TimeZone(str(row["tz"]))
                self.created_at = datetime.fromtimestamp(int(row["created_at"]))
                self.created_by = int(row["created_by"])
                self.lastmodified_at = datetime.fromtimestamp(int(row["lastmodified_at"]))
                self.lastmodified_by = int(row["lastmodified_by"])

            try:
                rows = await self._bot.database.select(
                    "SELECT alias FROM team_aliases WHERE team_id = ? ORDER BY alias ASC",
                    [str(team_id)],
                )
                if not rows:
                    self.aliases = []
                else:
                    for row in rows:
                        self.aliases.append(str(row["alias"]))
            except aiosqliteError as e:
                print(f"ERR Team.get(): {e}")
                return False

        return True


    def is_loaded(self) -> bool:
        if self.team_id == 0:
            return False
        else:
            return True

    async def load(self, key: str = 'team_id', keyval: str | int = None) -> bool:
        if keyval is None or key not in ['team_id', 'shortname']:
            return False
        else:
            assert self._bot.database, "ERR Team.py load(): database not available."
            row = await self._bot.database.get_one(
                f"SELECT * FROM teams WHERE {key} = ?", [keyval]
            )

            if not row:
                return False
            else:
                self.team_id = int(row["team_id"])
                self.name = str(row["name"])
                self.shortname = Handle(row["shortname"])
                self.tz = TimeZone(row["tz"])

                if row["created_by"] is not None:
                    self.created_by = int(row["created_by"])
                if row["created_at"] is not None:
                    self.created_at = datetime.fromtimestamp(int(row["created_at"]))
                if row["lastmodified_by"] is not None:
                    self.lastmodified_by = int(row["lastmodified_by"])
                if row["lastmodified_at"] is not None:
                    self.lastmodified_at = datetime.fromtimestamp(int(row["lastmodified_at"]))

                return True


    async def load_by_key(self, key: str = None):
        if key.isdigit():
            await self.load_by_id(int(key))
        else:
            await self.load_by_shortname(str(key))

    async def load_by_id(self, team_id: int = 0):

        await self.load('team_id', int(team_id))


    async def load_by_shortname(self, shortname: Handle = None):
        await self.load('shortname', str(shortname))

    async def is_shortname_unique(self, shortname: Handle = None) -> bool:
        t = Team(self.bot)

        await t.load_by_shortname(shortname)

        return t.is_loaded()
        
    #async def search(self, criteria: str = None) -> List[int]:
    #    pass

    async def update(self, field: str = None, value: Any = None) -> bool:
        if not field:
            return False

        assert self._bot.database, "ERR Manager.update(): database not available."

        cast_value = self.cast_value(field, value)
        setattr(self, field, cast_value)

        await self._bot.database.update(
            f"UPDATE teams SET {field} = ? WHERE user_id = ?", [cast_value, self.user_id]
        )
        return True

    async def add(self) -> bool:

        try:
            await self._bot.database.insert(
                "INSERT INTO teams (name, shortname, tz, created_at, created_by) VALUES (?, ?, ?, ?, ?)",
                [str(self.name), str(self.shortname), str(self.tz), str(self.created_at), int(self.created_by)]
                )

            print("a1")
            self.team_id = int(self._bot.database.lastrowid())
            print("a2")

            await self._bot.database.connection.commit()
            print("a3")

            # make sure there are no prior entries in team_aliases
            await self.clear_aliases()
            print("a4")

            return True
        except Exception as e:
            raise ValueError(e)
            return False
                

    async def setmodified(self) -> bool:
        try:
            await self.update('lastmodified_by', self.lastmodified_by)
            await self.update('lastmodified_at', int(time.time()))
            return True
        except:
            #fixme
            return False
        
    async def add_alias(self, alias: str = None) -> bool:
        # alias must be a valid Handle
        if not is_valid_handle(alias):
            return False

        # check if alias isn't already in the team's aliases
        if alias in self.aliases:
            return True

        # check if new alias is unique
        if not self.is_shortname_unique(alias):
            return False

        # add the alias to the database

        return True

    async def del_alias(self, alias: str = None) -> bool:
        # alias must be a valid Handle
        if not is_valid_handle(alias):
            return False

        if alias not in self.aliases:
            return True

        # delete the alias from the database

        return True

    async def clear_aliases(self) -> bool:

        if self.team_id is None:
            return False

        try:
            await self._bot.database.delete(
                "DELETE FROM team_aliases WHERE team_id = ?", [int(self.team_id)]
                )

            await self._bot.database.connection.commit()
        except:
            return False

        return True
