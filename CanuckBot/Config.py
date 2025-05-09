from typing import Any, Literal, Optional, Type
from enum import Enum
from pydantic import HttpUrl
from Discord.DiscordBot import DiscordBot
from CanuckBot import CanuckBotBase
from CanuckBot.types import HexColor, TimeZone
from Discord.types import DiscordChannelId, DiscordCategoryId, DiscordRoleId

class CONFIG_FIELDS_EDITABLE(str, Enum):
    logs_channel_id = "logs_channel_id"
    cmds_channel_id = "cmds_channel_id"
    default_add_hours_before = "default_add_hours_before"
    default_del_hours_after = "default_del_hours_after"
    default_category_id = "default_category_id"
    default_logo_url = "default_logo_url"
    default_tz = "default_tz"
    mngr_role_id = "mngr_role_id"
    default_comp_color = "default_comp_color"

class Config(CanuckBotBase):
    logs_channel_id: DiscordChannelId = 0
    cmds_channel_id: DiscordChannelId = 0
    default_add_hours_before: int = 0
    default_del_hours_after: int = 0
    default_category_id: DiscordCategoryId = 0
    default_logo_url: HttpUrl = HttpUrl(
        "https://raw.githubusercontent.com/saturnin55/CanuckBot/main/images/1x1-transparent.png"
    )
    default_tz: TimeZone = TimeZone("America/Toronto")
    mngr_role_id: DiscordRoleId = 0
    default_comp_color: HexColor = "#ffffff"
    optout_all_role_id: DiscordRoleId = 0

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, bot: DiscordBot, **kwargs):
        super().__init__( bot=bot, **kwargs)

    @classmethod
    async def create(cls: Type["Config"], bot: DiscordBot) -> "Config":
        instance = cls(bot)
        await instance.list()

        return instance

    async def update(self, field: str) -> bool:
        ret: bool
        assert self._bot.database, "ERR Config.py update(): database not available."
        ret = await self._bot.database.update(
            "UPDATE config SET value = ? WHERE field = ?",
            [str(getattr(self, field, None)), str(field)],
        )
        return ret

    async def get(self, field: Optional[str] = None) -> str | Literal[False]:
        value = getattr(self, field, None) if field else False

        return value or False

    async def list(self) -> dict[str, Any] | Literal[False]:
        data: dict[str, Any] = {}
        assert self._bot.database, "ERR Config.py list(): database not available."
        rows = await self._bot.database.select(
            "SELECT * FROM config ORDER BY field ASC"
        )

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
