import requests
import DatabaseFunctions
import json
import uuid
import os
import threading
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TG_TOKEN")

class Bot:

    def __init__(self):
        DatabaseFunctions.try_to_create_database()

    async def fetch_updates(self):
        print("FETCHING UPDATES NOW")
        text = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates").text
        saved_messages = set(map((lambda a: a[0]), DatabaseFunctions.get_all_update_ids()))
        result = json.loads(text)["result"]

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
                file_name = self.get_photo(file_id)
                caption = update["message"]["caption"]
            except:
                pass

            if file_name != "":
                DatabaseFunctions.insert_new_post(update_id, msg_id, file_name, caption, sender_name, sender_id)


    def get_all_posts(self):
        data = []
        for row in DatabaseFunctions.get_all_posts():
            data.append({
                "url": "/static/images/" + row[0],
                "subtitle": row[1],
                "sender": row[2]
            })
        return data

    def get_photo(self, file_id):
        file_path = json.loads(requests.get(f"https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}").text)["result"]["file_path"]
        file = requests.get(f"https://api.telegram.org/file/bot{TOKEN}/{file_path}").content
        file_type = file_path.split(".")[-1]
        print("Saving new file: " + str(uuid.uuid4()) + "." + file_type)
        file_name = str(uuid.uuid4()) + "." + file_type
        try:
            os.mkdir("./static/images")
        except:
            pass
        with open(f"./static/images/{file_name}", "wb") as img:
            img.write(file)
            img.close()
        return file_name