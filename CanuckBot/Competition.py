import CanuckBot
from CanuckBot.constants import (
    TYPE_BOOL,
    TYPE_COLOR,
    TYPE_DISCORD_CATEGORYID,
    TYPE_DISCORD_ROLEID,
    TYPE_INT,
    TYPE_STRING,
    TYPE_URL,
)

from . import CanuckBotBase


class Competition(CanuckBotBase):
    obj = "competition"
    FIELDS = {
        "id_competition": {"type": TYPE_INT},
        "handle": {"type": TYPE_STRING},
        "name": {"type": TYPE_STRING},
        "flag_active": {"type": TYPE_BOOL},
        "flag_intl": {"type": TYPE_BOOL},
        "category": {"type": TYPE_DISCORD_CATEGORYID},
        "logo": {"type": TYPE_URL},
        "create_before": {"type": TYPE_INT},
        "delete_after": {"type": TYPE_INT},
        "color": {"type": TYPE_COLOR},
        "roleid_optout": {"type": TYPE_DISCORD_ROLEID},
    }

    def __init__(self, bot):
        super().__init__(bot)
        self.data = {}

    @classmethod
    async def create(cls, bot, key: str) -> None:
        instance = Competition(bot)

        if CanuckBot.regex_is_integer(key) and CanuckBot.is_snowflakeid(int(key)):
            id_competition = int(key)
            await instance.load_by_id(id_competition)
            return instance
        else:
            handle = str(key)
            await instance.load_by_handle(handle)
            return instance

        return instance

    async def load_by_id(self, id_competition):
        row = await self.database.get_one(
            "SELECT * FROM competitions WHERE id_competition = ?", [id_competition]
        )
        self.load_data(row)

    async def load_by_handle(self, handle):
        print("x1")
        row = await self.database.get_one(
            "SELECT * FROM competitions WHERE handle = ?", [handle]
        )
        print("x2")
        self.load_data(row)
        print("x3")

    async def update(self, field, value) -> bool:
        value = CanuckBot.get_field_value(self.FIELDS[field]["type"], value)
        if not CanuckBot.is_valid_type(self.FIELDS[field]["type"], value):
            return False
        return await self.bot.database.update(
            "UPDATE config SET value = ? WHERE field = ?", [value, field]
        )

    def get(self, field=None) -> [str, bool]:
        if self.data.get(field) is None:
            return False
        else:
            return self.data.get(field)

    async def list(self) -> [list, bool]:
        rows = await self.bot.database.select("SELECT * FROM config ORDER BY field ASC")

        if not rows:
            return False
        else:
            for item in rows:
                self.data[item["field"]] = item["value"]
            return self.data
