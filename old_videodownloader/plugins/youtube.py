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
from utils.database.models import Youtube_videos, Video_formats, Dowmloaded_media

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
    url = message.text.strip()
    video = await Youtube_videos.filter(video_url=url).first()

    if video:
        video_formats = await Video_formats.filter(video_id=video.id).all()
        file_sizes = ""
        videoList = {}
        for videos in video_formats:
            is_downloaded = await Dowmloaded_media.filter(video_format_id=videos.id).first()
            file_size = videos.file_size
            if file_size > 2147483648:
                file_sizes += f"🛑 {videos.format_type}:  {humanbytes(file_size)}\n"
            elif is_downloaded:
                file_sizes += f"🚀 {videos.format_type}:  {humanbytes(file_size)}\n"
            else:
                file_sizes += f"✅ {videos.format_type}:  {humanbytes(file_size)}\n"

            videoList[videos.format_type] = {"format": f"📹 {videos.format_type}", 'format_note': videos.format_type, 'filesize': videos.file_size, "format_id": videos.format_id}
        
        keyboard = video_button(videoList, video.id)
        buttons = InlineKeyboardMarkup(list(keyboard))

        await message.reply_photo(video.thumbnail, caption=f"📹 {video.title}\n\n{file_sizes}\n\n❔ Iltimos, fayl turini tanlang: 👇", reply_markup=buttons)
        return
    else:
        analyze = await message.reply("Kuting...")

        # try:
        title, thumbnail, videolist = extractYt(url)
        added_video = await Youtube_videos.create(video_url=url, title=title)

        file_sizes = ""
        for video in videolist.values():
            file_size = video['filesize']

            await Video_formats.create(format_type=video['format_note'], format_id=int(video['format_id']), file_size=int(file_size), video_id=added_video.id)

            if file_size > 2147483648:
                file_sizes += f"🛑 {video['format_note']}:  {humanbytes(file_size)}\n"
            else:
                file_sizes += f"✅ {video['format_note']}:  {humanbytes(file_size)}\n"

        keyboard = video_button(videolist, added_video.id)
        buttons = InlineKeyboardMarkup(list(keyboard))
        img = await download_media(thumbnail)
        im = Image.open(img).convert("RGB")
        im.resize((320, 160))
        im.save(img,"jpeg")
        try:
            thumb_id = await message.reply_photo(img, caption=f"📹 {title}\n\n{file_sizes}\n\n❔ Iltimos, fayl turini tanlang: 👇", reply_markup=buttons)
            await analyze.delete()
            await Youtube_videos.filter(id=added_video.id).update(thumbnail=thumb_id.photo.file_id)
        except Exception as e:
            print(e)
            await analyze.edit_text("Yuklab bo'lmadi!")
        # except Exception as e:
        #     await analyze.edit_text("Bunday manzil topilmadi!:")
        #     print(e)
        #     return

    



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