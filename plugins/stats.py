# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import total_users, total_posts
import config


# ------------------------- #
# BUTTONS
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
# STATS COMMAND
# ------------------------- #

@Client.on_message(filters.command("stats"))
async def stats(_, message):

    if not message.from_user:
        return

    if message.from_user.id != config.OWNER_ID:

        return await message.reply_text(
            "❌ <b>You cannot use this command.</b>"
        )

    try:

        users = total_users()
        posts = total_posts()

    except Exception:

        return await message.reply_text(
            "⚠️ <b>Database error.</b>\n"
            "Try again later."
        )

    text = f"""
<b>📊 BOT STATISTICS</b>

👥 <b>Total Users :</b> {users}
📝 <b>Total Posts :</b> {posts}

›› Powered By : @Aero_Unity
"""

    await message.reply_text(
        text,
        reply_markup=stats_buttons()
    )


# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #