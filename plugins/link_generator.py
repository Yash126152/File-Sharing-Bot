from pyrogram import Client, filters
from pyrogram.types import Message, Update, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS
from helper_func import encode, get_message_id

# Define a global variable to store the title
hyperlink_title = "480p 720p 1080p"

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('blink'))
async def set_hyperlink_title(client: Client, message: Message):
    global hyperlink_title
    # Extract the title from the message text
    title = message.text.split("/blink ", 1)[-1]
    if title and title != '/blink':  # Check if the title is not empty and not equal to the command
        hyperlink_title = title
        await message.reply_text(f"/Batch Hyperlink title set to: {hyperlink_title}")
    else:
        await message.reply_text(f"Please provide a valid title.\n\nCurrent Batch Hyperlink Title :- {hyperlink_title}")

# Define a global variable to store the title
hyperlink_titl = "Click Me"

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('glink'))
async def set_hyperlink_titl(client: Client, message: Message):
    global hyperlink_titl
    # Extract the title from the message text
    title = message.text.split("/glink ", 1)[-1]
    if title and title != '/glink':  # Check if the title is not empty and not equal to the command
        hyperlink_titl = title
        await message.reply_text(f"/Genlink Hyperlink title set to: {hyperlink_titl}")
    else:
        await message.reply_text(f"Please provide a valid title.\n\nGenlink Hyperlink Title :- {hyperlink_titl}")

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text=f"Forward the First Message from DB Channel (with Quotes)..\n\nor Send the <a href='https://t.me/+I_99FqoC8ABhYTU1'>DB Channel Post</a> Link\n\nCurrent Batch Hyperlink Title - ( {hyperlink_title} ) Change - /btitle\n\nTime Out in 2 Minutes", chat_id=message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=120)
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
            second_message = await client.ask(text=f"Forward the Last Message from DB Channel (with Quotes)..\nor Send the <a href='https://t.me/+I_99FqoC8ABhYTU1'>DB Channel Post</a> link\n\nCurrent Batch Hyperlink Title - ( {hyperlink_title} ) Change - /btitle\n\nTime Out in 2 Minutes", chat_id=message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=120)
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

    await second_message.reply_text(f"<b>Links 🔗\n\nBot1 :</b> <a href='https://t.me/WMA_RQ2_bot?start={link}'>{hyperlink_title}</a>\n\n<b>Bot2 :</b> <a href='https://t.me/WMA_RQ_BOT?start={link}'>{hyperlink_title}</a>", quote=True,
        disable_web_page_preview=True
    )

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text=f"Forward Message from the DB Channel (with Quotes)..\nor Send the <a href='https://t.me/+I_99FqoC8ABhYTU1'>DB Channel Post</a> link\n\nCurrent Hyperlink Title - ( {hyperlink_titl} ) Change - /gtitle\n\nTime Out in 1 Minutes", chat_id=message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
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
    await channel_message.reply_text(f"<b>Links 🔗\n\n<b>Bot 1:</b> <a href='https://t.me/WMA_RQ2_bot?start={link}'>{hyperlink_titl}</a>\n\n<b>Bot 2:</b> <a href='https://t.me/WMA_RQ_BOT?start={link}'>{hyperlink_titl}</a>", quote=True,
        disable_web_page_preview=True
    )