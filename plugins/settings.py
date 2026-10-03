# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import posts
from utils.user_settings import get_user_settings


# ------------------------- #
# SETTINGS BUTTONS
# ------------------------- #

def settings_buttons(
    user_id,
    post_count,
    account_name,
    author_name
):

    username = str(author_name).lstrip("@")

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"USER ID : {user_id}",
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
                    "DEFAULT PAGE : @AU_Telegraph_Post_Bot",
                    callback_data="noop"
                )
            ],
            [
                InlineKeyboardButton(
                    f"ACCOUNT NAME : {account_name}",
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
                    url=f"https://t.me/{username}"
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
                    "🔙 Go Back",
                    callback_data="start_home"
                )
            ]
        ]
    )


# ------------------------- #
# SETTINGS COMMAND
# ------------------------- #

@Client.on_message(filters.command("settings"))
async def settings(_, message):

    user_id = message.from_user.id

    first_name = (
        message.from_user.first_name
        or "User"
    )

    try:

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

    except Exception:

        return await message.reply_text(
            "⚠️ <b>Unable to load settings.</b>\n"
            "Please try again later."
        )

    text = f"""
<b>⚙️ ACCOUNT SETTINGS</b>

<b>User ID :</b> <code>{user_id}</code>
<b>Domain :</b> Telegraph

<b>Account Name :</b> {account_name}
<b>Author Name :</b> {author_name}

<b>No. of Posts :</b> {post_count}
"""

    await message.reply_text(
        text,
        reply_markup=settings_buttons(
            user_id,
            post_count,
            account_name,
            author_name
        )
    )


# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #