from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bot import Bot

app = FastAPI()
bot = Bot()

templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

@app.get("/pics")
async def pics():
    bot.getUpdates()
    data = []
    for row in bot.selectData(f"SELECT file_name, message, sender_name FROM polaroids"):
        data.append({
            "url": "/static/images/" + row[0],
            "subtitle": row[1],
            "sender": row[2]
        })
    return data