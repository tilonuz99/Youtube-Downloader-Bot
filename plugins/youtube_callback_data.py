import asyncio
import os

from pyrogram import (Client, ContinuePropagation, filters)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaAudio, InputMediaVideo

from helper.ffmfunc import duration
from helper.ytdlfunc import downloadvideocli, downloadaudiocli
from PIL.Image import open
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


@Client.on_callback_query()
async def catch_youtube_dldata(c, q):
    cb_data = q.data.strip()

    yturl = cb_data.split("||")[-1]
    format_id = cb_data.split("||")[-2]
    thumb_image_path = "downloads" + \
        "/" + str(q.message.chat.id) + ".jpg"
    print(thumb_image_path)
    width = 360
    height = 340

    if os.path.exists(thumb_image_path):
        metadata = extractMetadata(createParser(thumb_image_path))

        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
        img = open(thumb_image_path)
        if cb_data.startswith("audio"):
            img.resize((320, height))
        else:
            img.resize((90, height))
        img.save(thumb_image_path, "JPEG")

    if not cb_data.startswith(("video", "audio")):
        print("no data found")
        raise ContinuePropagation

    filext = "%(title)s.%(ext)s"
    userdir = os.path.join(os.getcwd(), "downloads", str(q.message.chat.id))

    if not os.path.isdir(userdir):
        os.makedirs(userdir)
    await q.edit_message_reply_markup(
        InlineKeyboardMarkup([[InlineKeyboardButton("Downloading...", callback_data="down")]]))
    filepath = os.path.join(userdir, filext)
    # await q.edit_message_reply_markup([[InlineKeyboardButton("Processing..")]])

    audio_command = [
        "youtube-dl",
        "-c",
        "--prefer-ffmpeg",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", format_id,
        "-o", filepath,
        yturl,

    ]

    video_command = [
        "youtube-dl",
        "-c",
        "--embed-subs",
        "-f", f"{format_id}+bestaudio",
        "-o", filepath,
        "--hls-prefer-ffmpeg", yturl]

    loop = asyncio.get_event_loop()

    med = None
    if cb_data.startswith("audio"):
        filename = await downloadaudiocli(audio_command)
        med = InputMediaAudio(
            media=filename,
            thumb=thumb_image_path,
            caption=os.path.basename(filename),
            title=os.path.basename(filename)
        )

    if cb_data.startswith("video"):
        filename = await downloadvideocli(video_command)
        dur = round(duration(filename))
        med = InputMediaVideo(
            media=filename,
            duration=dur,
            width=width,
            height=height,
            thumb=thumb_image_path,
            caption=os.path.basename(filename),
            supports_streaming=True
        )

    if med:
        loop.create_task(send_file(c, q, med, filename))
    else:
        print("med not found")


async def send_file(c, q, med, filename):
    print(med)
    try:
        await q.edit_message_reply_markup(
            InlineKeyboardMarkup([[InlineKeyboardButton("Uploading...", callback_data="down")]]))
        await c.send_chat_action(chat_id=q.message.chat.id, action="upload_video")
        # this one is not working
        await q.edit_message_media(media=med)
    except Exception as e:
        print(e)
        await q.edit_message_text(e)
    finally:
        try:
            os.remove(filename)
        except:
            pass
