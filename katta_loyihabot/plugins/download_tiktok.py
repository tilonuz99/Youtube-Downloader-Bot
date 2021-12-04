from asyncio import get_event_loop
from os import path

from pyrogram import Client

from pyrogram.types import Message
from yt_dlp import YoutubeDL
from json import dumps

from app import client

@Client.on_message()
async def get_video_url(client: Client, message: Message):
    need_wait = await message.reply("Kuting...")
    options_down = {
        "format": format_selector,
        "overwrites": True,
        "noprogress": True,
        "quiet": True,
        "logger": None,
        'no_warnings': True,
        'outtmpl': '%(id)s.%(ext)s',
    }
    with YoutubeDL(options_down) as ydl:
        video_path = ydl.extract_info(message.text)
        await message.reply_video(f"{video_path.get('id')}.mp4")



def format_selector(ctx):
    """ Select the best video and the best audio that won't result in an mkv.
    This is just an example and does not handle all cases """

    # formats are already sorted worst to best
    formats = ctx.get('formats')[::-1]

    # acodec='none' means there is no audio
    best_video = next(f for f in formats
                      if f['vcodec'] != 'none' and f['acodec'] == 'none')

    # find compatible audio extension
    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    # vcodec='none' means there is no video
    best_audio = next(f for f in formats if (
        f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

    yield {
        # These are the minimum required fields for a merged format
        'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        # Must be + seperated list of protocols
        'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
    }