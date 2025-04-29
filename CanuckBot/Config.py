import CanuckBot
from CanuckBot.constants import (
    TYPE_COLOR,
    TYPE_DISCORD_CATEGORYID,
    TYPE_DISCORD_CHANNELID,
    TYPE_DISCORD_ROLEID,
    TYPE_INT,
    TYPE_STRING,
    TYPE_URL,
)

from . import CanuckBotBase


class Config(CanuckBotBase):
    obj = "config"
    FIELDS = {
        "channel_cmds": {"type": TYPE_DISCORD_CHANNELID},
        "channel_logs": {"type": TYPE_DISCORD_CHANNELID},
        "default_category": {"type": TYPE_DISCORD_CATEGORYID},
        "default_color": {"type": TYPE_COLOR},
        "default_create_before": {"type": TYPE_INT},
        "default_delete_after": {"type": TYPE_INT},
        "default_kickoff_warning": {"type": TYPE_INT},
        "default_logo": {"type": TYPE_URL},
        "default_tz": {"type": TYPE_STRING},
        "mngr_roleid": {"type": TYPE_DISCORD_ROLEID},
    }

    def __init__(self, bot):
        super().__init__(bot)
        self.data = {}

    @classmethod
    async def create(cls, bot):
        instance = Config(bot)
        instance.data = await instance.list()
        return instance

    async def update(self, field, value) -> bool:
        value = CanuckBot.get_field_value(self.get_field_type(field), value)
        if not CanuckBot.is_valid_type(self.get_field_type(field), value):
            return False
        return await self.bot.database.update(
            "UPDATE config SET value = ? WHERE field = ?", [value, field]
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
