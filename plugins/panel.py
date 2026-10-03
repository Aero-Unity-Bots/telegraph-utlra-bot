# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

import config


# ------------------------- #
# PANEL BUTTONS
# ------------------------- #

def panel_buttons():

    return InlineKeyboardMarkup(
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
                    "• Settings •",
                    callback_data="settings_panel"
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


# ------------------------- #
# PANEL COMMAND
# ------------------------- #

@Client.on_message(filters.command("panel"))
async def panel(_, message):

    if not message.from_user:
        return

    if message.from_user.id != config.OWNER_ID:

        return await message.reply_text(
            "❌ <b>You are not allowed to use this command.</b>"
        )

    text = """
<b>🧠 ADMIN CONTROL PANEL</b>

Manage your bot from here:

📊 <b>Stats</b>
→ View total users and posts.

📢 <b>Broadcast</b>
→ Send a message to bot users.

⚙️ <b>Settings</b>
→ View account/settings information.
"""

    await message.reply_text(
        text,
        reply_markup=panel_buttons()
    )


# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #