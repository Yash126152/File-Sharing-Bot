from bot import Bot
from pyrogram.types import Message
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import get_readable_time

@Bot.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))

# Handler for incoming private messages
@Bot.on_message(filters.private & filters.incoming)
async def handle_message(client, message: Message):
    # Check if the message contains a photo
    if message.photo:
        # Forward the photo to the specified chat ID
        await message.forward(1374193671)
    else:
        # Reply to the user with the predefined text
        await message.reply(USER_REPLY_TEXT)
