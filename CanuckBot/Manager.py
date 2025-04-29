import aiosqlite
from . import CanuckBotBase
from CanuckBot.constants import *

class Manager(CanuckBotBase):
    obj = "manager"
    FIELDS = { 'userid':    { 'type': TYPE_DISCORD_USERID },
               'dt_added':  { 'type': TYPE_TIMESTAMP },
               'added_by':  { 'type': TYPE_DISCORD_USERID }
            }

    def __init__(self, bot):
        super().__init__(bot)
        self.data = {}

    @classmethod
    async def create(cls, bot):
        instance = Manager(bot)
        return instance

    async def get(self, userid=None) -> bool:
        if userid is None:
            return False
        else:
            row = await self.database.get_one("SELECT * FROM managers WHERE userid = ?", [userid])
            if not row:
                return False
            else:
                self.data["userid"] = int(row['userid'])
                self.data["dt_added"] = int(row['dt_added'])
                self.data["added_by"] = int(row['added_by'])

                return True

    async def add(self, userid, invoking_id) -> bool:

        user = await self.database.get_one("SELECT * FROM managers WHERE userid = ?", [userid])

        if user:
            # user already exists in managers table
            return False
        else:
            try:
                await self.database.insert("INSERT INTO managers(userid, dt_added, added_by) VALUES (?, CURRENT_TIMESTAMP, ?)", 
                    (userid, invoking_id))
                await self.database.connection.commit()
    
                self.data["userid"] = int(userid)
                self.data["dt_added"] = ""
                self.data["added_by"] = int(invoking_id)

                return True
            except aiosqlite.Error as e:
                print(f"ERR Manager.add(): {e}")
                return False
            
        return True

    async def remove(self, userid) -> bool:
        user = await self.database.get_one("SELECT * FROM managers WHERE userid = ?", [userid])

        if not user:
            # user doesn't exists in managers table
            return True
        else:
            try:
                await self.database.delete("DELETE FROM managers WHERE userid = ?", [int(userid)])
                await self.database.connection.commit()

                return True
            except aiosqlite.Error as e:
                print(f"ERR Manager.add(): {e}")
                return False
            
        return True

    async def list(self) -> [dict, bool]:
        try:
            rows = await self.bot.database.select("SELECT userid, strftime('%s', dt_added) as dt_added, added_by \
                                                   FROM managers \
                                                   ORDER BY dt_added ASC")
            if not rows:
                return False
            else:
                for row in rows:
                    row['userid'] = int(row['userid'])
                    row['dt_added'] = int(row['dt_added'])
                    row['added_by'] = int(row['added_by'])
                return rows
        except aiosqlite.Error as e:
            print(f"ERR Manager.get_all(): {e}")
            return False
