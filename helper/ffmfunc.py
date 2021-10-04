import subprocess as sp
import json
import asyncio

async def probe(vid_file_path):

    command_to_exec = ["ffprobe",
               "-loglevel", "quiet",
               "-print_format", "json",
               "-show_format",
               "-show_streams",
               vid_file_path
               ]

    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE, )
    out, err = await process.communicate()
    
    return json.loads(out)


async def duration(vid_file_path):
    """
    Video's duration in seconds, return a float number
    """
    _json = await probe(vid_file_path)

    if 'format' in _json:
        if 'duration' in _json['format']:
            return float(_json['format']['duration'])

    if 'streams' in _json:
        # commonly stream 0 is the video
        for s in _json['streams']:
            if 'duration' in s:
                return float(s['duration'])

    raise Exception('duration Not found')
