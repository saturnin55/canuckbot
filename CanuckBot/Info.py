from . import CanuckBotBase
from pydantic import BaseModel, Field, TypeAdapter, PrivateAttr
from typing import get_type_hints, Any, Type
from discord.ext.commands import Bot

class Info(CanuckBotBase):
    info_id: int = None
    obj: str = None
    field: str = None
    info: str = None

    def __init__(self, bot: Bot = None):
        super().__init__(bot)

    @classmethod
    async def create(cls: Type["Info"], bot: Bot, obj: str = None, field: str = None) -> "Info":
        instance = Info(bot)
        instance.obj = obj
        instance.field = field
        instance.info = ""
        row = await instance.get()

        if not row:
            return instance

        instance.info_id = row["info_id"]
        instance.obj = row["obj"]
        instance.field = row["field"]
        instance.info = row["info"]

        return instance

    async def get(self) -> str | bool:
        if self.field is None:
            return False

        row = await self._bot.database.get_one(
            "SELECT * FROM info WHERE obj = ? AND field = ?", [str(self.obj), str(self.field)]
        )
        if not row:
            return False
        else:
            return row

    async def set(self, info) -> bool:
        if info is None:
            info = ""

        if self.info_id is None:
            ret = await self._bot.database.insert(
                "INSERT INTO info (info, obj, field) VALUES (?, ?, ?)",
                [str(info), str(self.obj), str(self.field)],
            )
        else:
            ret = await self._bot.database.update(
                "UPDATE info SET info = ? WHERE info_id = ?", [str(info), int(self.info_id)]
            )

        if ret:
            self.info = info
            return True
        else:
            return False
