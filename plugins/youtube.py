from datetime import datetime, timedelta
from pyrogram import Client, Filters, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Message
from bot import user_time
from config import youtube_next_fetch
from helper.ytdlfunc import extractYt, create_audio_button
import wget
import os
from PIL import Image

ytregex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"


@Client.on_message(Filters.regex(ytregex))
async def ytdl(_, message: Message):
    userLastDownloadTime = user_time.get(message.chat.id)
    try:
        if userLastDownloadTime > datetime.now():
            wait_time = round((userLastDownloadTime - datetime.now()).total_seconds())
            await message.reply_text(f"`Wait {wait_time} seconds before next Request`")
            return
    except:
        pass

    user_time[message.chat.id] = datetime.now() + timedelta(seconds=30)
    
    url = message.text.strip()
    await message.reply_chat_action("typing")
    title, thumbnail, videoList, audioList = extractYt(url)
    buttons = InlineKeyboardMarkup(list(create_audio_button(audioList)))
    await message.reply(thumbnail, reply_markup=buttons)
