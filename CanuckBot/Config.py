from typing import Any, Literal, Optional, Type
from enum import Enum
from pydantic import HttpUrl
from Discord.DiscordBot import DiscordBot
from CanuckBot import CanuckBotBase
from CanuckBot.types import HexColor, TimeZone, Log_Level
from Discord.types import Snowflake
import logging

class CONFIG_FIELDS_INFO(str, Enum):
    logs_channel_id = "logs_channel_id"
    cmds_channel_id = "cmds_channel_id"
    interval_cleanup_task = "interval_cleanup_task"
    interval_status_task = "interval_status_task"
    interval_match_task = "interval_match_task"
    interval_ = "cmds_channel_id"
    default_add_hours_before = "default_add_hours_before"
    default_del_hours_after = "default_del_hours_after"
    default_category_id = "default_category_id"
    default_logo_url = "default_logo_url"
    default_tz = "default_tz"
    mngr_role_id = "mngr_role_id"
    log_level = "log_level"
    optout_all_role_id = "optout_all_role_id"

class CONFIG_FIELDS_EDITABLE(str, Enum):
    logs_channel_id = "logs_channel_id"
    cmds_channel_id = "cmds_channel_id"
    interval_cleanup_task = "interval_cleanup_task"
    interval_status_task = "interval_status_task"
    interval_match_task = "interval_match_task"
    interval_ = "cmds_channel_id"
    default_add_hours_before = "default_add_hours_before"
    default_del_hours_after = "default_del_hours_after"
    default_category_id = "default_category_id"
    default_logo_url = "default_logo_url"
    default_tz = "default_tz"
    mngr_role_id = "mngr_role_id"

class Config(CanuckBotBase):
    logs_channel_id: Snowflake = 0
    cmds_channel_id: Snowflake = 0
    interval_cleanup_task: float = 0
    interval_status_task: float = 0
    interval_match_task: float = 0
    default_add_hours_before: int = 0
    default_del_hours_after: int = 0
    default_category_id: Snowflake = 0
    default_logo_url: HttpUrl = HttpUrl(
        "https://raw.githubusercontent.com/saturnin55/CanuckBot/main/images/1x1-transparent.png"
    )
    default_tz: TimeZone = TimeZone("America/Toronto")
    mngr_role_id: Snowflake = 0
    log_level: Log_Level = logging.INFO
    optout_all_role_id: Snowflake = 0

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, bot: DiscordBot, **kwargs):
        super().__init__( bot=bot, **kwargs)

    @classmethod
    async def create(cls: Type["Config"], bot: DiscordBot) -> "Config":
        instance = cls(bot)
        await instance.list()

        return instance

    async def reload(self):
        self.list

    async def update(self, field: str) -> bool:
        ret: bool
    
        try:
            assert self._bot.database, "ERR Config.py update(): database not available."
            ret = await self._bot.database.update(
                "UPDATE config SET value = ? WHERE field = ?",
                [str(getattr(self, field, None)), str(field)],
            )
        except Exception as e:
            raise ValueError(e)
            return False
 
        return ret

    async def get(self, field: Optional[str] = None) -> str | Literal[False]:
        try:
            value = getattr(self, field, None) if field else False
        except Exception as e:
            raise ValueError(e)
            return False

        return value or False

    async def list(self) -> dict[str, Any] | Literal[False]:
        data: dict[str, Any] = {}

        try:
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
        except Exception as e:
            raise ValueError(e)
            return False

            return data
