from os import path, getcwd
from datetime import datetime, timedelta

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import WebpageCurlFailed, MediaEmpty

from PIL import Image
from aiofiles.os import remove

from helper.ytdlfunc import extractYt, video_button
from helper.instafunc import get_media_url, download_media
from helper.ffmfunc import duration

from config import youtube_next_fetch, user_time

from utils.util import humanbytes
from utils.database.models import Youtube_videos, Video_formats, dowmloaded_media

ytregex = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
instaregex = r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:instagram\.com))(\/(?:p|tv|reel)/(?P<id>[^/?#&]+))'

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

    user_time[message.chat.id] = datetime.now() + timedelta(seconds=2)
    analyze = await message.reply("Kuting...")
    url = message.text.strip()
    video = await Youtube_videos.filter(video_url=url).first()

    if video:
        await message.reply("Bazada bor")
        await message.reply_photo(video.thumbnail)
        return
    else:
        try:
            title, thumbnail, videolist = extractYt(url)
        except:
            await analyze.edit_text("Bunday manzil topilmadi!")
            return
    
    

    file_sizes = ""
    for video in videolist.values():
        file_size = video['filesize']
        if file_size > 2147483648:
            file_sizes += f"🛑 {video['format_note']}:  {humanbytes(file_size)}\n"
        else:
            file_sizes += f"✅ {video['format_note']}:  {humanbytes(file_size)}\n"
    keyboard = video_button(videolist)
    buttons = InlineKeyboardMarkup(list(keyboard))
    img = await download_media(thumbnail)
    im = Image.open(img).convert("RGB")
    im.resize((320, 160))
    im.save(img,"jpeg")
    try:
        thumb_id = await message.reply_photo(img, caption=f"📹 {title}\n\n{file_sizes}\n\n❔ Iltimos, fayl turini tanlang: 👇", reply_markup=buttons)
        await Youtube_videos.create(video_url=url, title=title, thumbnail=thumb_id.photo.file_id)

        await analyze.delete()
    except:
        await analyze.edit_text("Yuklab bo'lmadi!")



@Client.on_message(filters.regex(instaregex))
async def insta(_, message: Message):
    userLastDownloadTime = user_time.get(message.chat.id)

    try:
        if userLastDownloadTime > datetime.now():
            wait_time = round((userLastDownloadTime - datetime.now()).total_seconds())
            await message.reply_text(f"`{wait_time} soniyadan so'ng qayta urining!`")
            return
        else:
            user_time[message.chat.id] = datetime.now() + timedelta(seconds=30)

    except:
        pass
    
    try:
        media_url, thumb_url, is_video = await get_media_url(message.text)
    except:
        await message.reply("Bunday manzil topilmadi!")
        return
    if not is_video:
        await message.reply_photo(media_url)
    else:
        img = await download_media(thumb_url)
        im = Image.open(img).convert("RGB")
        im.resize((320, 160))
        im.save(img,"jpeg")
        try:
            await message.reply_video(media_url)
        except WebpageCurlFailed:
            file_name = await download_media(media_url)
            media_duration = await duration(file_name)
            
            await message.reply_video(file_name, duration=int(media_duration), thumb=img)
            try:
                await remove(file_name)
            except:
                pass
            try:
                await remove(img)
            except:
                pass

        except MediaEmpty:
            file_name = await download_media(media_url)
            media_duration = await duration(file_name)
            await message.reply_video(file_name, duration=int(media_duration), thumb=img)
            
            try:
                await remove(file_name)
            except:
                pass
            try:
                await remove(img)
            except:
                pass