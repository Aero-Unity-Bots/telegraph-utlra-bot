
# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

import asyncio
import html
import time

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    InputMediaPhoto,
)
from utils.user_settings import get_user_settings
from database import add_user, total_users, total_posts, posts

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

START_IMAGE = (
    "https://telegra.ph/file/7b935e63ed6fee8c999f3-6dbf85b31ac01389e4.jpg"
)

ABOUT_IMAGE = (
    "https://telegra.ph/file/3fc5ec05583af1b0f9698-7c30a1d7b2204cc8e1.jpg"
)

BOT_START_TIME = time.time()

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

START_TEXT = """
<b>👋 Wᴇʟᴄᴏᴍᴇ Tᴏ Uʟᴛʀᴀ Tᴇʟᴇɢʀᴀᴘʜ Bᴏᴛ</b>
<blockquote>
Create detailed MediaInfo pages and manage your Telegraph account easily.
</blockquote>
<b>Choose an option below.</b>
"""

ABOUT_TEXT = """
<b> Mʏ Dᴇᴛᴀɪʟs</b>

<b>Lᴀɴɢᴜᴀɢᴇ :</b> <a href="https://www.python.org/">Pʏᴛʜᴏɴ 𝟹</a>
<b>Lɪʙʀᴀʀʏ :</b> <a href="https://docs.pyrogram.org/">Pʏʀᴏɢʀᴀᴍ</a>
<b>Dᴀᴛᴀʙᴀsᴇ :</b> <a href="https://www.mongodb.com/">MᴏɴɢᴏDB</a>
<b>Dᴏᴍᴀɪɴ :</b> <a href="https://telegra.ph/">Tᴇʟᴇɢʀᴀᴘʜ</a>
<b>Uᴘᴅᴀᴛᴇs :</b> <a href="https://t.me/Aero_Unity">Aᴇʀᴏ Uɴɪᴛʏ</a>
<b>Dᴇᴠᴇʟᴏᴘᴇʀ :</b> <a href="https://t.me/Mr_Mohammed_29">Mᴏʜᴀᴍᴍᴇᴅ</a>
"""

HELP_TEXT = """
<b>❓ HELP MENU</b>

• Reply to a video or document with <code>/tgm</code>
to create a detailed MediaInfo Telegraph page.

<b>Available Commands:</b>

<code>/tgm</code> - Create a Telegraph link
<code>/settings</code> - Check Your Details and Posts
<code>/screenshot</code> - Generate video screenshots
<code>/sample</code> - Generate a short video sample
<code>/spek</code> - Generate an audio spectrogram

<b>Need help?</b> Contact the Owner.
"""

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def start_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "• Aʙᴏᴜᴛ •",
                callback_data="about"
            ),
            InlineKeyboardButton(
                "• Hᴇʟᴘ •",
                callback_data="help"
            ),
        ],
        [
            InlineKeyboardButton(
                "• Uᴘᴅᴀᴛᴇs •",
                url="https://t.me/Aero_Unity"
            ),
            InlineKeyboardButton(
                "• Dᴇᴠᴇʟᴏᴘᴇʀ •",
                url="https://t.me/Mr_Mohammed_29"
            ),
        ],
    ])

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def home_button():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "• Hᴏᴍᴇ •",
                callback_data="start_home"
            )
        ]
    ])

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def about_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "• Uᴘᴅᴀᴛᴇs •",
                url="https://t.me/Aero_Unity"
            ),
            InlineKeyboardButton(
                "• Dᴇᴠᴇʟᴏᴘᴇʀ •",
                url="https://t.me/Mr_Mohammed_29"
            ),
        ],
        [
            InlineKeyboardButton(
                "• Hᴏᴍᴇ •",
                callback_data="start_home"
            )
        ],
    ])


# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def settings_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "• Rᴇsᴇᴛ Aʟʟ •",
                callback_data="reset_settings"
            ),
        ],
        [
            InlineKeyboardButton(
                "• Uᴘᴅᴀᴛᴇs •",
                url="https://t.me/Aero_Unity"
            ),
            InlineKeyboardButton(
                " • Dᴇᴠᴇʟᴏᴘᴇʀ •",
                url="https://t.me/Mr_Mohammed_29"
            ),
        ],
        [
            InlineKeyboardButton(
                "• Cʟᴏsᴇ",
                callback_data="close_menu"
            ),
        ],
    ])

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def stats_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "• Rᴇғʀᴇsʜ •",
                callback_data="refresh_stats"
            ),
            InlineKeyboardButton(
                "• Cʟᴏsᴇ •",
                callback_data="close_menu"
            ),
        ],
        [
            InlineKeyboardButton(
                "• Hᴏᴍᴇ •",
                callback_data="start_home"
            ),
        ],
    ])

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_uptime():
    seconds = int(time.time() - BOT_START_TIME)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    return (
        f"{days}d {hours}h "
        f"{minutes}m {seconds}s"
    )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def show_menu(query, text, buttons, photo=None):
    msg = query.message

    try:
        if msg.photo:
            if photo:
                await msg.edit_media(
                    media=InputMediaPhoto(
                        media=photo,
                        caption=text,
                    ),
                    reply_markup=buttons,
                )
            else:
                await msg.edit_caption(
                    caption=text,
                    reply_markup=buttons,
                )

        elif photo:
            await msg.delete()
            await query.message.reply_photo(
                photo=photo,
                caption=text,
                reply_markup=buttons,
            )

        else:
            await msg.edit_text(
                text,
                reply_markup=buttons,
                disable_web_page_preview=True,
            )

    except Exception as error:
        if "MESSAGE_NOT_MODIFIED" not in str(error):
            raise

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def get_settings_text(client, user_id):
    user = await client.get_users(user_id)
    first_name = user.first_name or "User"
    username = user.username

    if username:
        user_link = (
            f'<a href="https://t.me/{html.escape(username)}">'
            f'@{html.escape(username)}</a>'
        )
    else:
        user_link = (
            f'<a href="tg://user?id={user_id}">'
            f'{html.escape(first_name)}</a>'
        )

    user_data = get_user_settings(
        user_id,
        telegram_first_name=first_name,
    )

    account_name = html.escape(
        str(user_data.get("account_name", first_name))
    )

    author_name = html.escape(
        str(user_data.get("author_name", first_name))
    )

    post_count = posts.count_documents({
        "user_id": user_id
    })

    dc_id = "Unknown"

    if user.photo:
        dc_id = getattr(user.photo, "dc_id", "Unknown")

    text = f"""
<b>⚙️ Sᴇᴛᴛɪɴɢs</b>

<b>👤 Nᴀᴍᴇ  :</b> {account_name}
<b>👤 Usᴇʀɴᴀᴍᴇ :</b> {user_link}
<b>🆔 ID :</b> <code>{user_id}</code>
<b>🌐 Dᴀᴛᴀ Cᴇɴᴛᴇʀ ID :</b> <code>{dc_id}</code>
<b>📁 Dᴏᴍᴀɪɴ :</b> Tᴇʟᴇɢʀᴀᴘʜ
<b>📝 Tᴏᴛᴀʟ Pᴏsᴛs :</b> <code>{post_count}</code>
"""
    profile_photo = None

    if user.photo:
        profile_photo = user.photo.big_file_id

    return text, profile_photo

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def get_stats_text(client):
    start = time.perf_counter()

    bot = await client.get_me()

    ping = (time.perf_counter() - start) * 1000

    username = (
        f"@{html.escape(bot.username)}"
        if bot.username
        else "Not Available"
    )

    users = total_users()
    posts_count = total_posts()

    text = f"""
<b>📊 Bᴏᴛ Sᴛᴀᴛɪsᴛɪᴄs</b>

👤 <b>Usᴇʀɴᴀᴍᴇ :</b> {username}
🆔 <b>Bᴏᴛ ID :</b> <code>{bot.id}</code>
👥 <b>Tᴏᴛᴀʟ Usᴇʀs :</b> <code>{users}</code>
📝 <b>Tᴏᴛᴀʟ Pᴏsᴛs :</b> <code>{posts_count}</code>
⚡ <b>Pɪɴɢ :</b> <code>{ping:.2f} ms</code>
⏳ <b>Bᴏᴛ Uᴘᴛɪᴍᴇ :</b> <code>{get_uptime()}</code>

<b>›› Pᴏᴡᴇʀᴇᴅ Bʏ :</b> @Aero_Unity
"""
    return text

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_message(filters.command("start"))
async def start(client, message):
    if not message.from_user:
        return

    try:
        add_user(message.from_user.id)
    except Exception as error:
        print(f"Add user error: {error}")

    status = await message.reply_text(
        "⚡ Wᴇʟᴄᴏᴍɪɴɢ Yᴏᴜ . . ."
    )

    await asyncio.sleep(0.5)

    try:
        await status.delete()
    except Exception:
        pass

    await message.reply_photo(
        photo=START_IMAGE,
        caption=START_TEXT,
        reply_markup=start_buttons(),
    )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):
    data = query.data

    if not data:
        return
        
    if data == "about":
        try:
            await show_menu(
                query,
                ABOUT_TEXT,
                about_buttons(),
                photo=ABOUT_IMAGE,
            )
            await query.answer()

        except Exception as error:
            await query.answer(
                f"Unable to open About: {str(error)[:100]}",
                show_alert=True,
            )

    elif data == "help":
        try:
            await show_menu(
                query,
                HELP_TEXT,
                home_button(),
                photo=ABOUT_IMAGE,
            )
            await query.answer()

        except Exception as error:
            await query.answer(
                f"Unable to open Help: {str(error)[:100]}",
                show_alert=True,
            )

    elif data == "start_home":
        try:
            await show_menu(
                query,
                START_TEXT,
                start_buttons(),
                photo=START_IMAGE,
            )
            await query.answer()

        except Exception as error:
            await query.answer(
                f"Unable to return Home: {str(error)[:100]}",
                show_alert=True,
            )

    elif data == "settings_panel":
        try:
            text, profile_photo = await get_settings_text(
                client,
                query.from_user.id,
            )

            await show_menu(
                query,
                text,
                settings_buttons(),
                photo=profile_photo,
            )

            await query.answer()

        except Exception as error:
            await query.answer(
                f"Settings error: {str(error)[:150]}",
                show_alert=True,
            )

    elif data == "open_stats":
        try:
            text = await get_stats_text(client)

            await show_menu(
                query,
                text,
                stats_buttons(),
            )

            await query.answer()

        except Exception as error:
            await query.answer(
                f"Statistics error: {str(error)[:120]}",
                show_alert=True,
            )

    elif data == "refresh_stats":
        try:
            text = await get_stats_text(client)

            await show_menu(
                query,
                text,
                stats_buttons(),
            )

            await query.answer("Statistics refreshed!")

        except Exception as error:
            await query.answer(
                f"Refresh failed: {str(error)[:120]}",
                show_alert=True,
            )

    elif data == "reset_settings":
        try:
            from utils.user_settings import reset_user_settings

            reset_user_settings(query.from_user.id)

            text, profile_photo = await get_settings_text(
                client,
                query.from_user.id,
            )

            await show_menu(
                query,
                "<b>✅ Settings reset successfully.</b>\n\n" + text,
                settings_buttons(),
                photo=profile_photo,
            )

            await query.answer("Settings reset successfully!")

        except Exception as error:
            await query.answer(
                f"Unable to reset settings: {str(error)[:120]}",
                show_alert=True,
            )

    elif data == "close_menu":
        try:
            await query.message.delete()
            await query.answer("Menu closed!")

        except Exception as error:
            await query.answer(
                f"Unable to close: {str(error)[:100]}",
                show_alert=True,
            )

    else:
        return


# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #