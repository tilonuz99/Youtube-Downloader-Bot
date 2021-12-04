from asyncio import get_event_loop

from pyrogram import Client, idle

from tortoise import Tortoise, run_async
import config

DOWNLOAD_LOCATION = "./downloads"
BOT_TOKEN = config.BOT_TOKEN

APP_ID = config.APP_ID
API_HASH = config.API_HASH


plugins = dict(
    root="plugins",
)

client = Client(
    "tiktok_down",
    bot_token=BOT_TOKEN,
    api_id=APP_ID,
    api_hash=API_HASH,
    plugins=plugins,
    sleep_threshold=180
)


async def main():
    await client.start()
    print("Starting...")
    # await connect_database()
    await idle()


if __name__ == "__main__":
    try:
        run_async(main())
    except KeyboardInterrupt:
        Tortoise.close_connections()