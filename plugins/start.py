
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

START_GIF = (
    "https://media.giphy.com/media/"
    "3o7aD2saalBwwftBIY/giphy.gif"
)

START_TEXT = """
<b>Welcome To AU Ultra Telegraph Bot</b>

⚡ Create beautiful Telegraph pages
⚙️ Manage your account settings given below buttons
"""

ABOUT_TEXT = """
<b>🤖 ABOUT THIS BOT</b>

<b>Language :</b> Python 3
<b>Library :</b> Pyrogram
<b>Database :</b> MongoDB
<b>Domain :</b> Telegraph

<b>Channel :</b> @Aero_Unity
<b>Owner :</b> @Mr_Mohammed_29
"""

HELP_TEXT = """
<b>❓ HELP MENU</b>

<b>/tgm</b>
→ Create a Telegraph page.

<b>MediaInfo</b>
→ Reply to a video/document with <code>/tgm</code>
to create a detailed MediaInfo Telegraph page.
"""


# ------------------------- #
# START BUTTONS
# ------------------------- #

def start_buttons():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "• Updates •",
                    url="https://t.me/Aero_Unity"
                )
            ],
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
                    "• Settings •",
                    callback_data="settings_panel"
                )
            ],
            [
                InlineKeyboardButton(
                    "• Owner •",
                    url="https://t.me/Mr_Mohammed_29"
                )
            ],
        ]
    )


def back_button():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "• Home •",
                    callback_data="start_home"
                )
            ]
        ]
    )


# ------------------------- #
# SETTINGS BUTTONS
# ------------------------- #

def settings_back_button():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "• Home •",
                    callback_data="start_home"
                )
            ]
        ]
    )


# ------------------------- #
# STATS BUTTONS
# ------------------------- #

def stats_buttons():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 Refresh",
                    callback_data="refresh_stats"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔙 Home",
                    callback_data="start_home"
                )
            ]
        ]
    )


# ------------------------- #
# START COMMAND
# ------------------------- #

@Client.on_message(filters.command("start"))
async def start(client, message):

    try:
        add_user(message.from_user.id)
    except Exception:
        pass

    m = await message.reply_text(
        "🚀 Sʜᴀᴅᴏᴡ Oғ Mᴏɴᴀʀᴄʜ . . ."
    )

    await asyncio.sleep(0.5)

    await m.edit_text("🎊")
    await asyncio.sleep(0.5)

    await m.edit_text("⚡")
    await asyncio.sleep(0.5)

    await m.edit_text(
        "🤖 Wᴇʟᴄᴏᴍɪɴɢ Yᴏᴜ . . ."
    )

    await asyncio.sleep(0.7)

    await m.delete()

    await message.reply_animation(
        animation=START_GIF,
        caption=START_TEXT,
        reply_markup=start_buttons()
    )


# ------------------------- #
# CALLBACK HANDLER
# ------------------------- #

@Client.on_callback_query()
async def callback_handler(
    client: Client,
    query: CallbackQuery
):

    data = query.data

    # Always answer the callback first where possible.
    try:
        await query.answer()
    except Exception:
        pass

    # -------------------------
    # ABOUT
    # -------------------------

    if data == "about":

        await query.message.edit_caption(
            caption=ABOUT_TEXT,
            reply_markup=back_button()
        )

    # -------------------------
    # HELP
    # -------------------------

    elif data == "help":

        await query.message.edit_caption(
            caption=HELP_TEXT,
            reply_markup=back_button()
        )

    # -------------------------
    # HOME
    # -------------------------

    elif data == "start_home":

        try:

            await query.message.edit_caption(
                caption=START_TEXT,
                reply_markup=start_buttons()
            )

        except Exception:

            await query.message.edit_text(
                START_TEXT,
                reply_markup=start_buttons()
            )

    # -------------------------
    # SETTINGS
    # -------------------------

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
                "account_name",
                first_name
            )

            author_name = user_data.get(
                "author_name",
                first_name
            )

            text = f"""
<b>⚙️ ACCOUNT SETTINGS</b>

<b>User ID :</b> <code>{user_id}</code>

<b>Domain :</b> Telegraph

<b>Account Name :</b> {account_name}
<b>Author Name :</b> {author_name}

<b>No. of Posts :</b> {post_count}
"""

            buttons = InlineKeyboardMarkup(
                [
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
                                f"https://t.me/"
                                f"{author_name.lstrip('@')}"
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
                    ],
                ]
            )

            try:

                await query.message.edit_caption(
                    caption=text,
                    reply_markup=buttons
                )

            except Exception:

                await query.message.edit_text(
                    text,
                    reply_markup=buttons
                )

        except Exception:

            await query.message.edit_text(
                "⚠️ Unable to load your settings.",
                reply_markup=settings_back_button()
            )

    # -------------------------
    # STATS
    # -------------------------

    elif data == "refresh_stats":

        try:

            users = total_users()
            posts = total_posts()

            text = f"""
<b>📊 BOT STATISTICS</b>

👥 <b>Total Users :</b> {users}
📝 <b>Total Posts :</b> {posts}

›› Powered By : @Aero_Unity
"""

            await query.message.edit_text(
                text,
                reply_markup=stats_buttons()
            )

        except Exception:

            await query.message.edit_text(
                "⚠️ <b>Database error.</b>\n"
                "Please try again later.",
                reply_markup=stats_buttons()
            )

    # -------------------------
    # ADMIN STATS PANEL
    # -------------------------

    elif data == "stats_panel":

        if query.from_user.id != getattr(
            __import__("config"),
            "OWNER_ID",
            0
        ):
            return

        try:

            users = total_users()
            posts = total_posts()

            text = f"""
<b>📊 BOT STATISTICS</b>

👥 <b>Total Users :</b> {users}
📝 <b>Total Posts :</b> {posts}

›› Powered By : @Aero_Unity
"""

            await query.message.edit_text(
                text,
                reply_markup=stats_buttons()
            )

        except Exception:

            await query.message.edit_text(
                "⚠️ Database error.",
                reply_markup=stats_buttons()
            )

    # -------------------------
    # BROADCAST PANEL
    # -------------------------

    elif data == "broadcast_panel":

        if query.from_user.id != getattr(
            __import__("config"),
            "OWNER_ID",
            0
        ):
            return

        await query.message.edit_text(
            "📢 <b>BROADCAST</b>\n\n"
            "Reply to the message you want to broadcast "
            "and use <code>/broadcast</code>.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔙 Back",
                            callback_data="admin_panel"
                        )
                    ]
                ]
            )
        )

    # -------------------------
    # ADMIN PANEL
    # -------------------------

    elif data == "admin_panel":

        if query.from_user.id != getattr(
            __import__("config"),
            "OWNER_ID",
            0
        ):
            return

        await query.message.edit_text(
            "🧠 <b>ADMIN CONTROL PANEL</b>\n\n"
            "Manage your bot from here:",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "• Stats •",
                            callback_data="stats_panel"
                        ),
                        InlineKeyboardButton(
                            "• Broadcast •",
                            callback_data="broadcast_panel"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "• Close •",
                            callback_data="close_panel"
                        )
                    ]
                ]
            )
        )

    # -------------------------
    # RESET SETTINGS
    # -------------------------

    elif data == "reset_settings":

        try:

            from utils.user_settings import reset_user_settings

            reset_user_settings(
                query.from_user.id
            )

            await query.message.edit_text(
                "✅ <b>Settings reset completed.</b>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "⚙️ Settings",
                                callback_data="settings_panel"
                            ),
                            InlineKeyboardButton(
                                "🔙 Home",
                                callback_data="start_home"
                            )
                        ]
                    ]
                )
            )

        except ImportError:

            await query.message.edit_text(
                "⚠️ Settings reset function is not "
                "available in your current user-settings module.",
                reply_markup=settings_back_button()
            )

        except Exception:

            await query.message.edit_text(
                "⚠️ Unable to reset settings.",
                reply_markup=settings_back_button()
            )

    # -------------------------
    # CLOSE
    # -------------------------

    elif data == "close_panel":

        try:
            await query.message.delete()
        except Exception:
            pass

    # -------------------------
    # NOOP
    # -------------------------

    elif data == "noop":

        return


# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #