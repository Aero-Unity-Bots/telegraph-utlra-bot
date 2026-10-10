
# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

import asyncio

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

<b>/tgm</b> Reply To Documents,videos to get link
<b>/screenshot</b> - Generate video screenshots relpy with media
<b>/sample</b> - Generate a short video sample reply with media
<b>/spek</b> - Generate an audio spectrogram reply with media
"""

# ------------------------- #
# START BUTTONS
# ------------------------- #

def start_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "• About •",
                callback_data="about"
            ),
            InlineKeyboardButton(
                "• Help •",
                callback_data="help"
            )
        ],
        [
            InlineKeyboardButton(
                "• Updates •",
                url="https://t.me/Aero_Unity"
            ),
            InlineKeyboardButton(
                "• Owner •",
                url="https://t.me/Mr_Mohammed_29"
            )
        ],
        [
            InlineKeyboardButton(
                "• Settings •",
                callback_data="settings_panel"
            )
        ],
    ])


def home_button():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "• Home •",
                callback_data="start_home"
            )
        ]
    ])


def about_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "• Updates •",
                url="https://t.me/Aero_Unity"
            ),
            InlineKeyboardButton(
                "• Owner •",
                url="https://t.me/Mr_Mohammed_29"
            )
        ],
        [
            InlineKeyboardButton(
                "• Home •",
                callback_data="start_home"
            )
        ]
    ])


def stats_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "• Refresh •",
                callback_data="refresh_stats"
            )
        ],
        [
            InlineKeyboardButton(
                "• Home •",
                callback_data="start_home"
            )
        ]
    ])


# ------------------------- #
# START COMMAND
# ------------------------- #

@Client.on_message(filters.command("start"))
async def start(client, message):

    try:
        add_user(message.from_user.id)
    except Exception:
        pass

    status = await message.reply_text(
        "🚀 Sʜᴀᴅᴏᴡ Oғ Mᴏɴᴀʀᴄʜ . . ."
    )

    await asyncio.sleep(0.5)
    await status.edit_text("🎊")

    await asyncio.sleep(0.5)
    await status.edit_text("⚡")

    await asyncio.sleep(0.5)
    await status.edit_text("🤖 Wᴇʟᴄᴏᴍɪɴɢ Yᴏᴜ . . .")

    await asyncio.sleep(0.7)
    await status.delete()

    await message.reply_photo(
        photo=START_IMAGE,
        caption=START_TEXT,
        reply_markup=start_buttons()
    )


# ------------------------- #
# CALLBACK HANDLER
# ------------------------- #

@Client.on_callback_query()
async def callback_handler(client: Client, query: CallbackQuery):

    data = query.data

    try:
        await query.answer()
    except Exception:
        pass

    # ABOUT
    if data == "about":
        await query.message.reply_photo(
            photo=ABOUT_IMAGE,
            caption=ABOUT_TEXT,
            reply_markup=about_buttons()
        )

    # HELP
    elif data == "help":
        await query.message.reply_photo(
            photo=ABOUT_IMAGE,
            caption=HELP_TEXT,
            reply_markup=home_button()
        )

    # HOME
    elif data == "start_home":
        try:
            await query.message.edit_caption(
                caption=START_TEXT,
                reply_markup=start_buttons()
            )
        except Exception:
            try:
                await query.message.reply_photo(
                    photo=START_IMAGE,
                    caption=START_TEXT,
                    reply_markup=start_buttons()
                )
            except Exception:
                pass

    # SETTINGS
    elif data == "settings_panel":
        try:
            from utils.user_settings import get_user_settings
            from database import posts

            user_id = query.from_user.id
            user = await client.get_users(user_id)
            first_name = user.first_name or "User"

            post_count = posts.count_documents(
                {"user_id": user_id}
            )

            user_data = get_user_settings(
                user_id,
                telegram_first_name=first_name
            )

            account_name = user_data.get(
                "account_name", first_name
            )

            author_name = user_data.get(
                "author_name", first_name
            )

            text = f"""
<b>⚙️ ACCOUNT SETTINGS</b>

<b>User ID :</b> <code>{user_id}</code>
<b>Domain :</b> Telegraph
<b>Account Name :</b> {account_name}
<b>Author Name :</b> {author_name}
<b>No. of Posts :</b> {post_count}
"""

            buttons = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "USER ID",
                        callback_data="noop"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "DOMAIN : Telegraph",
                        callback_data="noop"
                    )
                ],
                [
                    InlineKeyboardButton(
                        f"ACCOUNT : {account_name}",
                        callback_data="noop"
                    )
                ],
                [
                    InlineKeyboardButton(
                        f"AUTHOR : {author_name}",
                        callback_data="noop"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "PROFILE LINK",
                        url=(
                            "https://t.me/"
                            + author_name.lstrip("@")
                        )
                    )
                ],
                [
                    InlineKeyboardButton(
                        f"NO. OF POSTS : {post_count}",
                        callback_data="noop"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔄 Reset All",
                        callback_data="reset_settings"
                    ),
                    InlineKeyboardButton(
                        "🔙 Home",
                        callback_data="start_home"
                    )
                ]
            ])

            await query.message.reply_text(
                text,
                reply_markup=buttons
            )

        except Exception as error:
            await query.message.reply_text(
                f"⚠️ Unable to load settings.\n"
                f"<code>{str(error)[:300]}</code>",
                reply_markup=home_button()
            )

    # REFRESH STATS
    elif data == "refresh_stats":
        try:
            users = total_users()
            posts = total_posts()

            text = f"""
<b>📊 BOT STATISTICS</b>

👥 <b>Total Users :</b> {users}
📝 <b>Total Posts :</b> {posts}
<b>Powered By :</b> @Aero_Unity
"""

            await query.message.reply_text(
                text,
                reply_markup=stats_buttons()
            )

        except Exception:
            await query.message.reply_text(
                "⚠️ Database error. Please try again later.",
                reply_markup=stats_buttons()
            )

    # RESET SETTINGS
    elif data == "reset_settings":
        try:
            from utils.user_settings import reset_user_settings

            reset_user_settings(query.from_user.id)

            await query.message.reply_text(
                "✅ <b>Settings reset completed.</b>",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton(
                            "• Settings •",
                            callback_data="settings_panel"
                        ),
                        InlineKeyboardButton(
                            "• Home •",
                            callback_data="start_home"
                        )
                    ]
                ])
            )

        except ImportError:
            await query.message.reply_text(
                "⚠️ reset_user_settings is missing "
                "from utils/user_settings.py",
                reply_markup=home_button()
            )

        except Exception:
            await query.message.reply_text(
                "⚠️ Unable to reset settings.",
                reply_markup=home_button()
            )

    # NOOP
    elif data == "noop":
        return

# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #