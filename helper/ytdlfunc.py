from __future__ import unicode_literals
from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup
import youtube_dl
from utils.util import humanbytes
import asyncio
from json import dumps

def buttonmap(item):
    quality = item['format']
    if "audio" in quality:
        return [InlineKeyboardButton(f"{quality} 🎵 {humanbytes(item['filesize'])}",
                                     callback_data=f"ytdata||audio||{item['format_id']}||{item['yturl']}")]
    else:
        return [InlineKeyboardButton(f"{quality} 📹 {humanbytes(item['filesize'])}",
                                     callback_data=f"ytdata||video||{item['format_id']}||{item['yturl']}")]

# Return a array of Buttons
def create_buttons(quailitylist):
    return map(buttonmap, quailitylist)

def video_audio_button(url):
    ydl = youtube_dl.YoutubeDL({'cachedir': False})
    with ydl:
        r = ydl.extract_info(url, download=False)
        thumb_url = r['thumbnail']
        title = r['title']

    return [
        [InlineKeyboardButton(f"📹 Video", callback_data=f"select||video||{url}")],
        [InlineKeyboardButton(f"🎵 Audio", callback_data=f"select||audio||{url}")]
        ], thumb_url, title,

# extract Youtube info
def extractYt(yturl):
    ydl = youtube_dl.YoutubeDL({'cachedir': False})
    with ydl:
        videoList = {}
        audioList = []

        r = ydl.extract_info(yturl, download=False)
        for format in r['formats']:
            if format['filesize'] is not None:
                if not "dash" in str(format['format']).lower() and not "p60" in str(format['format']).lower() and not "p30" in str(format['format']).lower():
                    if 'audio' in format['format']:
                        audioList.append({"format": f"{format['abr']}k - {humanbytes(format['filesize'])}", "format_id": format['format_id'],
                                            "yturl": yturl})
                    else:
                        videoList[format['format_note']] = {"format": f"📹 {format['format_note']}", 'format_note': format['format_note'], "filesize": format['filesize'],"format_id": format['format_id'],
                                    "yturl": yturl}

        return r['title'], r['thumbnail'], videoList, audioList


def video_button(videos_list):
    keyboards = []
    for item in videos_list.values():
        keyboards.append(InlineKeyboardButton(item, callback_data=f"ytdata||video||{item['format_id']}||{item['yturl']}"))
    keyboards = [keyboards[i:i + 3] for i in range(0, len(keyboards), 3)]
    keyboards = keyboards + [InlineKeyboardButton("🔉 MP3", callback_data=f"ytdata||audio||{item['format_id']}||{item['yturl']}")]

    return keyboards

async def downloadvideocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,

        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE, )

async def downloadaudiocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,

        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE, )
    
