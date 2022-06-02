import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from TelegramBot import TelegramBot
from InstagramBot import InstagramBot
from BotScheduler import BotScheduler
import db

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database = db.OrmAbstraction()
telegram = TelegramBot(database)
instagram = InstagramBot(database)
instagram_scheduler = BotScheduler(instagram, 200.0)
telegram_scheduler = BotScheduler(telegram, 5.0)


@app.get("/telegram_pics")
async def telegram_pics():
    pics = telegram.get_all_items()
    return pics


@app.get("/instagram_pics")
async def instagram_pics():
    pics = instagram.get_all_items()
    return pics


@app.get("/pics")
async def get_all_pics():
    ig_pics = instagram.get_all_items()
    tg_pics = telegram.get_all_items()
    return ig_pics + tg_pics


if __name__ == "__main__":
    instagram_scheduler.start()
    telegram_scheduler.start()

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", debug=False, workers=4)
