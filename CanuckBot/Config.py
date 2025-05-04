from . import CanuckBotBase
from pydantic import HttpUrl, BaseModel, Field, TypeAdapter, PrivateAttr
from typing import get_type_hints, Any
from .types import SnowflakeId, HexColor
from .TimeZone import TimeZone
from discord.ext.commands import Bot


class Config(CanuckBotBase):

    channel_logs: SnowflakeId = 0
    channel_cmds: SnowflakeId = 0
    default_add_hours_before: int = 0
    default_del_hours_after: int = 0
    default_category_id: SnowflakeId = 0
    default_logo_url: HttpUrl = "https://raw.githubusercontent.com/saturnin55/CanuckBot/main/images/1x1-transparent.png"
    default_tz: TimeZone = "America/Toronto"
    mngr_role_id: SnowflakeId = 0
    default_comp_color: HexColor = "#ffffff"
    optout_all_role_id: SnowflakeId = 0

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, bot):
        super().__init__(bot)

    @classmethod
    async def create(cls, bot):
        instance = cls(bot)
        await instance.list()

        return instance

    async def update(self, field) -> bool:
        ret: bool

        ret = await self._bot.database.update(
            "UPDATE config SET value = ? WHERE field = ?", [
                str(getattr(self, field, None)), str(field)]
        )
        return ret

    async def get(self, field: str = None) -> str | bool:
        value = getattr(self, field, None)

        if value is None:
            return False
        else:
            return value

    async def list(self) -> list | bool:
        data: dict[str, Any] = {}

        rows = await self._bot.database.select("SELECT * FROM config ORDER BY field ASC")

        if not rows:
            return False
        else:
            for item in rows:
                field = item["field"]
                value = item["value"]

                cast_value = self.cast_value(field, value)
                setattr(self, item["field"], cast_value)
                data[item["field"]] = cast_value

        return data
