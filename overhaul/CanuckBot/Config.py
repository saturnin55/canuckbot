import CanuckBot
from . import CanuckBotBase
from .types import SnowflakeId
from .TimeZone import TimeZone


class Config(CanuckBotBase):
    obj = "config"

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

    async def update(self, field, value) -> bool:
        return await self.bot.database.update(
            "UPDATE config SET value = ? WHERE field = ?", [str(value), str(field)]
        )

    async def get(self, field=None) -> str | bool:
        if self.data.get(field) is None:
            return False
        else:
            return self.data.get(field)

    async def list(self) -> list | bool:
        rows = await self.bot.database.select("SELECT * FROM config ORDER BY field ASC")

        if not rows:
            return False
        else:
            for item in rows:
                self.data[item["field"]] = item["value"]
            return self.data
