import requests
import json
import uuid
import os
from dotenv import load_dotenv
from Bot import Bot
from db import Post


class TelegramBot(Bot):

    def __init__(self, database):
        super().__init__(database)
        load_dotenv()
        self.TOKEN = os.getenv("TG_TOKEN")

    def fetch_updates(self):
        raw_updates: str = requests.get(f"https://api.telegram.org/bot{self.TOKEN}/getUpdates").text
        updates = json.loads(raw_updates)["result"]

        saved_messages_ids: set = set(map(lambda d: d[0], self.database.get_ids_by_platform("telegram")))
        tg_posts: [Post] = []

        for update in updates:
            update_id = update["update_id"]
            msg_id = update["message"]["message_id"]
            post_id = str(update_id) + str(msg_id)
            msg_date = update["message"]["date"]
            sender_name = ""
            try:
                sender_name = update["message"]["from"]["username"]
            except:
                print("Remember to set a username on Telegram.")

            file_name = ""
            caption = ""

            # Checks wheter id of message is already in the database
            if post_id not in saved_messages_ids:
                try:
                    file_id = update["message"]["photo"][-1]["file_id"]
                    file_name = self._get_photo(file_id)
                    caption = update["message"]["caption"]
                except:
                    pass

                if file_name != "":
                    tg_posts.append(
                        Post(
                            post_id=post_id,
                            datetime=msg_date,
                            username=sender_name,
                            caption=caption,
                            file="/static/tg_images/" + file_name,
                            platform="telegram"
                        )
                    )

        self.database.save_posts(tg_posts)

    # Overriding function from abstract class
    def get_all_items(self) -> list:
        posts = self.database.get_all_posts(Post.platform == "telegram")
        posts = list(map(lambda post: dict(post), posts))
        return posts

    def _get_photo(self, file_id):
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
