# db_utils.py
import os
import sqlite3
from pathlib import Path


def connect_db():
    db_path = os.getenv("DB_PATH")
    if not db_path:
        raise EnvironmentError(
            "DB_PATH environment variable is not set. Check your .env file."
        )

    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"Database file not found at: {db_path}")

    return sqlite3.connect(db_path)


def is_user_manager(user_id):
    # fixme need to convert this to aiosqlite and use the DatabaseManager
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM managers WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result is not None:
            return result
        else:
            return False
    except sqlite3.Error as e:
        print(f"{e}")
