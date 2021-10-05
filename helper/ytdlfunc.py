from __future__ import unicode_literals
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from youtube_dl import YoutubeDL

from utils.util import humanbytes
from asyncio import create_subprocess_exec, subprocess
from json import dumps


# extract Youtube info
def extractYt(yturl):
    ydl = YoutubeDL({'cachedir': False, 'quiet': True})
    with ydl:
        videoList = {}

        try:
            r = ydl.extract_info(yturl, download=False)
        except:
            return None
        for format in r['formats']:
            if format['filesize'] is not None:
                if not "dash" in str(format['format']).lower() and not "p60" in str(format['format']).lower() and not "p30" in str(format['format']).lower():
                    if 'audio' not in format['format']:
                        videoList[format['format_note']] = {"format": f"📹 {format['format_note']}", 'format_note': format['format_note'], 'filesize': format['filesize'],"format_id": format['format_id']}

        return r['title'], r['thumbnail'], videoList


def video_button(videos_list, video_id):
    keyboards = [] 
    for item in videos_list.values():
        file_size = item['filesize']
        if file_size > 2147483648:
            keyboards.append(InlineKeyboardButton(text=item['format'], callback_data=f"not_down"))
        else:
            keyboards.append(InlineKeyboardButton(text=item['format'], callback_data=f"y||video||{item['format_id']}||{video_id}"))
    keyboards = [keyboards[i:i + 3] for i in range(0, len(keyboards), 3)]
    keyboards.append([InlineKeyboardButton(text="🔊 MP3", callback_data=f"y||audio||{video_id}")])

    return keyboards

async def downloadvideocli(command_to_exec, filepath):
    print(*command_to_exec)
    process = await create_subprocess_exec(
        *command_to_exec,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, )
    stdout, stderr = await process.communicate()

    e_response = stderr.decode().strip()
    t_response = stdout.decode()There aren't any subtitles to embed.strip()

    if e_response:
        print("Xtaolik:", e_response)
    elif t_response:
        print("Not error: ", t_response)

    return filepath

async def downloadaudiocli(command_to_exec):
    process = await create_subprocess_exec(
        *command_to_exec,

        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, )
    
