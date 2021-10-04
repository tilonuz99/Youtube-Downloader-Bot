import tempfile
from re import search
from json import loads
from urllib.parse import urlparse

from aiohttp import ClientSession
from aiohttp.client_reqrep import ClientResponse

import aiofiles
from utils.util import humanbytes


header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,fr;q=0.8,ro;q=0.7,ru;q=0.6,la;q=0.5,pt;q=0.4,de;q=0.3',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

cookies = {'csrftoken':	"lfo9sIGoNROMHTePniIFa7b3FpBFMDYq",
            'ds_user_id': "16192637034",
            'ig_did': "3271E12C-89CB-4528-ABB6-3CC9F42A8270",
            'ig_nrcb': "1", 'mid': "YVltKwAEAAGwCkBMI2dafpGULYMe", 'rur': "CLN\\05416192637034\\0541664790117:01f7c4b02a23923729a930ec2fc999b39cd4e0d09018496abad9cb8e7fb35e4fa7c9946d", 'sessionid': "16192637034:k35n51jK9ELLEG:3",
            'shbid': "10772\\05416192637034\\0541664786623:01f7ae0b390b073e3544a2e0cec447dba46759dde8343ca74467431832384e8c569c4da1",
            'shbts': "1633250623\\05416192637034\\0541664786623:01f718b5cc2201644c5f8e9cd9caaee6d51c808796baf04b2eec6dd46b18f55e7d9aaa62"}


async def fetch(client, video_url):

    async with client.get(video_url, headers=header, cookies=cookies) as resp:
        return await resp.text()


async def get_media_url(video_url):
    async with ClientSession() as client:
        htmls = await fetch(client, video_url)
        datas = search(
            r'window\.__additionalDataLoaded\s*\(\s*[^,]+,\s*({.+?})\s*\)\s*;', htmls)
        data = next(group for group in datas.groups() if group is not None)
        media = loads(data)
        media_data = media['graphql']['shortcode_media']
        if media_data['is_video']:
            media_url = media_data["video_url"]
        else:
            media_url = media_data['display_url']
        thumb_url = media_data['display_url']
        
        replaced_url = urlparse(media_url).netloc

        replaced_thumb_url = thumb_url.replace(replaced_url, 'scontent.cdninstagram.com', 1).strip()

        replaced_media_url = media_url.replace(replaced_url, 'scontent.cdninstagram.com', 1).strip()

        return replaced_media_url, replaced_thumb_url, media_data['is_video']


async def download_media(media_url):
    async with ClientSession() as session:
        async with session.get(media_url) as resp:
            if resp.status == 200:
                resp: ClientResponse = resp
                conntent_type = '.mp4' if resp.content_type.startswith('video') else '.jpg'
                tf = tempfile.NamedTemporaryFile(prefix="media_", suffix=conntent_type)
                file_name = tf.name.replace('/tmp/', 'downloads/')

                async with aiofiles.open(file_name, mode='wb') as f:
                    await f.write(await resp.read())
                
                return file_name