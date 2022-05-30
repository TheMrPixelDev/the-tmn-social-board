from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from TelegramBot import TelegramBot
from InstagramBot import InstagramBot
import db
from BotScheduler import BotScheduler

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
instagram_scheduler = BotScheduler(instagram, 200)
telegram_scheduler = BotScheduler(telegram, 10)


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
