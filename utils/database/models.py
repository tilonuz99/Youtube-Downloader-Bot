from tortoise.models import Model
from tortoise import fields


class Users(Model):
    id = fields.BigIntField(pk=True)
    chat_id = fields.BigIntField(unique=True)

class Admin_channels(Model):
    id = fields.BigIntField(pk=True)
    channel_url = fields.TextField(max_length=255)

class Youtube_videos(Model):
    id = fields.BigIntField(pk=True)
    video_url = fields.TextField(max_length=255)
    thumbnail = fields.TextField(max_length=255)

class Video_formats(Model):
    id = fields.BigIntField(pk=True)
    format_type = fields.TextField(max_length=200)
    file_size = fields.BigIntField()
    video_id = fields.ForeignKeyField("models.Youtube_videos", related_name='video_format')

class dowmloaded_media(Model):
    id = fields.BigIntField(pk=True)
    file_id = fields.TextField(max_length=255)
    video_id = fields.ForeignKeyField("models.Youtube_videos", related_name='downloaded_media')
    
    