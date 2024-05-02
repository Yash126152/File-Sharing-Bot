import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats','donate']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"{base64_string}"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("📂 Get File", url=f'https://t.me/{client.username}?start={link}')]])

    try:
        await reply_text.edit(f"<b>links 🔗</b>\n\nBot 1 - <code>https://t.me/WMA_RQ1_bot?start={link}</code>\n\nBot 2 - <code>https://t.me/WMA_RQ2_bot?start={link}</code>\n\nBot 3 - <code>https://t.me/WMA_RQ_bot?start={link}</code>\n\nBot 4 - <code>https://t.me/WebMoviesRebot?start={link}</code>", reply_markup=reply_markup)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Failed to update links. Error: " + str(e))

    try:
        await message.reply_text(f"<b>Links 🔗\n\nBot 1:</b> <a href='https://t.me/WMA_RQ1_bot?start={link}'>Click Me</a>\n\n<b>Bot 2:</b> <a href='https://t.me/WMA_RQ2_bot?start={link}'>Click Me</a>\n\n<b>Bot 3:</b> <a href='https://t.me/WMA_RQ_bot?start={link}'>Click Me</a>\n\n<b>Bot 4:</b> <a href='https://t.me/WebMoviesRebot?start={link}'>Click Me</a>", quote=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Failed to reply with links.")
    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass
