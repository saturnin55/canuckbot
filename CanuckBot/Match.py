import time
from enum import Enum
from datetime import date, datetime
from typing import List, Type, Any, Optional
from pydantic import HttpUrl
from CanuckBot import CanuckBotBase
from CanuckBot.types import Match_Status, TimeZone
from Discord.types import Snowflake
from CanuckBot.utils import is_valid_handle
from Discord.DiscordBot import DiscordBot


class MATCH_FIELDS_INFO(str, Enum):
    match_id = "match_id"
    home_id = "home_id"
    away_id = "away_id"
    competition_id = "competition_id"
    status = "status"
    kickoff_at = "kickoff_at"
    venue = "venue"
    description = "description"
    channel_id = "channel_id"
    hours_before_kickoff = "hours_before_kickoff"
    hours_after_kickoff = "hours_after_kickoff"
    watch = "watch"
    stream = "stream"
    created_by = "created_by"
    created_at = "created_at"
    lastmodified_by = "lastmodified_by"
    lastmodified_at = "lastmodified_at"

class MATCH_FIELDS_EDITABLE(str, Enum):
    home_id = "home_id"
    away_id = "away_id"
    competition_id = "competition_id"
    status = "status"
    kickoff_at = "kickoff_at"
    venue = "venue"
    description = "description"
    channel_id = "channel_id"
    hours_before_kickoff = "hours_before_kickoff"
    hours_after_kickoff = "hours_after_kickoff"
    watch = "watch"
    stream = "stream"

class Match(CanuckBotBase):
    match_id: int
    home_id: int | None = None
    away_id: int | None = None
    competition_id: int
    status: Match_Status = Match_Status.Pending
    kickoff_at: datetime = 0
    venue: str | None = None
    description: str = None
    channel_id: Snowflake = 0
    info_msg_id: Snowflake = 0
    hours_before_kickoff: int = 0
    hours_after_kickoff: int = 0
    watch: str | None = None
    stream: HttpUrl | None = None
    created_by: Snowflake = 0
    created_at: datetime = 0
    lastmodified_by: Snowflake | None = None
    lastmodified_at: datetime | None = None

    class Match:
        arbitrary_types_allowed = True

    def __init__(self, bot: DiscordBot, **kwargs):
        super().__init__(bot, **kwargs)


    @classmethod
    async def create(cls: Type["Match"], bot: DiscordBot) -> "Match":
        instance = cls(bot)
        return instance


    @classmethod
    async def create(cls: Type["Match"], bot: DiscordBot) -> "Match":
        instance = cls(bot)
        return instance

    async def get(self, match_id: Optional[int] = None) -> bool:
        if match_id is None:
            return False
        else:
            try:
                assert self._bot.database, "ERR Match.py get(): database not available."
                row = await self._bot.database.get_one(
                    "SELECT * FROM matches WHERE match_id = ?", [str(match_id)]
                )

                if not row:
                    return False
                else:
                    self.match_id = int(row["match_id"])
                    self.home_id = int(row["home_id"])
                    self.away_id = int(row["away_id"])
                    self.competition_id = int(row["competition_id"])
                    self.status = int(row["status"])
                    self.kickoff_at = datetime.fromtimestamp(int(row["kickoff_at"]))
                    self.venue = str(row["venue"])
                    self.description = str(row["description"])
                    self.channel_id = int(row["channel_id"])
                    self.info_msg_id = int(row["info_msg_id"])
                    self.hours_before_kickoff = int(row["hours_before_kickoff"])
                    self.hours_after_kickoff = int(row["hours_after_kickoff"])
                    self.watch = str(row["watch"])
                    self.stream = str(row["watch"])
                    self.created_at = datetime.fromtimestamp(int(row["created_at"]))
                    self.created_by = int(row["created_by"])
                    self.lastmodified_at = datetime.fromtimestamp(int(row["lastmodified_at"]))
                    self.lastmodified_by = int(row["lastmodified_by"])

            except Exception as e:
                raise ValueError(e)
                return False

        return True


    def is_loaded(self) -> bool:
        if self.match_id == 0:
            return False
        else:
            return True


    async def load(self, key: str = 'team_id', keyval: str | int = None) -> bool:
            if keyval is None or key not in ['match_id']:
                raise ValueError(f"Can't load match `{keyval}` using `{key}` field!")
                return False
            else:
                try:
                    return await self.load(int(keyval))
                except Exception as e:
                    raise ValueError(f"Can't load match `{keyval}` using `{key}` field!")
                    return False

    async def load_by_id(self, team_id: int = 0) -> bool:
        try:
            return await self.load(int(keyval))
        except Exception as e:
            raise ValueError(f"Can't load match `{keyval}` using `{key}` field!")
            return False

    async def update(self, field: str = None, value: Any = None)-> bool:
        if not field:
            return False

        try:
            assert self._bot.database, "ERR Match.update(): database not available."

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
            elif self.is_type(field, Match_Status):
                value = (getattr(self, field)).value
            elif self.is_type(field, TimeZone):
                value = str(getattr(self, field))
            else:
                raise ValueError(f"ERR Match.update(): unknown type for field `{field}`")

            await self._bot.database.update(
                f"UPDATE matches SET {field} = ? WHERE match_id = ?", [value, self.match_id]
            )
            return True
        except Exception as e:
            raise ValueError(e)
            return False


    async def remove(self) -> bool:

        try:
            await self._bot.database.delete("DELETE FROM matches WHERE match_id = ?", [int(self.match_id)])

            self.match_id = 0
            self.home_id = None
            self.away_id = None
            self.competition_id = None
            self.status = Match_Status.Pending
            self.kickoff_at = 0
            self.venue = None
            self.description = None
            self.channel_id = 0
            self.info_msg_id = 0
            self.hours_before_kickoff = 0
            self.hours_after_kickoff = 0
            self.watch = None
            self.stream = None
            self.created_at = 0
            self.created_by = 0
            self.lastmodified_at = None
            self.lastmodified_by = None

            return True
        except Exception as e:
            raise ValueError(e)
            return False


    async def add(self) -> bool:

        try:
            await self._bot.database.insert(
                "INSERT INTO matches (home_id, away_id, competition_id, status, kickoff_at, "
                    "hours_before_kickoff, hours_after_kickoff, created_at, created_by) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                [int(self.home_id), int(self.away_id), int(self.competition_id), int(self.status), int(self.kickoff_at), int(self.hours_before_kickoff), int(self.hours_after_kickoff), int(self.created_at), int(self.created_by)]
                )

            self.match_id = int(self._bot.database.lastrowid())

            await self._bot.database.connection.commit()

            return True
        except Exception as e:
            raise ValueError(e)
            return False


    # check if there is a match already existing between the 2 teams on that day
    async def is_match_exists(self, home_id:int = None, away_id:int = None, competition_id:int = None, kickoff_at:int = None) -> bool:
        pass


    async def setmodified(self) -> bool:
        try:
            await self.update('lastmodified_by', self.lastmodified_by)
            await self.update('lastmodified_at', int(time.time()))
            return True
        except Exception as e:
            raise ValueError(e)
            return False


    async def search(self, criteria: str = None) -> list[dict[str, Any]] | bool:
        data = []

        if not criteria:
            return data

        rows = await self._bot.database.select(
            "SELECT *"
            "FROM matches"
            "WHERE ",
            [str(criteria)]
        )

        if not rows:
            return data
        else:
            for row in rows:
                row["match_id"] = int(row["match_id"])
                row["home_id"] = int(row["home_id"])
                row["away_id"] = int(row["away_id"])
                row["competition_id"] = int(row["competition_id"])
                row["status"] = int(row["status"])
                row["kickoff_at"] = datetime.fromtimestamp(int(row["kickoff_at"]))

                row["venue"] = str(row["venue"])
                row["description"] = str(row["description"])

                if row["channel_id"] is not None:
                    row["channel_id"] = int(row["channel_id"])
                else:
                    row["channel_id"] = None

                if row["info_msg_id"] is not None:
                    row["info_msg_id"] = int(row["info_msg_id"])
                else:
                    row["info_msg_id"] = None

                row["hours_before_kickoff"] = int(row["hours_before_kickoff"])
                row["hours_after_kickoff"] = int(row["hours_after_kickoff"])
                row["watch"] = str(row["watch"])
                row["stream"] = str(row["watch"])

                if row["created_at"] is not None:
                    row["created_at"] = datetime.fromtimestamp(int(row["created_at"]))
                if row["created_by"] is not None:
                    row["created_by"] = int(row["created_by"])
                if row["lastmodified_at"] is not None:
                    row["lastmodified_at"] = datetime.fromtimestamp(int(row["lastmodified_at"]))
                if row["lastmodified_by"] is not None:
                    row["lastmodified_by"] = int(row["lastmodified_by"])

            return rows
        except Exception as e:
            raise ValueError(e)
            return False

        
    async def generate_channel_topic(self) -> str:
        pass


    async def generate_channel_name(self) -> str:
        pass
