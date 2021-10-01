from datetime import datetime, timedelta
from pyrogram import Client, Filters, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Message
from bot import user_time
from config import youtube_next_fetch
from helper.ytdlfunc import extractYt, create_audio_button, create_video_button, video_audio_button
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
    keyboard, thumbnail, title = video_audio_button(url)
    # buttons = InlineKeyboardMarkup(list(create_audio_button(audioList)))
    buttons = InlineKeyboardMarkup(list(keyboard))

    img = wget.download(thumbnail)
    im = Image.open(img).convert("RGB")
    output_directory = os.path.join(os.getcwd(), "downloads", str(message.chat.id))
    print(output_directory)
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)
    thumb_image_path = f"{output_directory}.jpg"
    im.save(thumb_image_path,"jpeg")
    await message.reply_photo(thumb_image_path, caption=title, reply_markup=buttons)

























# buttons = InlineKeyboardMarkup(list(create_audio_button(audioList)))
    # buttons = InlineKeyboardMarkup(list(create_video_button(videoList)))

    # img = wget.download(thumbnail)
    # im = Image.open(img).convert("RGB")
    # output_directory = os.path.join(os.getcwd(), "downloads", str(message.chat.id))
    # print(output_directory)
    # if not os.path.isdir(output_directory):
    #     os.makedirs(output_directory)
    # thumb_image_path = f"{output_directory}.jpg"
    # im.save(thumb_image_path,"jpeg")
    # await message.reply_photo(thumb_image_path, caption=title, reply_markup=buttons)
