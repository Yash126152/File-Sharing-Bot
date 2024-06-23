import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import check_subscription, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user
from database.air_db import secondary_present_user, secondary_add_user

# Replace with your admin user IDs
ADMIN_IDS = [1374193671, 6357617991]  # Example admin IDs

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    subscribed_channel1, subscribed_channel2 = await check_subscription(client, message)
    is_present_in_airdrop = await secondary_present_user(user_id)

    if not subscribed_channel1 and not subscribed_channel2 and not is_present_in_airdrop:
        buttons = [
            [InlineKeyboardButton(text="Join Channel 1", url="https://t.me/Cash_scope")],
            [InlineKeyboardButton(text="Join Channel 2", url="https://t.me/WMA_RQ")],
            [InlineKeyboardButton(text="Join Airdrop", url="https://t.me/community_bot/join?startapp=id_396-r_MTk1MTc1MzZfMzUwNA==")]
        ]
        await message.reply(
            text="You must join the required channels and the airdrop to use me.",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
        return

    if not subscribed_channel1 and subscribed_channel2 and is_present_in_airdrop:
        buttons = [
            [InlineKeyboardButton(text="Join Channel", url="https://t.me/Cash_scope")]
        ]
        await message.reply(
            text="I think you forgot to join Channel or You left it.",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
        return

    if subscribed_channel1 and not subscribed_channel2 and is_present_in_airdrop:
        buttons = [
            [InlineKeyboardButton(text="Join Channel", url="https://t.me/WMA_RQ")]
        ]
        await message.reply(
            text="I think you forgot to join Channel or You left it.",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
        return

    if subscribed_channel1 and subscribed_channel2 and not is_present_in_airdrop:
        buttons = [
            [InlineKeyboardButton(text="Join Airdrop", url="https://t.me/community_bot/join?startapp=id_396-r_MTk1MTc1MzZfMzUwNA==")]
        ]
        await message.reply_photo(
            photo="https://telegra.ph/file/db33645e979836f48cf5f.jpg",
            caption=(
                "Complete the airdrop task to use me.\n\n"
                "For help, use the image above.\n\n"
                "Note: Send Me screenshot for verification. "
                "This is not an automatic verification; it is done manually. So it Take Some Time"
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
        return

    if not subscribed_channel1 or not subscribed_channel2 and not is_present_in_airdrop:
        buttons = []
        if not subscribed_channel1:
            buttons.append([InlineKeyboardButton(text="Join Channel 1", url="https://t.me/Cash_scope")])
        if not subscribed_channel2:
            buttons.append([InlineKeyboardButton(text="Join Channel 2", url="https://t.me/WMA_RQ")])
        buttons.append([InlineKeyboardButton(text="Join Airdrop", url="https://t.me/community_bot/join?startapp=id_396-r_MTk1MTc1MzZfMzUwNA==")])
        await message.reply(
            text="You must join the required channel and the airdrop to use me.",
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True
        )
        return

    # Proceed with the existing functionality if the user is subscribed and joined the airdrop
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Wait a second...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong!")
            return
        await temp_msg.delete()

        snt_msgs = []

        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html,
                                                filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                                         reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
                snt_msgs.append(snt_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                                         reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                snt_msgs.append(snt_msg)
            except:
                pass
        sent_message = await message.reply_text("Files will be deleted in 10 minutes to avoid copyright issues. Please forward and save them.")

        # Add a delay of 10 minutes before editing the message
        await asyncio.sleep(600)

        # Edit the message
        try:
            await sent_message.edit("Your file/video has been successfully deleted 🥺", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Restore Deleted", url=f"https://t.me/{client.username}?start={message.command[1]}")]]))
        except:
            pass
        for snt_msg in snt_msgs:
            try:
                await snt_msg.delete()
            except:
                pass
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⚡️ ᴀʙᴏᴜᴛ", callback_data="about"),
                    InlineKeyboardButton('🍁 Provide By', url='https://t.me/WMA_RQ')
                ]
            ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return

@Bot.on_message(filters.command('add') & filters.private)
async def add_user_command(client: Client, message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("You are not authorized to use this command.")
        return

    try:
        user_id_to_add = int(message.text.split()[1])
    except IndexError:
        await message.reply("Please provide a user ID to add.")
        return
    except ValueError:
        await message.reply("Invalid user ID provided.")
        return

    if await secondary_present_user(user_id_to_add):
        await message.reply("User is already added to the secondary database.")
    else:
        await secondary_add_user(user_id_to_add)
        await message.reply(f"User {user_id_to_add} has been added to the secondary database.")


#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a reply to any telegram message without any spaces.</code>"""

#=====================================================================================##


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")


@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass

        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()