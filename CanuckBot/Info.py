from typing import Any, Literal, Optional, Type

from CanuckBot import CanuckBotBase


class Info(CanuckBotBase):
    info_id: int
    obj: str
    field: str
    info: str

    def __init__(self, bot):
        super().__init__(bot)

    @classmethod
    async def create(
        cls: Type["Info"], bot, obj: Optional[str] = None, field: Optional[str] = None
    ) -> "Info":
        instance = Info(bot)
        instance.obj = obj or ""
        instance.field = field or ""
        instance.info = ""
        row = await instance.get()

        if not row:
            return instance

        instance.info_id = row["info_id"]
        instance.obj = row["obj"]
        instance.field = row["field"]
        instance.info = row["info"]

        return instance

    async def get(self) -> dict[str, Any] | Literal[False]:
        if self.field is None:
            return False
        assert self._bot.database, "ERR Info.py get(): database not available."
        row = await self._bot.database.get_one(
            "SELECT * FROM info WHERE obj = ? AND field = ?",
            [str(self.obj), str(self.field)],
        )
        if not row:
            return False
        else:
            return row

    async def set(self, info) -> bool:
        if info is None:
            info = ""
        assert self._bot.database, "ERR Info.py set(): database not available."
        if self.info_id is None:
            ret = await self._bot.database.insert(
                "INSERT INTO info (info, obj, field) VALUES (?, ?, ?)",
                [str(info), str(self.obj), str(self.field)],
            )
        else:
            ret = await self._bot.database.update(
                "UPDATE info SET info = ? WHERE info_id = ?",
                [str(info), int(self.info_id)],
            )

        if ret:
            self.info = info
            return True
        else:
            return False
