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


# extract Youtube info
def extractYt(yturl):
    ydl = youtube_dl.YoutubeDL({'cachedir': False})
    with ydl:
        videoList = {}
        audioList = []

        r = ydl.extract_info(yturl, download=False)
        for format in r['formats'][::-1]:
            if 'audio' in format['format']:
                pass
            if not "dash" in str(format['format']).lower():
                if 'audio' in format['format']:
                    audioList.append({"format": f"{format['abr']}k - {humanbytes(format['filesize'])}", "format_id": format['format_id'],
                                        "yturl": yturl})
                else:
                    videoList[format['format_note']] = {"format": f"{str(format['format']).split('-')[1].strip()} - {humanbytes(format['filesize'])}", "format_id": format['format_id'],
                                "yturl": yturl}

        return r['title'], r['thumbnail'], videoList, audioList

def map_audio_button(item):
    text = item['format']
    return [InlineKeyboardButton(text, callback_data=f"ytdata||audio||{item['format_id']}||{item['yturl']}")]

def create_audio_button(audio_list):
    return map(map_audio_button, audio_list)

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
    
