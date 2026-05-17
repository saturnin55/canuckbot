# db_utils.py
import os
import sqlite3
from pathlib import Path
from typing import Any, Literal
from CanuckBot.types import User_Level
from Discord.types import Snowflake
from database import DatabaseManager


async def is_user_manager(db: DatabaseManager, user_id: int, level: User_Level = User_Level.Superadmin) -> dict[str, Any] | Literal[False]:
    try:
        row = await db.get_one("SELECT user_id FROM managers WHERE user_id = ? AND level <= ?", [user_id, level.value])

        if not row:
            return False
        else:
            return row

    except sqlite3.Error as e:
        print(f"{e}")
        return False
