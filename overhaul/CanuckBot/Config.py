import CanuckBot
from typing import get_type_hints, Any
from . import CanuckBotBase
from .types import SnowflakeId
from .TimeZone import TimeZone


class Config(CanuckBotBase):

    channel_logs = SnowflakeId
    channel_cmd = SnowflakeId
    default_add_hours_before: int
    default_del_hours_after: int
    default_category_id = SnowflakeId
    default_logo_url = HttpUrl
    default_tz = TimeZone
    mngr_role_id = SnowflakeId
    default_comp_color = HexColor
    optout_all_role_id = SnowflakeId
    
    def __init__(self, bot):
        super().__init__(bot)
        self.data = {}

    @classmethod
    async def create(cls, bot):
        instance = Config(bot)
        instance.data = await instance.list()
        return instance

    async def update(self, field) -> bool:
        ret: bool

        ret = await self.bot.database.update(
            "UPDATE config SET value = ? WHERE field = ?", [str(getattr(self, field, None)), str(field)]
        )
        return ret

    async def get(self, field: str = None) -> str | bool:
        value = getattr(self, field, None)

        if value is None:
            return False
        else:
            return  value

    async def list(self) -> list | bool:
        data: dict[str, Any] = {}

        rows = await self.bot.database.select("SELECT * FROM config ORDER BY field ASC")

        if not rows:
            return False
        else:
            hints = get_type_hints(Config)
            for item in rows:
                expected_type = hints.get(item["field"])
                if expected_type:
                    cast_value = expected_type(item["value"])
                    setattr(self, item["field"], cast_value)
                    data[item["field"]] = cast_value
                else:
                    # fixme: oops
                    pass
            return data
