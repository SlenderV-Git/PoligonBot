import sqlite3
from aiogram.handlers import message

def give_users_list(db_path):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT telegram_id FROM users_list")
        return [item[0] for item in cur.fetchall()]

def set_user_data(db_path, message : message):
    with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS users_list (id INTEGER PRIMARY KEY, username TEXT, telegram_id INTEGER, page INTEGER)")
            values = (message.from_user.username, message.from_user.id, 1)
            cur.execute("INSERT INTO users_list (username, telegram_id, page) VALUES (?, ?, ?)", values)
            conn.commit()
    
def set_data(db_path, item, value, id):
     with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"UPDATE users_list SET {item} = {value} WHERE telegram_id = {id}")
        conn.commit()

def get_data(db_path, item, id):
     with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT {item} FROM users_list WHERE telegram_id = {id}")
        return cur.fetchone()[0]

'''def create_bookmarks(db_path):
     with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS bookmark (bookmark_id INTEGER PRIMARY KEY, num_page INTEGER, telegram_id INTEGER)")
        conn.commit()

def add_bookmarks(db_path, page, id):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO bookmark (num_page, telegram_id) VALUES ({page}, {id})")
        conn.commit()

def get_bookmark(db_path, page, id):
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT num_page FROM bookmark GROUP BY telegram_id")
        conn.commit()'''