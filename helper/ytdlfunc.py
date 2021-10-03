from __future__ import unicode_literals
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from youtube_dl import YoutubeDL

from utils.util import humanbytes
from asyncio import create_subprocess_exec, subprocess
from json import dumps


# extract Youtube info
def extractYt(yturl):
    ydl = YoutubeDL({'cachedir': False})
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
    process = await create_subprocess_exec(
        *command_to_exec,

        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, )

async def downloadaudiocli(command_to_exec):
    process = await create_subprocess_exec(
        *command_to_exec,

        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, )
    
