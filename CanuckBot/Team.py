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
                await self.load_aliases()
            except Exception as e:
                raise ValueError(e)
                return False

        return True


    async def load_aliases(self) -> bool:
        try:
            rows = await self._bot.database.select(
                "SELECT alias FROM team_aliases WHERE team_id = ? ORDER BY alias ASC",
                [str(self.team_id)],
            )
            if not rows:
                self.aliases = []
            else:
                for row in rows:
                    self.aliases.append(str(row["alias"]))
        except Exception as e:
            raise ValueError(e)
            return False

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

                await self.load_aliases()

                return True


    async def load_by_key(self, key: str = None):
        if key.isdigit():
            await self.load_by_id(int(key))
        else:
            await self.load_by_shortname(str(key))

    async def load_by_id(self, team_id: int = 0):

        await self.load('team_id', int(team_id))


    async def is_alias(self, alias: str = None) -> bool | int:

        if not alias:
            return False

        try:
            row = await self._bot.database.get_one(
                f"SELECT a.team_id FROM teams a, team_aliases b WHERE a.team_id = b.team_id AND LOWER(b.alias) = LOWER(?)", [str(alias)]
            )
            if not row:
                return False
            else:
                return row["team_id"]

        except Exception as e:
            raise ValueError(e)
            return False

    
    async def load_by_alias(self, alias: str = None):

        #if not is_valid_handle(alias):
        #    return False

        if not alias:
            return False

        team_id = await self.is_alias(alias)

        try:
            if not team_id:
                self.team_id = 0
                return False
            else:
                await self.load_by_id(team_id)
                return True
        except Exception as e:
            raise ValueError(e)
            return False


    async def load_by_shortname(self, shortname: Handle = None):
        if await self.load('shortname', str(shortname)):
            return True
        else:
            # check by aliases
            return await self.load_by_alias(shortname)

        return False

    async def is_shortname_unique(self, shortname: Handle = None) -> bool:

        t = Team(self._bot)

        await t.load_by_shortname(shortname)

        if t.is_loaded():
            return t.team_id
        else:
            return False
        
    async def update(self, field: str = None, value: Any = None) -> bool:
        try:
            if not field:
                return False

            assert self._bot.database, "ERR Manager.update(): database not available."

            cast_value = self.cast_value(field, value)
            setattr(self, field, cast_value)

            await self._bot.database.update(
                f"UPDATE teams SET {field} = ? WHERE user_id = ?", [cast_value, self.user_id]
            )
            return True
        except Exception as e:
            raise ValueError(e)
            return False


    async def remove(self) -> bool:

        try:
            await self._bot.database.delete("DELETE FROM teams WHERE team_id = ?", [int(self.team_id)])

            await self.clear_aliases()

            self.team_id = 0
            self.name = None
            self.shortname = None
            self.tz = None
            self.aliases = []
            self.created_at = 0
            self.created_by = None
            self.lastmodified_at = None
            self.lastmodified_by = None

            return True
        except Exception as e:
            raise ValueError(e)
            return False

    async def add(self) -> bool:

        try:
            await self._bot.database.insert(
                "INSERT INTO teams (name, shortname, tz, created_at, created_by) VALUES (?, ?, ?, ?, ?)",
                [str(self.name), str(self.shortname), str(self.tz), str(self.created_at), int(self.created_by)]
                )

            self.team_id = int(self._bot.database.lastrowid())

            await self._bot.database.connection.commit()

            # make sure there are no prior entries in team_aliases
            await self.clear_aliases()

            return True
        except Exception as e:
            raise ValueError(e)
            return False
                

    async def setmodified(self) -> bool:
        try:
            await self.update('lastmodified_by', self.lastmodified_by)
            await self.update('lastmodified_at', int(time.time()))
            return True
        except Exception as e:
            raise ValueError(e)
            return False
        
    async def add_alias(self, alias: str = None) -> bool:

        try:
            # alias must be a valid Handle
            if not is_valid_handle(alias):
                return False

            # check if alias isn't already in the team's aliases
            if await self.is_alias(alias):
                return True

            # check if new alias is unique
            ret = await self.is_shortname_unique(alias)

            if ret:
                raise ValueError(f"Alias `{alias}` is used by another team: `team_id : {ret}`")
                return False

            # add the alias to the database
            await self._bot.database.insert(
                "INSERT INTO team_aliases (team_id, alias) VALUES (?, ?)",
                [int(self.team_id), str(alias)]
                )

            # add the alias to the database
            await self._bot.database.connection.commit()

            self.aliases.append(alias)

            return True

        except Exception as e:
            raise ValueError(e) 
            return False

    async def remove_alias(self, alias: str = None) -> bool:
    
        try:
            if not alias:
                return False

            # alias must be a valid Handle
            if not is_valid_handle(alias):
                return False

            if alias.lower() not in (val.lower() for val in self.aliases): 
                return True

            # delete the alias from the database
            await self._bot.database.delete(
                "DELETE FROM team_aliases WHERE team_id = ? and alias = ?",
                [int(self.team_id), str(alias)]
                )

            await self._bot.database.connection.commit()

            self.aliases.remove(alias)

            return True

        except Exception as e:
            raise ValueError(e)
            return False

    async def clear_aliases(self) -> bool:

        if self.team_id is None:
            return False

        try:
            await self._bot.database.delete(
                "DELETE FROM team_aliases WHERE team_id = ?", [int(self.team_id)]
                )

            await self._bot.database.connection.commit()

        except Exception as e:
            raise ValueError(e)
            return False

        return True
