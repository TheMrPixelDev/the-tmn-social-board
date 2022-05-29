import sqlite3


class Database:

    def __init__(self):
        self.try_to_create_database()

    def try_to_create_database(self):
        with sqlite3.connect("./content.db") as conn:
            cursor = conn.cursor()
            # try to create the telegrams table
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS telegrams (update_id INTEGER PRIMARY KEY, msg_id INTEGER, file_name TEXT, '
                'message TEXT, sender_name TEXT, sender_id INTEGER)')
            # try to create the instagrams table
            cursor.execute(
                'CREATE TABLE IF NOT EXISTS instagrams (post_id TEXT PRIMARY KEY, url TEXT, caption TEXT, username TEXT, time INTEGER)')
            conn.commit()

    def get_all_telegrams(self):
        with sqlite3.connect("./content.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT file_name, message, sender_name FROM telegrams'
            )
            conn.commit()
            return cursor.fetchall()

    def get_all_instagrams(self):
        with sqlite3.connect("./content.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM instagrams'
            )
            conn.commit()
            return cursor.fetchall()

    def insert_new_telegram(self, update_id, msg_id, file_name, caption, sender_name, sender_id):
        with sqlite3.connect("./content.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO telegrams VALUES (?, ?, ?, ?, ?, ?)',
                (update_id, msg_id, file_name, caption, sender_name, sender_id)
            )
            conn.commit()

    def insert_new_instagram(self, post_id: int, url: str, caption: str, username: str, time: int):
        with sqlite3.connect("./content.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO instagrams VALUES (?, ?, ?, ?, ?)',
                (post_id, url, caption, username, time)
            )
            conn.commit()

    def get_all_telegram_ids(self):
        with sqlite3.connect("./content.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT update_id FROM telegrams"
            )
            conn.commit()
            ids = cursor.fetchall()
            return set(map(lambda a: a[0], ids))

    def get_all_instagram_ids(self) -> set:
        with sqlite3.connect("./content.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT post_id FROM instagrams"
            )
            conn.commit()
            ids = cursor.fetchall()
            return set(map(lambda a: a[0], ids))
