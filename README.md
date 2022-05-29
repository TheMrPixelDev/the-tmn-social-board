# TMN SOCIAL BOARD

This is an application which displays pictures sent to a Telegram-Bot.
It's used at the TMN-Party of the Fachschaft Philo and FSinfo at the University of Passau.

### Features
+ send pictures to Telegram-Bot
+ provides a centralzied Rest-API
+ scrape instagram hashtags

### Installation
1. Clone this repository
```bash
git clone https://github.com/TheMrPixelDev/the-tmn-social-board.git
```

2. Create a .env file in the root directory and open it
```bash
touch .env
nano .env
```

3. Add your telegram bot token and a path to the json file containing your instagram cookies.
```
TG_TOKEN=your_telegram_bot_token
IG_COOKIE_PATH=/path/to/your/json/file
```

