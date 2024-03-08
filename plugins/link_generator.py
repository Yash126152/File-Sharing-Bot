from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text="Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link", chat_id=message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote=True)
            continue

    while True:
        try:
            second_message = await client.ask(text="Forward the Last Message from DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id=message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote=True)
            continue

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"{base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("📂 Get Files", url=f'https://t.me/{client.username}?start={link}')]])
    await second_message.reply_text(f"<b>links 🔗</b>\n\nBot1 - <code>https://t.me/WMA_RQ1_bot?start={link}</code>\n\nBot2 - <code>https://t.me/WMA_RQ2_bot?start={link}</code>\n\nBot3 - <code>https://t.me/WMA_RQ_bot?start={link}</code>\n\nBot4 - <code>https://t.me/WebMoviesRebot?start={link}</code>", quote=True, reply_markup=reply_markup)
    await message.reply_text(f"<b>Links 🔗\n\nBot1:</b> <a href='https://t.me/WMA_RQ1_bot?start={link}'>480p 720p 1080p</a>\n\n<b>Bot2:</b> <a href='https://t.me/WMA_RQ2_bot?start={link}'>480p 720p 1080p</a>\n\n<b>Bot3:</b> <a href='https://t.me/WMA_RQ_bot?start={link}'>480p 720p 1080p</a>\n\n<b>Bot4:</b> <a href='https://t.me/WebMoviesRebot?start={link}'>480p 720p 1080p</a>", quote=True)

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text="Forward Message from the DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id=message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is not taken from DB Channel", quote=True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"{base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("📂 Get File", url=f'https://t.me/{client.username}?start={link}')]])
    await channel_message.reply_text(f"<b>links</b>\n\nBot 1 - <code>https://t.me/WMA_RQ1_bot?start={link}</code>\n\nBot 2 - <code>https://t.me/WMA_RQ2_bot?start={link}</code>\n\nBot 3 - <code>https://t.me/WMA_RQ_bot?start={link}</code>\n\nBot 4 - <code>https://t.me/WebMoviesRebot?start={link}</code>", quote=True, reply_markup=reply_markup)
    await message.reply_text(f"<b>Bot 1:</b> <a href='https://t.me/WMA_RQ1_bot?start={link}'>Click Me</a>\n\n<b>Bot 2:</b> <a href='https://t.me/WMA_RQ2_bot?start={link}'>Click Me</a>\n\n<b>Bot 3:</b> <a href='https://t.me/WMA_RQ_bot?start={link}'>Click Me</a>\n\n<b>Bot 4:</b> <a href='https://t.me/WebMoviesRebot?start={link}'>Click Me</a>", quote=True)
