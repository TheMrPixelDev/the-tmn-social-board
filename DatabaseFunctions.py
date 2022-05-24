import sqlite3

def try_to_create_database():
    with sqlite3.connect("./content.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS polaroids (update_id INTEGER PRIMARY KEY, msg_id INTEGER, file_name TEXT, "
            "message TEXT, sender_name TEXT, sender_id INTEGER)")
        conn.commit()

def get_all_posts():
    with sqlite3.connect("./content.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT file_name, message, sender_name FROM polaroids"
        )
        conn.commit()
        return cursor.fetchall()

def insert_new_post(update_id, msg_id, file_name, caption, sender_name, sender_id):
    with sqlite3.connect("./content.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO polaroids VALUES (?, ?, ?, ?, ?, ?)",
            (update_id, msg_id, file_name, caption, sender_name, sender_id)
        )
        conn.commit()

def get_all_update_ids():
    with sqlite3.connect("./content.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT update_id FROM polaroids"
        )
        conn.commit()
        return cursor.fetchall()

