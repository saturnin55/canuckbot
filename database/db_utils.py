# db_utils.py
import os
from pathlib import Path
from CanuckBot.types import User_Level, DiscordUserId
from database import DatabaseManager


#def connect_db():
#    db_path = os.getenv("DB_PATH")
#    if not db_path:
#        raise EnvironmentError(
#            "DB_PATH environment variable is not set. Check your .env file."
#        )
#
#    path = Path(db_path)
#    if not path.exists():
#        raise FileNotFoundError(f"Database file not found at: {db_path}")
#
#    return sqlite3.connect(db_path)


def is_user_manager(db: DatabaseManager = None, user_id: DiscordUserId = None, level: User_Level = User_Level.Superadmin):
    # fixme need to convert this to aiosqlite and use the DatabaseManager
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM managers WHERE user_id = ? AND access_level <= ?", (user_id, level.value))
        result = cursor.fetchone()
        conn.close()

        if result is not None:
            return result
        else:
            return False
    except sqlite3.Error as e:
        print(f"{e}")
