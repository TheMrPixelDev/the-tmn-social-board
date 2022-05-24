from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from Bot import Bot
import DatabaseFunctions

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

bot = Bot()
bot.fetch_updates()

@app.get("/pics")
async def pics():
    bot.fetch_updates()
    pics = bot.get_all_posts()
    return pics