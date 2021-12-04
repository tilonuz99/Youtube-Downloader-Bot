from tortoise.models import Model
from tortoise import fields, Tortoise

class Users(Model):
    id = fields.BigIntField(pk=True)
    chat_id = fields.BigIntField(unique=True)

class Admin_channels(Model):
    id = fields.BigIntField(pk=True)
    channel_url = fields.TextField(max_length=255)

class Youtube_videos(Model):
    id = fields.BigIntField(pk=True)
    video_url = fields.TextField(max_length=255)
    title = fields.TextField(max_length=255)
    thumbnail = fields.TextField(max_length=255, null=True)

    def __int__(self):
        return self.id


class Video_formats(Model):
    id = fields.BigIntField(pk=True)
    format_type = fields.TextField(max_length=200)
    format_id = fields.BigIntField()
    file_size = fields.BigIntField()
    video = fields.ForeignKeyField("models.Youtube_videos", related_name='video_format')

class Dowmloaded_media(Model):
    id = fields.BigIntField(pk=True)
    file_id = fields.TextField(max_length=255)
    video = fields.ForeignKeyField("models.Youtube_videos", related_name='downloaded_media')
    video_format = fields.ForeignKeyField("models.Video_formats", related_name='format')


async def connect_database():
    await Tortoise.init(
        db_url="sqlite://database.db", modules={"models": [__name__]}
    )
    await Tortoise.generate_schemas()