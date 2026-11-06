# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

import os
import time
import config

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import total_posts

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

BOT_START_TIME = time.time()
STATS_IMAGE = "https://telegra.ph/file/e16e87da766cc9d9f5206-85448a377887db6c7a.jpg"

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
        f"{days}d {hours}h {minutes}m {seconds}s"
    )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def stats_buttons():

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "• Rᴇғʀᴇsʜ •",
                    callback_data="refresh_stats"
                ),
                InlineKeyboardButton(
                    "• Cʟᴏsᴇ •",
                    callback_data="close_stats"
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

async def get_stats_text(client):

    start = time.perf_counter()
    bot = await client.get_me()
    ping = (time.perf_counter() - start) * 1000

    username = (
        f"@{bot.username}"
        if bot.username
        else "Not Available"
    )

    posts = total_posts()

    text = f"""
<b>📊 Bᴏᴛ Sᴛᴀᴛɪsᴛɪᴄs</b>

 <b>Usᴇʀɴᴀᴍᴇ :</b> {username}
 <b>ID :</b> <code>{bot.id}</code>
 <b>Tᴏᴛᴀʟ Pᴏsᴛs :</b> {posts}
 <b>Pɪɴɢ :</b> {ping:.2f} ms
 <b>Bᴏᴛ Uᴘᴛɪᴍᴇ :</b> {get_uptime()}

›› <b>Pᴏᴡᴇʀᴇᴅ Bʏ :</b> @Aero_Unity
"""
    return text

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_message(filters.command("stats"))
async def stats(client, message):

    if not message.from_user:
        return

    if message.from_user.id != config.OWNER_ID:
        return await message.reply_text(
            "<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ.</b>"
        )

    try:

        text = await get_stats_text(client)
        stats_image = STATS_IMAGE

        if stats_image:

            await message.reply_photo(
                photo=stats_image,
                caption=text,
                reply_markup=stats_buttons()
            )

        else:

            await message.reply_text(
                text,
                reply_markup=stats_buttons()
            )

    except Exception as error:

        await message.reply_text(
            f"⚠️ <b>Stats Error:</b>\n<code>{error}</code>"
        )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_callback_query(
    filters.regex("^refresh_stats$")
)
async def refresh_stats(client, query):

    if not query.from_user or query.from_user.id != config.OWNER_ID:
        return await query.answer(
            "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ",
            show_alert=True
        )

    try:

        text = await get_stats_text(client)

        await query.message.edit_caption(
            caption=text,
            reply_markup=stats_buttons()
        )

        await query.answer("Statistics refreshed!")

    except Exception as error:

        await query.answer(
            f"Refresh failed: {error}",
            show_alert=True
        )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_callback_query(
    filters.regex("^close_stats$")
)
async def close_stats(_, query):

    if not query.from_user or query.from_user.id != config.OWNER_ID:
        return await query.answer(
            "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ",
            show_alert=True
        )

    await query.message.delete()
    await query.answer("Wʜʏ ᴀʀᴇ ʏᴏᴜ ᴄᴜʀɪᴏᴜs!")

# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #