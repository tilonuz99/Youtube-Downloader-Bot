from asyncio import get_event_loop
from os import path, makedirs, getcwd, remove
from tempfile import NamedTemporaryFile


from pyrogram import (Client, ContinuePropagation, filters)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaAudio, InputMediaVideo, CallbackQuery

from helper.ffmfunc import duration
from helper.ytdlfunc import downloadvideocli, downloadaudiocli
from PIL.Image import open
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from utils.database.models import Youtube_videos


@Client.on_callback_query()
async def catch_youtube_dldata(c, q: CallbackQuery):
    cb_data = q.data.strip()
    media_type = cb_data.split("||")[1]
    video_id = cb_data.split("||")[-1]
    format_id = cb_data.split("||")[-2]
    
    thumb_image = q.message.photo.file_id
    video = await Youtube_videos.filter(id=int(video_id)).first()

    tf = NamedTemporaryFile(prefix="media_", suffix=".%(ext)s")
    filepath = tf.name.replace('/tmp/', '')

    yturl = video.video_url

    audio_command = [
        "youtube-dl",
        "-c",
        "--prefer-ffmpeg",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "bestaudio",
        "-o", filepath,
        yturl,

    ]

    video_command = [
        "youtube-dl",
        '-c',
        '-k',
        "-f", f"{format_id}",
        "--hls-prefer-ffmpeg", yturl,
        "-o", filepath
        ]

    video_command.append("--no-warnings")
    video_command.append("--restrict-filenames")

    

    med = None
    if media_type == "audio":
        filename = await downloadaudiocli(audio_command)
        med = InputMediaAudio(
            media=filename,
            thumb=thumb_image,
            caption=path.basename(filename),
            title=path.basename(filename)
        )

    if media_type == "video":
        filename = await downloadvideocli(video_command, filepath)
        # dur = round((await duration(filename)))
        if filename:
            print(filename)
            med = InputMediaVideo(
                media=filename,
                # duration=dur,
                thumb=thumb_image,
                caption=path.basename(filename),
                supports_streaming=True
            )

    if med:
        await send_file(c, q, med, filename)
    else:
        print("med not found")


async def send_file(c, q, med, filename):
    try:
        await q.edit_message_reply_markup(
            InlineKeyboardMarkup([[InlineKeyboardButton("Uploading...", callback_data="down")]]))
        await c.send_chat_action(chat_id=q.message.chat.id, action="upload_video")
        await q.edit_message_media(media=med)
    except Exception as e:
        print(e)
        await q.edit_message_text(e)
    finally:
        try:
            remove(filename)
        except:
            pass
