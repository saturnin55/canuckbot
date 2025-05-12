# db_utils.py
import os
from pathlib import Path
from CanuckBot.types import User_Level
from Discord.types import Snowflake
from database import DatabaseManager

async def is_user_manager(db: DatabaseManager = None, user_id: int = None, level: User_Level = User_Level.Superadmin):
    try:
        row = await db.get_one("SELECT user_id FROM managers WHERE user_id = ? AND level <= ?", [user_id, level.value])

        if not row:
            return False
        else:
            return row

    except sqlite3.Error as e:
        print(f"{e}")
