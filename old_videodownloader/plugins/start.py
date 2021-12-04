from pyrogram import Client, filters, StopPropagation
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.database.models import Users

@Client.on_message(filters.command(["start"]), group=-2)
async def start(client, message):
    # return
    joinButton = InlineKeyboardMarkup([
        [InlineKeyboardButton("Channel", url="https://t.me/aryan_bots")],
        [InlineKeyboardButton(
            "Report Bugs 😊", url="https://t.me/aryanvikash")]
    ])
    welcomed = f"Hey <b>{message.from_user.first_name}</b>\n/help for More info"
    await message.reply_text(welcomed, reply_markup=joinButton)
    try:
        await Users.create(chat_id=message.from_user.id)
    except:
        pass

    # raise StopPropagation
