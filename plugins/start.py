import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT
from helper_func import check_subscription, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user

CHANNEL1_URL = "https://t.me/Cash_scope"
CHANNEL2_URL = "https://t.me/WMA_RQ"
LOG_CHANNEL = -1001916032450

@Bot.on_message(filters.command('donate') & filters.private)
async def donate_command(client: Client, message: Message):
    donate_message = (
        "🌟 Thank you for considering a donation! Your support helps us keep this bot running smoothly. 🌟\n\n"
        "You can donate using the link below:\n"
        "[Donate](https://oxapay.com/donate/25685660)"
    )

    await message.reply_text(
        text=donate_message,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    subscribed_channel1, subscribed_channel2 = await check_subscription(client, message)
    bot_info = await client.get_me()
    bot_username = bot_info.username

    if not await present_user(user_id):
        try:
            await add_user(user_id)
            await client.send_message(
                LOG_CHANNEL,
                f"#NewUser on @{bot_username}<br>\n"
                f"⬩ Username:  <a href='tg://user?id={user_id}'>{message.from_user.first_name}</a><br>\n"
                f"⬩ User ID: <code>{user_id}</ code>"
            )
        except Exception as e:
            print(f"Error adding user: {e}")
    if len(message.text) > 7:
        try:
            base64_string = message.text.split(" ", 1)[1]
        except IndexError:
            return
        string = await decode(base64_string)
        argument = string.split("-")

        if not subscribed_channel1 and not subscribed_channel2:
            await message.reply_text(
                "Dear User\n\nYou need to join in My Channel to use me\n\nKindly Please Join Channel",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="🛰 Join Channel 🛰", url="https://t.me/Cash_scope")],
                    [InlineKeyboardButton(text="🔄 Reload 🔄", url=f"https://t.me/{client.username}?start={message.command[1]}")]
                ])
            )
            return

        if not subscribed_channel1 or not subscribed_channel2:
            try:
                if len(argument) == 2:
                    ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                    messages = await get_messages(client, ids)
                    messagee = await messages[0].copy(chat_id=message.from_user.id)

                    # Add the new code block here
                    sent_message = await message.reply_text(
                        "𝔉𝔦𝔩𝔢𝔰 𝔴𝔦𝔩𝔩 𝔟𝔢 𝔡𝔢𝔩𝔢𝔱𝔢𝔡 𝔦𝔫 10 𝔪𝔦𝔫𝔲𝔱𝔢𝔰 𝔱𝔬 𝔞𝔳𝔬𝔦𝔡 𝔠𝔬𝔭𝔶𝔯𝔦𝔤𝔥𝔱 𝔦𝔰𝔰𝔲𝔢𝔰. ℙ𝕝𝕖𝕒𝕤𝕖 𝕗𝕠𝕣𝕨𝕒𝕣𝕕 𝕒𝕟𝕕 𝕤𝕒𝕧𝕖 𝕥𝕙𝕖𝕞.\n\nMake money with airdrops! Join the ones listed below and start earning free crypto today!",
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("Hamster Airdrop", url="https://t.me/hamster_kombat_boT/start?startapp=kentId1374193671"),
                            InlineKeyboardButton("PixelTap Airdrop", url="https://t.me/pixelversexyzbot?start=1374193671")]
                        ])
                    )

                    await asyncio.sleep(600)  # 600 seconds = 10 minutes

                    try:
                        await messagee.delete()
                        await sent_message.edit(
                            " Yᴏᴜʀ Vɪᴅᴇᴏ ɪꜱ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ 🥺",
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Restore Delete", url=f"https://t.me/{client.username}?start={message.command[1]}")]])
                        )
                    except Exception as e:
                        print(f"Error editing message: {e}")
                    return
                elif len(argument) == 3:
                    start = int(int(argument[1]) / abs(client.db_channel.id))
                    end = int(int(argument[2]) / abs(client.db_channel.id))

                    ids = list(range(start, end + 1))
                    num_files = len(ids)
                    half_files = num_files // 2
                    half_ids = ids[:half_files]

                    messages = await get_messages(client, half_ids)
                    sent_messages = []

                    for msg in messages:
                        new_caption = f"{msg.caption.html if msg.caption else ''}\n\n𝔉𝔦𝔩𝔢𝔰 𝔴𝔦𝔩𝔩 𝔟𝔢 𝔡𝔢𝔩𝔢𝔱𝔢𝔡 𝔦𝔫 10 𝔪𝔦𝔫𝔲𝔱𝔢𝔰 𝔱𝔬 𝔞𝔳𝔬𝔦𝔡 𝔠𝔬𝔭𝔶𝔯𝔦𝔤𝔥𝔱 𝔦𝔰𝔰𝔲𝔢𝔰. ℙ𝕝𝕖𝕒𝕤𝕖 𝕗𝕠𝕣𝕨𝕒𝕣𝕕 𝕒𝕟𝕕 𝕤𝕒𝕧𝕖 𝕥𝕙𝕖𝕞."
                        sent_msg = await msg.copy(
                            chat_id=message.from_user.id,
                            caption=new_caption,
                            parse_mode=ParseMode.HTML,
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("Hamster Airdrop", url="https://t.me/hamster_kombat_boT/start?startapp=kentId1374193671"),
                                InlineKeyboardButton("PixelTap Airdrop", url="https://t.me/pixelversexyzbot?start=1374193671")]
                            ])
                        )
                        sent_messages.append(sent_msg)

                    if num_files > half_files:
                        left_files = ids[half_files:]
                        left_file_names = []
                        for file_id in left_files:
                            try:
                                msg = await client.get_messages(client.db_channel.id, file_id)
                                if msg.document:
                                    file_name = msg.document.file_name
                                elif msg.video:
                                    file_name = msg.video.file_name
                                elif msg.photo:
                                    file_name = "Photo"
                                elif msg.text:
                                    file_name = "Text Message"
                                else:
                                    file_name = f"File Maybe Deleted From Database. Contact Developer File id - {file_id}"

                                # Remove words containing '@'
                                filtered_file_name = ' '.join(word for word in file_name.split() if '@' not in word)

                                # Use original file name if filtered name is empty
                                if not filtered_file_name:
                                    filtered_file_name = file_name

                                left_file_names.append(filtered_file_name)
                            except Exception as e:
                                if "Empty messages cannot be copied" in str(e):
                                    left_file_names.append("Dear User, this file is unfortunately deleted from the database. Please contact the Admin.")
                                else:
                                    left_file_names.append(f"Unknown file {file_id} (error: {e})")

                        left_files_info = "\n".join(f"{idx + 1}. {file_name}" for idx, file_name in enumerate(left_file_names))
                        must_channel_url = CHANNEL1_URL if subscribed_channel1 else CHANNEL2_URL
                        await message.reply_text(
                            f"Oops! Failed to send {num_files - half_files} files. Here are the remaining files:\n\n{left_files_info}\n\nJoin Channel To Get All Files.",
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton("🛰 Join Channel 🛰", url=must_channel_url)],
                                [InlineKeyboardButton("🔄 Reload 🔄", url=f"https://t.me/{client.username}?start={message.command[1]}")]
                            ])
                        )

                    await asyncio.sleep(600)  # Wait for 10 minutes before cleaning up
                    for sent_msg in sent_messages:
                        try:
                            await sent_msg.delete()
                        except Exception as e:
                            print(f"Error deleting messages: {e}")
                return
            except Exception as e:
                await message.reply_text(f"Something went wrong: {e}")
                return

        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1) if start <= end else range(start, end - 1, -1)
                num_files = len(ids)
                temp_msg = await message.reply(f"{num_files} Files Sending...")
            except Exception as e:
                await message.reply_text(f"Error processing arguments: {e}")
                return
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
                temp_msg = await message.reply("Sending File...")
            except Exception as e:
                await message.reply_text(f"Error processing arguments: {e}")
                return

        try:
            messages = await get_messages(client, ids)
        except Exception as e:
            await message.reply_text(f"Something went wrong: {e}")
            return
        await temp_msg.delete()

        snt_msgs = []

        for msg in messages:
            caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name) if CUSTOM_CAPTION and msg.document else (msg.caption.html if msg.caption else "")
            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

            try:
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                await asyncio.sleep(0.5)
                snt_msgs.append(snt_msg)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                snt_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                snt_msgs.append(snt_msg)
            except Exception as e:
                print(f"Error sending message: {e}")

        sent_message = await message.reply_text(
            "𝔉𝔦𝔩𝔢𝔰 𝔴𝔦𝔩𝔩 𝔟𝔢 𝔡𝔢𝔩𝔢𝔱𝔢𝔡 𝔦𝔫 10 𝔪𝔦𝔫𝔲𝔱𝔢𝔰 𝔱𝔬 𝔞𝔳𝔬𝔦𝔡 𝔠𝔬𝔭𝔶𝔯𝔦𝔤𝔥𝔱 𝔦𝔰𝔰𝔲𝔢𝔰. ℙ𝕝𝕖𝕒𝕤𝕖 𝕗𝕠𝕣𝕨𝕒𝕣𝕕 𝕒𝕟𝕕 𝕤𝕒𝕧𝕖 𝕥𝕙𝕖𝕞.\n\nMake money with airdrops! Join the ones listed below and start earning free crypto today!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Hamster Airdrop", url="https://t.me/hamster_kombat_boT/start?startapp=kentId1374193671"),
                InlineKeyboardButton("PixelTap Airdrop", url="https://t.me/pixelversexyzbot?start=1374193671")]
            ])
        )

        await asyncio.sleep(600)  # 600 seconds = 10 minutes

        try:
            await sent_message.edit(
                "Your video(es) is successfully deleted 🥺",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Restore Delete", url=f"https://t.me/{client.username}?start={message.command[1]}")]])
            )
        except Exception as e:
            print(f"Error editing message: {e}")
        for snt_msg in snt_msgs:
            try:
                await snt_msg.delete()
            except Exception as e:
                print(f"Error deleting sent message: {e}")
        return

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⚡️ About", callback_data="about"),
                InlineKeyboardButton('🍁 Provided By', url='https://t.me/WMA_RQ')
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