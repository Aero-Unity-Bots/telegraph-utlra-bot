# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

import asyncio
import html

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from database import add_user, total_users, total_posts

# ------------------------- #
# CONFIG
# ------------------------- #

START_IMAGE = (
    "https://telegra.ph/file/7b935e63ed6fee8c999f3-6dbf85b31ac01389e4.jpg"
)

ABOUT_IMAGE = (
    "https://telegra.ph/file/3fc5ec05583af1b0f9698-7c30a1d7b2204cc8e1.jpg"
)

START_TEXT = """
<b>Welcome To Ultra Telegraph Bot</b>
"""

ABOUT_TEXT = """
<b>🤖 ABOUT THIS BOT</b>

<b>Language :</b> <a href="https://www.python.org/">Python 3</a>
<b>Library :</b> <a href="https://docs.pyrogram.org/">Pyrogram</a>
<b>Database :</b> <a href="https://www.mongodb.com/">MongoDB</a>
<b>Domain :</b> <a href="https://telegra.ph/">Telegraph</a>
<b>Updates :</b> <a href="https://t.me/Aero_Unity">Aero_Unity</a>
<b>Owner :</b> <a href="https://t.me/Mr_Mohammed_29">Mohammed</a>
"""

HELP_TEXT = """
<b>❓ HELP MENU</b>

• Reply to a video or document with <code>/tgm</code>
to create a detailed MediaInfo Telegraph page.

<b>/tgm</b> - Create a Telegraph link
<b>/screenshot</b> - Generate video screenshots
<b>/sample</b> - Generate a short video sample
<b>/spek</b> - Generate an audio spectrogram
"""

# ------------------------- #
# BUTTONS
# ------------------------- #

def start_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("• About •", callback_data="about"),
            InlineKeyboardButton("• Help •", callback_data="help"),
        ],
        [
            InlineKeyboardButton("• Updates •", url="https://t.me/Aero_Unity"),
            InlineKeyboardButton("• Owner •", url="https://t.me/Mr_Mohammed_29"),
        ],
        [
            InlineKeyboardButton("• Settings •", callback_data="settings_panel"),
        ],
    ])


def home_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("• Home •", callback_data="start_home")]
    ])


def about_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("• Updates •", url="https://t.me/Aero_Unity"),
            InlineKeyboardButton("• Owner •", url="https://t.me/Mr_Mohammed_29"),
        ],
        [InlineKeyboardButton("• Home •", callback_data="start_home")],
    ])


def settings_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Reset All", callback_data="reset_settings"),
        ],
        [
            InlineKeyboardButton("• Home •", callback_data="start_home"),
        ],
    ])


# ------------------------- #
# EDIT CURRENT MENU
# ------------------------- #

async def show_menu(query, text, buttons, photo=None):
    """Update the existing menu message instead of sending a new message."""

    msg = query.message

    try:
        if msg.photo:
            if photo:
                await msg.edit_media(
                    media=__import__(
                        "pyrogram"
                    ).types.InputMediaPhoto(
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


# ------------------------- #
# START COMMAND
# ------------------------- #

@Client.on_message(filters.command("start"))
async def start(client, message):
    try:
        add_user(message.from_user.id)
    except Exception:
        pass

    status = await message.reply_text("⚡ Wᴇʟᴄᴏᴍɪɴɢ Yᴏᴜ . . .")
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


# ------------------------- #
# CALLBACK HANDLER
# ------------------------- #

@Client.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):
    data = query.data

    await query.answer()

    # ABOUT
    if data == "about":
        try:
            await show_menu(
                query,
                ABOUT_TEXT,
                about_buttons(),
                photo=ABOUT_IMAGE,
            )
        except Exception:
            await query.answer("Unable to open About.", show_alert=True)

    # HELP
    elif data == "help":
        try:
            await show_menu(
                query,
                HELP_TEXT,
                home_button(),
                photo=ABOUT_IMAGE,
            )
        except Exception:
            await query.answer("Unable to open Help.", show_alert=True)

    # HOME
    elif data == "start_home":
        try:
            await show_menu(
                query,
                START_TEXT,
                start_buttons(),
                photo=START_IMAGE,
            )
        except Exception:
            await query.answer("Unable to return Home.", show_alert=True)

    # SETTINGS
    elif data == "settings_panel":
        try:
            from utils.user_settings import get_user_settings
            from database import posts

            user_id = query.from_user.id
            user = await client.get_users(user_id)
            first_name = user.first_name or "User"

            post_count = posts.count_documents({"user_id": user_id})

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

            text = f"""
<b>⚙️ ACCOUNT SETTINGS</b>

<b>User ID :</b> <code>{user_id}</code>
<b>Domain :</b> Telegraph
<b>Account Name :</b> {account_name}
<b>Author Name :</b> {author_name}
<b>No. of Posts :</b> {post_count}
"""

            await show_menu(
                query,
                text,
                settings_buttons(),
            )

        except Exception as error:
            await query.answer(
                f"Settings error: {str(error)[:150]}",
                show_alert=True,
            )

    # REFRESH STATS
    elif data == "refresh_stats":
        try:
            users = total_users()
            posts_count = total_posts()

            text = f"""
<b>📊 BOT STATISTICS</b>

👥 <b>Total Users :</b> {users}
📝 <b>Total Posts :</b> {posts_count}
<b>Powered By :</b> @Aero_Unity
"""

            await show_menu(query, text, home_button())

        except Exception:
            await query.answer("Database error.", show_alert=True)

    # RESET SETTINGS
    elif data == "reset_settings":
        try:
            from utils.user_settings import reset_user_settings

            reset_user_settings(query.from_user.id)

            await show_menu(
                query,
                "<b>✅ Settings reset completed.</b>",
                settings_buttons(),
            )

        except Exception:
            await query.answer(
                "Unable to reset settings.",
                show_alert=True,
            )

    elif data == "noop":
        return


# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #
