import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from helper_func import encode

# Define a global variable to store the title
hyperlink_titl = "Click Me"

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('flink'))
async def set_hyperlink_titl(client: Client, message: Message):
    global hyperlink_titl
    # Extract the title from the message text
    title = message.text.split("/flink ", 1)[-1]
    if title and title != '/flink':  # Check if the title is not empty and not equal to the command
        hyperlink_titl = title
        await message.reply_text(f"/Forward Message Hyperlink title set to: {hyperlink_titl}")
    else:
        await message.reply_text(f"Please provide a valid title.\n\nCurrent Forward Message's Hyperlink Title :- {hyperlink_titl}")

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','users','broadcast','batch','genlink','stats','donate','blink','glink','flink','refund','admin']))
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
        await reply_text.edit_text(
            f"<b>Links\n\nBot 1:</b> <a href='https://t.me/WMA_RQ1_bot?start={link}'>{hyperlink_titl}</a>\n\n"
            f"<b>Bot 2:</b> <a href='https://t.me/WebMoviesRebot?start={link}'>{hyperlink_titl}</a>", 
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    except Exception as e:
        print(e)
        await reply_text.edit_text("Failed to update links. Error: " + str(e))

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