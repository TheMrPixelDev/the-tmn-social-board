from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from TelegramBot import TelegramBot
from InstagramBot import InstagramBot
from Database import Database
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

database = Database()
telegram = TelegramBot(database)
instagram = InstagramBot(database)
instagram_scheduler = BotScheduler(instagram, 200)
telegram_scheduler = BotScheduler(telegram, 10)

@app.get("/telegram_pics")
async def telegram_pics():
    #telegram.fetch_updates()
    pics = telegram.get_all_items()
    return pics

@app.get("/instagram_pics")
async def instagram_pics():
    #instagram.fetch_updates()
    pics = instagram.get_all_items()
    return pics