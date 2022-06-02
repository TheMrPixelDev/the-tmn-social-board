import time
from Bot import Bot
import threading


# *
# This was the easiest implementation to solve this problem I could think of.
# If you know a better was to solve this for example using an event loop,
# feel free to make a pull request.
# Some inspiration: https://github.com/encode/uvicorn/issues/706
# *#


class BotScheduler(threading.Thread):

    def __init__(self, bot: Bot, delay: float):
        if not isinstance(bot, Bot):
            raise Exception(f"{bot} does not implement Bot.")
        else:
            self.bot = bot
            self.delay: float = delay
        super().__init__(target=self._execute, args=(bot, delay))

    @staticmethod
    def _execute(bot: Bot, delay: float):
        print(f"Starting thread to executed function {bot.fetch_updates} every {delay}s.")
        while True:
            bot.fetch_updates()
            time.sleep(delay)
