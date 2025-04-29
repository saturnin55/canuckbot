# db_utils.py
import sqlite3

DB_PATH = 'database/database.db'  # Path to your SQLite database

def connect_db():
    return sqlite3.connect(DB_PATH)

def is_user_manager(user_id):
    try:
        conn = connect_db()
    except aiosqlite.Error as e:
        print(f"{e}")

    cursor = conn.cursor()
    cursor.execute('SELECT userid FROM managers WHERE userid = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result is not None:
        return result
    else:
        return False

    return result is not None

