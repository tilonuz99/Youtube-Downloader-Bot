from datetime import datetime, timedelta

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot import user_time
from config import youtube_next_fetch
from helper.ytdlfunc import extractYt, map_video_button
import wget
import os
from PIL import Image
from utils.util import humanbytes

ytregex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"


@Client.on_message(filters.regex(ytregex))
async def ytdl(_, message: Message):
    userLastDownloadTime = user_time.get(message.chat.id)
    try:
        if userLastDownloadTime > datetime.now():
            wait_time = round((userLastDownloadTime - datetime.now()).total_seconds())
            await message.reply_text(f"`{wait_time} soniyadan so'ng qayta urining!`")
            return
    except:
        pass

    user_time[message.chat.id] = datetime.now() + timedelta(seconds=30)
    
    url = message.text.strip()
    title, thumbnail, videolist = extractYt(url)
    file_sizes = ""
    for video in videolist.values():
        file_size = video['filesize']
        if file_size > 2147483648:
            file_sizes += f"🛑 {video['format_note']}:  {humanbytes(file_size)}\n"
        else:
            file_sizes += f"✅ {video['format_note']}:  {humanbytes(file_size)}\n"
    keyboard = map_video_button(videolist)
    buttons = InlineKeyboardMarkup(list(keyboard))
    
    img = wget.download(thumbnail, out=False)
    im = Image.open(img).convert("RGB")
    output_directory = os.path.join(os.getcwd(), "downloads", str(message.chat.id))
    thumb_image_path = f"{output_directory}.jpg"
    im.save(thumb_image_path,"jpeg")
    await message.reply_photo(thumb_image_path, caption=f"📹 {title}\n\n{file_sizes}\n\n❔ Iltimos, fayl turini tanlang: 👇", reply_markup=buttons)





@Client.on_message()
async def _get_insta(c, message: Message):
    await message.reply