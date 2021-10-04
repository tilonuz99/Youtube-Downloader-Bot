from pyrogram import Client
import config
from utils.database.models import connect_database
DOWNLOAD_LOCATION = "./downloads"
BOT_TOKEN = config.BOT_TOKEN

APP_ID = config.APP_ID
API_HASH = config.API_HASH


plugins = dict(
    root="plugins",
)

Client(
    "YouTubeDlBot",
    bot_token=BOT_TOKEN,
    api_id=APP_ID,
    api_hash=API_HASH,
    plugins=plugins,
    sleep_threshold=180
).run(connect_database())
