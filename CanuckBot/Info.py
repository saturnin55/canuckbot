import aiosqlite
import CanuckBot

class Info():
    bot = None
    id_info = None
    obj = None
    field = None
    value = None

    def __init__(self, bot):
        self.bot = bot

    @classmethod
    async def create(cls, bot, obj, field):
        instance = Info(bot)
        instance.obj = obj
        instance.field = field
        instance.info = ""
        row = await instance.get()

        if not row:
            return instance

        instance.id_info = row["id_info"]
        instance.obj = row["obj"]
        instance.field = row["field"]
        instance.info = row["info"]

        return instance

    async def get(self) -> [str, bool]:
        if self.field is None:
            return False

        row = await self.bot.database.get_one(f"SELECT * FROM info WHERE obj = ? AND field = ?", [self.obj, self.field])
        if not row:
            return False
        else:
            return row

    async def set(self, info) -> bool:
        if info is None:
            info = ""

        if self.id_info is None:
            ret = await self.bot.database.insert(f"INSERT INTO info (info, obj, field) VALUES (?, ?, ?)", [info, self.obj, self.field])
        else:
            ret =  await self.bot.database.update(f"UPDATE info SET info = ? WHERE id_info = ?", [info, self.id_info])

        if ret:
            self.info = info
            return True
        else:
            return False
