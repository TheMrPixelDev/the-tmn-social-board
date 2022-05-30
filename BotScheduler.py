from Bot import Bot
import asyncio
import datetime

class BotScheduler:
    def __init__(self, bot: Bot, delay: float):
        if not isinstance(bot, Bot):
            raise Exception(f"{bot} does not implement Bot.")
        else:
            self.bot = bot
            self.loop = asyncio.get_event_loop()
            self.delay: float = delay
            self._running = asyncio.Lock()

    def set_delay(self, delay: float) -> None:
        self.delay: float = delay

    def start(self) -> None:
        self.loop.call_later(delay=self.delay, callback=self._execute)

    def _execute(self):
        self.bot.fetch_updates()
        print(f"Executed function {self.bot.fetch_updates} at {datetime.datetime.now()} (delay: {self.delay}s).")
        self.start()