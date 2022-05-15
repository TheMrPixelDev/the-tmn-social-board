import requests
import json
import sqlite3
import uuid
import threading

#GET TOKEN FROM ENVIRONMENT
TOKEN = ""

class Bot:

    def __init__(self):
        con = sqlite3.connect("./content.db")
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS polaroids (update_id INTEGER PRIMARY KEY, msg_id INTEGER, file_name TEXT, "
            "message TEXT, sender_name TEXT, sender_id INTEGER)")
        con.commit()
        con.close()

    def insertData(self, query, data):
        conn = sqlite3.connect("./content.db")
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        conn.close()

    def selectData(self, query):
        conn = sqlite3.connect("./content.db")
        curser = conn.cursor()
        data = list(curser.execute(query))
        conn.commit()
        conn.close()
        return data
        
    def getUpdates(self):
        text = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").text
        saved_messages = set(map((lambda a: a[0]), self.selectData("SELECT update_id FROM polaroids")))

        result = json.loads(text)["result"]
        print(result)
        for update in result:
            update_id = update["update_id"]
            msg_id = update["message"]["message_id"]
            sender_id = update["message"]["from"]["id"]
            sender_name = ""
            try:
                sender_name = update["message"]["from"]["username"]
            except:
                pass
            file_name = ""
            caption = ""

            if update_id in saved_messages:
                continue

            try:
                file_id = update["message"]["photo"][-1]["file_id"]
                file_name = self.getPhoto(file_id)
                caption = update["message"]["caption"]
            except:
                pass

            if file_name != "":
                data = (update_id, msg_id, file_name, caption, sender_name, sender_id)
                print(data)
                self.insertData("INSERT INTO polaroids VALUES (?, ?, ?, ?, ?, ?)", data=data)

        #threading.Timer(5, self.getUpdates).start()

    def getPhoto(self, file_id):
        file_path = json.loads(requests.get(f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}").text)["result"]["file_path"]
        file = requests.get(f"https://api.telegram.org/file/bot{TOKEN}/{file_path}").content
        file_name = str(uuid.uuid4()) + ".jpg"
        with open(f"./static/images/{file_name}", "wb") as img:
            img.write(file)
            img.close()
        return file_name