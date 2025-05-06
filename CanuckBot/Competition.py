from datetime import date
from pydantic import HttpUrl, BaseModel, Field, TypeAdapter, PrivateAttr
from typing import Type, List, Any, Optional
from discord.ext.commands import Bot
from CanuckBot import CanuckBotBase
from CanuckBot.types import Handle, HexColor, DiscordRoleId, DiscordCategoryId, Competition_Type
from Discord.types import DiscordRoleId, DiscordCategoryId


class Competition(CanuckBotBase):
    competition_id: int = 0
    name: str | None = Field(default=None)
    shortname: Handle | None = None
    logo_url: HttpUrl = "https://raw.githubusercontent.com/saturnin55/CanuckBot/main/images/1x1-transparent.png"
    color: HexColor = "#ffffff"
    competition_type: Competition_Type = Competition_Type.Men
    is_monitored: bool = False
    is_international: bool = False
    optout_role_id: DiscordRoleId = 0
    category_id: DiscordCategoryId = 0
    hours_before_kickoff: int = 0
    hours_after_kickoff: int = 0
    created_at: date | None = Field(default=None)

    class Competition:
        arbitrary_types_allowed = True

    def __init__(self, bot: Bot):
        super().__init__(bot)

    @classmethod
    async def create(cls: Type["Competition"], bot: Bot) -> "Competition":
        instance = cls(bot)

        return instance

    async def load_by_id(self, competition_id: int = 0):
        pass

    async def load_by_handle(self, handle: Handle = None):
        pass

    async def update(self, field: str = None, value: Any = None)-> bool:
        pass

    def get(self, field: str = None) -> str | bool:
        pass

    async def list(self) -> List[dict] | bool:
        pass
