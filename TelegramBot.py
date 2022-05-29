import requests
import json
import uuid
import os
from dotenv import load_dotenv
from Bot import Bot


class TelegramBot(Bot):

    def __init__(self, database):
        super().__init__(database)
        load_dotenv()
        self.TOKEN = os.getenv("TG_TOKEN")

    def fetch_updates(self):
        raw_updates: str = requests.get(f"https://api.telegram.org/bot{self.TOKEN}/getUpdates").text
        updates = json.loads(raw_updates)["result"]

        saved_messages: set = self.database.get_all_telegram_ids()

        for update in updates:
            update_id = update["update_id"]
            msg_id = update["message"]["message_id"]
            sender_id = update["message"]["from"]["id"]
            sender_name = ""
            try:
                sender_name = update["message"]["from"]["username"]
            except:
                print("Remember to set a username on Telegram.")

            file_name = ""
            caption = ""

            # Checks wheter id of message is already in the database
            if update_id not in saved_messages:

                try:
                    file_id = update["message"]["photo"][-1]["file_id"]
                    file_name = self.get_photo(file_id)
                    caption = update["message"]["caption"]
                except:
                    pass

                if file_name != "":
                    self.database.insert_new_telegram(update_id, msg_id, file_name, caption, sender_name, sender_id)

    # Overriding function from abstract class
    def get_all_items(self) -> list:
        posts = self.database.get_all_telegrams()
        formatted_posts: list = list(map(lambda post: {
            "url": "/static/images/" + post[0],
            "caption": post[1],
            "username": post[2]
        }, posts))

        return formatted_posts

    def get_photo(self, file_id):
        file_path = \
        json.loads(requests.get(f"https://api.telegram.org/bot{self.TOKEN}/getFile?file_id={file_id}").text)["result"][
            "file_path"]
        file = requests.get(f"https://api.telegram.org/file/bot{self.TOKEN}/{file_path}").content
        file_type = file_path.split(".")[-1]
        print("Saving new file: " + str(uuid.uuid4()) + "." + file_type)
        file_name = str(uuid.uuid4()) + "." + file_type

        try:
            os.mkdir("./static/tg_images")
        except:
            pass

        with open(f"./static/tg_images/{file_name}", "wb") as img:
            img.write(file)
            img.close()
        return file_name
