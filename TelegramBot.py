import random

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
            message: dict = update.get("message")

            # Checks the update even contains a message
            if message is not None:

                update_id = update.get("update_id")
                msg_id = message.get("message_id")
                post_id = str(update_id) + str(msg_id)

                # Check if update is already in database
                if post_id not in saved_messages_ids:
                    msg_type = update.get("message").get("chat").get("type")
                    # Check if message is in group chat or not
                    if msg_type == "group":
                        parsed_post = self._parse_group_chat_update(update)
                        if parsed_post is not None:
                            tg_posts.append(parsed_post)
                    elif msg_type == "private":
                        parsed_post = self._parse_private_chat_update(update)
                        if parsed_post is not None:
                            tg_posts.append(parsed_post)

        self.database.save_posts(tg_posts)

    def _parse_group_chat_update(self, update: dict) -> Post or None:
        photo = update.get("message").get("photo")
        caption: str = update.get("message").get("caption")
        update_id: int = update.get("update_id")
        msg_id: int = update.get("message").get("message_id")
        post_id = str(update_id) + str(msg_id)
        msg_date: int = update.get("message").get("date")
        username: str = update.get("message").get("from").get("username")
        group_chat_id: int = update.get("message").get("chat").get("id")

        # Check if the bot is mentioned and photo has been sent
        if photo is not None and caption is not None and "@tmn_social_bot" in caption:
            photo_id = photo[-1].get("file_id")
            file_name = self._get_photo(photo_id)
            clean_caption = caption.replace("@tmn_social_bot", "")
            res_msg = self._get_random_msg()
            self._send_message(chat_id=group_chat_id, text=res_msg)
            return Post(
                post_id=post_id,
                datetime=str(msg_date),
                username=username,
                file=file_name,
                caption=clean_caption,
                platform="telegram"
            )
        else:
            return None

    def _parse_private_chat_update(self, update: dict) -> Post or None:
        photo: dict = update.get("message").get("photo")
        caption: str = update.get("message").get("caption")
        update_id: int = update.get("update_id")
        msg_id: int = update.get("message").get("message_id")
        post_id = str(update_id) + str(msg_id)
        username: str = update.get("message").get("from").get("username")
        datetime = update.get("message").get("date")

        if photo is not None:
            file_id: str = photo[-1].get("file_id")
            file_name: str = self._get_photo(file_id)
            return Post(
                username=username,
                file=file_name,
                datetime=str(datetime),
                caption=caption,
                post_id=post_id,
                platform="telegram"
            )
        else:
            return None

    @staticmethod
    def _log(message) -> None:
        print(f"[TG-Bot] {message}")

    def _send_message(self, text: str, chat_id: int):
        req_rul = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
        try:
            requests.get(req_rul)
        except Exception as e:
            print(e)
            self._log("Was not able to send group response.")


    # Overriding function from abstract class
    def get_all_items(self) -> list:
        posts = self.database.get_all_posts(Post.platform == "telegram")
        posts = list(map(lambda post: dict(post), posts))
        return posts

    def _get_photo(self, file_id):
        file_path = json.loads(
            requests.get(f"https://api.telegram.org/bot{self.TOKEN}/getFile?file_id={file_id}").text).get("result").get(
            "file_path")
        req_url = f"https://api.telegram.org/file/bot{self.TOKEN}/{file_path}"
        file = requests.get(req_url).content
        # file_type = file_path.split(".")[-1]
        file_type = "jpg"
        self._log("Saving new file: " + str(uuid.uuid4()) + "." + file_type)
        file_name = str(uuid.uuid4()) + "." + file_type

        try:
            os.mkdir("./static/tg_images")
        except FileExistsError:
            self._log("Telegram photos folder already exists.")

        with open(f"./static/tg_images/{file_name}", "wb") as img:
            img.write(file)
            img.close()
        return "/static/tg_images/" + file_name

    def _get_random_msg(self) -> str:
        messages = [
            "Jo diggi, habs gespeichert!",
            "Seh ich aus, wie ein CPU-Knecht? Hhhh is drin...",
            "Hab 's mir gerade gesnacked!",
            "Nices Bild! Habs gleich in die Sammlung aufgenommen.",
            "Nicht ganz mein Ding, aber is halt mein Job das zu speichern.",
            "Mei is des n hübsches Foto.",
            "Let's get sis party started!!! Got it!",
            "HAaaabssd.. Higgs... gspeicheRttT Higgs... 🍺😜",
            "Awesome! Is drin!",
            "Gib mir meeeeeeehr!",
            "Hoth. Das Bild wurde in den Jeditempel aufgenommen.",
            "Ey ihr seid ja on fire! Gesaved! Gebt mir mehr!"
        ]
        rnd = random.Random()
        index = rnd.randint(0, len(messages) - 1)
        return messages[index]
