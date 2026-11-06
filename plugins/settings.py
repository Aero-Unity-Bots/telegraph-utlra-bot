# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

import html
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import posts
from utils.user_settings import get_user_settings

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def settings_buttons():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "• Uᴘᴅᴀᴛᴇs •",
                    url="https://t.me/Aero_Unity"
                ),
                InlineKeyboardButton(
                    "• Dᴇᴠᴇʟᴏᴘᴇʀ •",
                    url="https://t.me/Mr_Mohammed_29"
                )
            ],
            [
                InlineKeyboardButton(
                    "• Cʟᴏsᴇ •",
                    callback_data="close_settings"
                )
            ]
        ]
    )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_message(filters.command("settings"))
async def settings(client, message):

    if not message.from_user:
        return

    user = message.from_user
    user_id = user.id
    first_name = user.first_name or "User"
    username = user.username

    if username:
        username_text = (
            f'<a href="https://t.me/{html.escape(username)}">'
            f'@{html.escape(username)}</a>'
        )
    else:
        username_text = (
            f'<a href="tg://user?id={user_id}">'
            f'{html.escape(first_name)}</a>'
        )

    try:
    
        post_count = posts.count_documents(
            {"user_id": user_id}
        )

        user_data = get_user_settings(
            user_id,
            telegram_first_name=first_name
        )

        account_name = html.escape(
            str(user_data.get("account_name") or first_name)
        )

        author_name = html.escape(
            str(user_data.get("author_name") or "Unknown")
        )

        profile_photo = None
        dc_id = "Unknown"

        if user.photo:
            dc_id = getattr(
                user.photo,
                "dc_id",
                "Unknown"
            )

            try:
                profile_photo = await client.download_media(
                    user.photo.big_file_id,
                    in_memory=True
                )

            except Exception as error:
                print(
                    f"[Profile Photo Download Error] {error}"
                )

        text = f"""
<b>⚙️ Sᴇᴛᴛɪɴɢs </b>

🔎 <b>Nᴀᴍᴇ :</b> {account_name}
👤 <b>Usᴇʀɴᴀᴍᴇ :</b> {username_text}
🆔 <b>ID :</b> <code>{user_id}</code>
🌐 <b>Dᴀᴛᴀ Cᴇɴᴛᴇʀ ID :</b> <code>{dc_id}</code>
📝 <b>Tᴏᴛᴀʟ Pᴏsᴛs :</b> <code>{post_count}</code>
🔗 <b>Dᴏᴍᴀɪɴ :</b> Tᴇʟᴇɢʀᴀᴘʜ
"""
        buttons = settings_buttons()

        # Send profile photo if available
        if profile_photo:

            await message.reply_photo(
                photo=profile_photo,
                caption=text,
                reply_markup=buttons
            )

        else:

            await message.reply_text(
                text,
                reply_markup=buttons,
                disable_web_page_preview=True
            )

    except Exception as error:

        print(
            f"[Settings Error] "
            f"{type(error).__name__}: {error}"
        )

        await message.reply_text(
            "⚠️ <b>Unable to load account settings.</b>\n"
            "Please try again later."
        )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_callback_query(
    filters.regex("^close_settings$")
)
async def close_settings(_, query):

    if not query.from_user:
        return
        
    if (
        query.message.reply_to_message
        and query.message.reply_to_message.from_user
        and query.from_user.id != query.message.reply_to_message.from_user.id
    ):
        return await query.answer(
            "This settings message belongs to another user.",
            show_alert=True
        )

    await query.message.delete()
    await query.answer("Settings closed!")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #