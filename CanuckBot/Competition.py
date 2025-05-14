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
    created_at: date = None
    lastmodified_by: Snowflake | None = None
    lastmodified_at: date | None = None


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
                return await self.load_by_handle(str(key))
        except Exception as e:
            raise ValueError(e)
            return False

    async def load_by_id(self, competition_id: int = 0) -> bool:

        try:
            return await self.load('competition_id', int(competition_id))
        except Exception as e:
            raise ValueError(e)
            return False


    async def load_by_handle(self, shortname: Handle = None) -> bool:
        try:
            return await self.load('shortname', str(shortname))
        except Exception as e:
            raise ValueError(e)
            return False

    async def update(self, field: str = None, value: Any = None)-> bool:
        pass

    async def list(self) -> list[dict[str, Any]] | bool:
        try:
            assert self._bot.database, "ERR Competition.list(): database not available."

            data = []

            rows = await self._bot.database.select(
                "SELECT * FROM competitions ORDER by is_international DESC, shortname ASC"
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
            print(f"ERR Competition.liste()")
            return False
                
    def get(self, field: str = None) -> str | bool:
        pass

    async def list(self) -> List[dict] | bool:
        pass

    def is_loaded(self) -> bool:
        if self.competition_id == 0:
            return False
        else:
            return True
