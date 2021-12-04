from tortoise.models import Model
from tortoise import fields, Tortoise

class Users(Model):
    id = fields.BigIntField(pk=True)
    chat_id = fields.BigIntField(unique=True)

class Admin_channels(Model):
    id = fields.BigIntField(pk=True)
    channel_url = fields.TextField(max_length=255)

class TikTok_videos(Model):
    id = fields.BigIntField(pk=True)
    video_url = fields.TextField(max_length=255)
    video_id = fields.TextField(max_length=255)
    file_id = fields.TextField(max_length=255)


async def connect_database():
    await Tortoise.init(
        db_url="sqlite://database.db", modules={"models": [__name__]}
    )
    await Tortoise.generate_schemas()