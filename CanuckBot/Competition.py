from enum import Enum
from datetime import date, datetime
from pydantic import HttpUrl, BaseModel, Field, TypeAdapter, PrivateAttr
from typing import Type, List, Any, Optional
from discord.ext.commands import Bot
from CanuckBot import CanuckBotBase
from CanuckBot.types import Handle, HexColor, Competition_Type
from Discord.types  import Snowflake


class COMPETITION_FIELDS_INFO(str, Enum):
    competition_id = "competition_id"
    name = "name"
    shortname = "shortname"
    logo_url = "logo_url"
    competition_type = "competition_type"
    is_monitored = "is_monitored"
    is_international = "is_international"
    optout_role_id = "optout_role_id"
    category_id = "category_id"
    hours_before_kickoff = "hours_before_kickoff"
    hours_after_kickoff = "hours_after_kickoff"
    created_by = "created_by"
    created_at = "created_at"
    lastmodified_by = "lastmodified_by"
    lastmodified_at = "lastmodified_at"

class COMPETITION_FIELDS_EDITABLE(str, Enum):
    name = "name"
    shortname = "shortname"
    logo_url = "logo_url"
    competition_type = "competition_type"
    is_monitored = "is_monitored"
    is_international = "is_international"
    optout_role_id = "optout_role_id"
    category_id = "category_id"
    hours_before_kickoff = "hours_before_kickoff"
    hours_after_kickoff = "hours_after_kickoff"

class Competition(CanuckBotBase):
    competition_id: int = 0
    name: str | None = Field(default=None)
    shortname: Handle | None = None
    logo_url: HttpUrl = "https://raw.githubusercontent.com/saturnin55/CanuckBot/main/images/1x1-transparent.png"
    competition_type: Competition_Type = Competition_Type.Men
    is_monitored: bool = False
    is_international: bool = False
    optout_role_id: Snowflake = 0
    category_id: Snowflake | None = 0
    hours_before_kickoff: int = 0
    hours_after_kickoff: int = 0
    created_by: Snowflake = None
    created_at: datetime = None
    lastmodified_by: Snowflake | None = None
    lastmodified_at: datetime | None = None


    class Competition:
        arbitrary_types_allowed = True

    def __init__(self, bot: Bot):
        super().__init__(bot)

    @classmethod
    async def create(cls: Type["Competition"], bot: Bot) -> "Competition":
        instance = cls(bot)

        return instance

    async def load(self, key: str = 'competition_id', keyval: str | int = None) -> bool:
        if keyval is None or key not in ['competition_id', 'shortname']:
            raise ValueError(f"Can't load competition `{keyval}` using `{key}` field!")
            return False
        else:
            assert self._bot.database, "ERR Competition.py load(): database not available."
            row = await self._bot.database.get_one(
                f"SELECT * FROM competitions WHERE {key} = ?", [keyval]
            )
            if not row:
                return False
            else:
                self.competition_id = int(row["competition_id"])
                self.name = str(row["name"])
                self.shortname = Handle(row["shortname"])
                self.logo_url = HttpUrl(row["logo_url"])
                self.competition_type = Competition_Type(row["competition_type"])
                self.is_monitored = bool(row["is_monitored"])
                self.is_international = bool(row["is_international"])
                self.optout_role_id = int(row["optout_role_id"]) if row["optout_role_id"] is not None else 0
                self.category_id = int(row["category_id"])
                self.hours_before_kickoff = int(row["hours_before_kickoff"])
                self.hours_after_kickoff = int(row["hours_after_kickoff"])
                if row["created_by"] is not None:
                    self.created_by = int(row["created_by"])
                if row["created_at"] is not None:
                    self.created_at = datetime.fromtimestamp(int(row["created_at"]))
                if row["lastmodified_by"] is not None:
                    self.lastmodified_by = int(row["lastmodified_by"])
                if row["lastmodified_at"] is not None:
                    self.lastmodified_at = datetime.fromtimestamp(int(row["lastmodified_at"]))

        return True


    async def load_by_key(self, key: str = None) -> bool:
        try:
            if key.isdigit():
                return await self.load_by_id(int(key))
            else:
                return await self.load_by_shortname(str(key))
        except Exception as e:
            raise ValueError(e)
            return False


    async def load_by_id(self, competition_id: int = 0) -> bool:

        try:
            return await self.load('competition_id', int(competition_id))
        except Exception as e:
            raise ValueError(e)
            return False


    async def add(self) -> bool:

        try:
            await self._bot.database.insert(
                "INSERT INTO competitions (name, shortname, logo_url, competition_type, is_monitored, is_international, optout_role_id, category_id, hours_before_kickoff, hours_after_kickoff, created_at, created_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [str(self.name), str(self.shortname), str(self.logo_url), str(self.competition_type), int(self.is_monitored), int(self.is_international), int(self.optout_role_id), int(self.category_id), int(self.hours_before_kickoff), int(self.hours_after_kickoff), int(self.created_at), int(self.created_by)]
                )

            self.competition_id = int(self._bot.database.lastrowid())

            await self._bot.database.connection.commit()

            return True
        except Exception as e:
            raise ValueError(e)
            return False


    async def update(self, field: str = None, value: Any = None)-> bool:
        if not field:
            return False

        try:
            assert self._bot.database, "ERR Competition.update(): database not available."

            cast_value = self.cast_value(field, value)
            setattr(self, field, cast_value)

            if self.is_type(field, bool):
                value = int(getattr(self, field))
            elif self.is_type(field, int):
                value = int(getattr(self, field))
            elif self.is_type(field, str):
                value = str(getattr(self, field))
            elif self.is_type(field, Snowflake):
                value = int(getattr(self, field))
            elif self.is_type(field, datetime):
                value = (getattr(self, field)).timestamp()
            elif self.is_type(field, Handle):
                value = str(getattr(self, field))
            elif self.is_type(field, HttpUrl):
                value = str(getattr(self, field))
            elif self.is_type(field, Competition_Type):
                value = str(getattr(self, field))
            else:
                raise ValueError(f"ERR Competition.update(): unknown type for field `{field}`")


            await self._bot.database.update(
                f"UPDATE competitions SET {field} = ? WHERE competition_id = ?", [value, self.competition_id]
            )
            return True
        except Exception as e:
            raise ValueError(e)
            return False


    async def remove(self) -> bool:

        try:
            await self._bot.database.delete("DELETE FROM competitions WHERE competition_id = ?", [int(self.competition_id)])

            # fixme : check for active, pending matches ?

            self.competition_id = 0
            self.name = None
            self.shortname = None
            self.is_monitored = False
            self.is_international = False
            self.optout_role_id = 0
            self.category_id = 0
            self.hours_before_kickoff = 0
            self.hours_after_kickoff = 0
            self.created_at = 0
            self.created_by = None
            self.lastmodified_at = None
            self.lastmodified_by = None

            return True
        except Exception as e:
            raise ValueError(e)
            return False


    async def list(self) -> list[dict[str, Any]] | bool:
        try:
            assert self._bot.database, "ERR Competition.list(): database not available."

            data = []

            rows = await self._bot.database.select(
                "SELECT * FROM competitions ORDER by shortname ASC"
            )
            if not rows:
                return data
            else:
                for row in rows:
                    row["competition_id"] = int(row["competition_id"])
                    row["name"] = str(row["name"])
                    row["shortname"] = Handle(row["shortname"])
                    row["logo_url"] = HttpUrl(row["logo_url"])
                    row["competition_type"] = Competition_Type(row["competition_type"])
                    row["is_monitored"] = bool(row["is_monitored"])
                    row["is_international"] = bool(row["is_international"])
                    row["optout_role_id"] = int(row["optout_role_id"]) if row["optout_role_id"] is not None else 0
                    row["category_id"] = int(row["category_id"])
                    row["hours_before_kickoff"] = int(row["hours_before_kickoff"])
                    row["hours_after_kickoff"] = int(row["hours_after_kickoff"])
                    if row["created_by"] is not None:
                        row["created_by"] = int(row["created_by"])
                    if row["created_at"] is not None:
                        row["created_at"] = datetime.fromtimestamp(int(row["created_at"]))
                    if row["lastmodified_at"] is not None:
                        row["lastmodified_at"] = datetime.fromtimestamp(int(row["lastmodified_at"]))
                    if row["lastmodified_by"] is not None:
                        row["lastmodified_by"] = int(row["lastmodified_by"])

            return rows
        except:
            raise ValueError(e)
            return False
                
    def get(self, field: str = None) -> str | bool:
        pass

    def is_loaded(self) -> bool:
        if self.competition_id == 0:
            return False
        else:
            return True


    async def load_by_shortname(self, shortname: Handle = None):
        return await self.load('shortname', str(shortname))

        return False


    async def is_shortname_unique(self, shortname: Handle = None) -> bool:

        comp = Competition(self._bot)

        await comp.load_by_shortname(shortname)

        if comp.is_loaded():
            return comp.competition_id
        else:
            return False


