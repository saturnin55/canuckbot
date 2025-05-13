"""
Copyright © Krypton 2019-Present - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized Discord bot in Python

Version: 6.2.0
"""

from typing import Any, Literal, Optional

import aiosqlite


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection
        self.connection.row_factory = aiosqlite.Row

    async def get_one(self, sql: str, values: list) -> dict[str, Any] | Literal[False]:
        try:
            rows = await self.select(sql, values)
            if not rows or len(rows) < 1:
                return False
            else:
                return rows[0]
        except aiosqlite.Error as e:
            print(f"ERR Database.get_one(): {e}")
            return False

    async def delete(self, sql: str, values: Optional[list] = None) -> bool:
        try:
            async with self.connection.execute(sql, values) as cursor:
                await self.connection.commit()
                if cursor.rowcount > 0:
                    return True
                else:
                    return False
        except aiosqlite.Error as e:
            print(f"ERR Database.delete(): {e}")
            return False

    async def select(
        self, sql: str, values: Optional[list] = None
    ) -> list[dict[str, Any]] | Literal[False]:
        try:
            async with self.connection.execute(sql, values) as cursor:
                rows = await cursor.fetchall()
                items = [dict(row) for row in rows]
                if len(items) > 0:
                    return items
                else:
                    return False
        except aiosqlite.Error as e:
            print(f"ERR Database.select(): {e}")
            return False

    async def update(self, sql: str, values: list) -> bool:
        try:
            print(f"SQL : |{sql}")
            print(f"values : |{values}")
            async with self.connection.execute(sql, values) as cursor:
                await self.connection.commit()

                if cursor.rowcount > 0:
                    return True
                else:
                    return False
        except aiosqlite.Error as e:
            formatted_sql = sql.replace("?", "{}").format(
                *[repr(p) for p in [sql, values]]
            )
            print(f"ERR Database.update(): {e}, query : |{formatted_sql}|")
            return False

    async def insert(self, sql: str, values: list) -> bool:
        try:
            async with self.connection.execute(sql, values) as cursor:
                await self.connection.commit()
                if cursor.rowcount > 0:
                    return True
                else:
                    return False
        except aiosqlite.Error as e:
            print(f"ERR Database.insert(): {e}")
            return False

    async def mngr_add(self, user_id: int, invoking_user: int) -> None:
        print(user_id)
        rows = await self.connection.execute(
            "SELECT user_id FROM managers WHERE user_id=? ORDER BY user_id DESC LIMIT 1",
            (user_id,),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            if result is not None:
                return
            await self.connection.execute(
                "INSERT INTO managers(user_id, created_at, created_by) VALUES (?, CURRENT_TIMESTAMP, ?)",
                (
                    user_id,
                    invoking_user,
                ),
            )
            await self.connection.commit()
