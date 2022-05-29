import requests
import json
from uuid import uuid4
from Bot import Bot
import os
from dotenv import load_dotenv


class InstagramBot(Bot):

    def __init__(self, database):
        super().__init__(database)
        self.database = database
        load_dotenv()
        COOKIE_PATH = os.getenv("IG_COOKIE_PATH")
        self.cookies = {}
        with open(COOKIE_PATH, "r") as file:
            raw_json = file.read()
            self.cookies = json.loads(raw_json)

    # overriding abstract method from class Bot
    def fetch_updates(self) -> None:

        raw_response: str = requests.get("https://www.instagram.com/explore/tags/tussimeetsnerd/?__a=1&__d=dis", cookies=self.cookies).text
        json_response: dict = json.loads(raw_response)
        extracted_posts = self.format_response(json_response)

        already_saved_post_ids: set = self.database.get_all_instagram_ids()

        for post in extracted_posts:

            post_id: str = str(post["id"])

            if post_id not in already_saved_post_ids:
                print("Found post which has not been saved yet")
                print(post)
                file_name: str = str(uuid4()) + ".jpg"
                file_path: str = "./static/ig_images/" + file_name
                file_content: bytes = requests.get(post["url"]).content
                final_url: str = "/static/ig_images/" + file_name
                self.save_to_file(file_path=file_path, file_content=file_content)
                self.database.insert_new_instagram(
                    post_id=str(post["id"]),
                    url=str(final_url),
                    caption=str(post["caption"]),
                    username=str(post["username"]),
                    time=int(post["taken_at"])
                )

    def format_response(self, content: dict) -> list:

        posts: list = []

        for post in content["data"]["recent"]["sections"]:
            try:
                medias = post["layout_content"]["medias"]
                for media in medias:
                    try:
                        time = media["media"]["taken_at"]
                        caption = media["media"]["caption"]["text"]
                        post_id = media["media"]["id"]
                        username = media["media"]["user"]["username"]
                        url = media["media"]["image_versions2"]["candidates"][0]["url"]
                        posts.append(
                            {"url": url, "taken_at": time, "caption": caption, "id": post_id, "username": username})
                    except:
                        pass
            except:
                pass

        return posts

    def save_to_file(self, file_path: str, file_content: bytes) -> None:
        try:
            os.mkdir("./static/ig_images")
        except:
            pass

        with open(file_path, "wb") as file:
            file.write(file_content)
            file.close()

    # overriding abstract method from class Bot
    def get_all_items(self) -> list:
        posts = self.database.get_all_instagrams()
        formatted_posts = list(map(lambda post: {
            "id": post[0],
            "url": post[1],
            "caption": post[2],
            "username": post[3],
            "time": post[4]
        }, posts))
        return formatted_posts
