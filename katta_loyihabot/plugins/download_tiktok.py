from asyncio import gather
from os import path, remove
from re import findall

from pyrogram import Client

from pyrogram.types import Message
from yt_dlp import YoutubeDL

from utils.database.models import TikTok_videos
from tortoise.query_utils import Q

options_down = {
        "noprogress": True,
        "quiet": True,
        "logger": None,
        'no_warnings': True
    }

@Client.on_message()
async def send_video(client: Client, message: Message):

    task1 = gather(get_video_url(message))

async def get_video_url(message):
    url = message.text

    if url.startswith("https://vm.tiktok.com"):
        post_id = url.replace("https://vm.tiktok.com/", '')
        post_id = post_id.replace('/', '')
    elif url.startswith("https://m.tiktok.com/v/"):
        find = findall("((?:https?:\/\/(?:www|m|vm)\.))?((?:tiktok\.com))(?:/v/([a-zA-Z0-9]+)|(?P<id>[a-zA-Z0-9])+)",
                    url)
        post_id = find[0][2]
    elif "@" in url and "/video/" in url:
        post_id = url.split("/video/")[1].split("?")[0]
    else:
        await message.reply("Video topilmadi!")
        return
    video = await TikTok_videos.filter(Q(video_url=url) | Q(video_id=post_id)).first()
    if video:
        await message.reply_video(video.file_id)
        return
    else:
        need_wait = await message.reply("Kuting...")
    with YoutubeDL(options_down) as ydl:
        video_info = ydl.extract_info(message.text, False)
        video_formats = video_info.get("formats")
        for formate in video_formats:
            if formate.get("format_note") in ["Direct video (API)", "Direct video"]:
                try:
                    await need_wait.delete()
                    file = await message.reply_video(formate.get('url'))
                    await TikTok_videos.create(video_url=url, video_id=post_id, file_id=file.video.file_id)
                    break
                except Exception as e:
                    try:
                        await need_wait.edit_text("Videoni yuklab olib bo'lmadi!")
                    except:
                        await message.reply("Videoni yuklab olib bo'lmadi!")
                    return