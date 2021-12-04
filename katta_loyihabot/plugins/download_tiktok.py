from asyncio import gather
from os import path, remove

from pyrogram import Client

from pyrogram.types import Message
from yt_dlp import YoutubeDL

from utils.database.models import TikTok_videos
from tortoise.expressions import Q

options_down = {
        "noprogress": True,
        "quiet": True,
        "logger": None,
        'no_warnings': True
    }

@Client.on_message()
async def send_video(client: Client, message: Message):
    need_wait = await message.reply("Kuting...")

    task1 = gather(get_video_url(message, need_wait))

async def get_video_url(message, need_wait):
    video = await TikTok_videos.filter(Q(video_url=url)).first()
    if video:
        print("Bazada bor")

    with YoutubeDL(options_down) as ydl:
        video_info = ydl.extract_info(message.text, False)
        video_formats = video_info.get("formats")
        for formate in video_formats:
            if formate.get("format_note") in ["Direct video (API)", "Direct video"]:
                try:
                    await need_wait.delete()
                    file = await message.reply_video(formate.get('url'))
                    await TikTok_videos.create(video_url=message.text, video_id=video_info.get("id"), file_id=file.video.file_id)
                    break
                except:
                    await need_wait.edit_text("Videoni yuklab olib bo'lmadi!")