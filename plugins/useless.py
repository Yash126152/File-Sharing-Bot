from bot import Bot
from pyrogram.types import Message, ChatPermissions
from pyrogram import filters
from config import ADMINS, BOT_STATS_TEXT, USER_REPLY_TEXT
from datetime import datetime
from helper_func import get_readable_time
from pyrogram.errors import FloodWait
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Bot and channel details
BOT_ID = 7171429665
CHANNEL_ID = -1001954696718

# List of commands to ignore
IGNORE_COMMANDS = ['/start', '/users', '/broadcast', '/batch', '/genlink', '/stats', '/donate', '/blink', '/glink', '/flink', '/refund', '/admin']

# Command to get bot statistics
@Bot.on_message(filters.command('stats') & filters.user(ADMINS))
async def stats(bot: Bot, message: Message):
    now = datetime.now()
    delta = now - bot.uptime
    time = get_readable_time(delta.seconds)
    await message.reply(BOT_STATS_TEXT.format(uptime=time))

# Command to give the bot invite users permission in the specified channel
@Bot.on_message(filters.command('grant_invite_permission') & filters.user(ADMINS))
async def grant_invite_permission(bot: Bot, message: Message):
    try:
        await bot.set_chat_permissions(
            chat_id=CHANNEL_ID,
            permissions=ChatPermissions(
                can_invite_users=True
            )
        )
        await message.reply("Invite users permission granted to the bot in the specified channel.")
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await message.reply(f"Rate limit exceeded. Please try again in {e.x} seconds.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

# Command to handle incoming private messages
@Bot.on_message(filters.private & filters.incoming)
async def useless(_, message: Message):
    # Check if the message is a command in the ignore list
    if message.text and (message.text.lower() in IGNORE_COMMANDS or message.text.isdigit()):
        return

    if USER_REPLY_TEXT:
        await message.reply(USER_REPLY_TEXT)