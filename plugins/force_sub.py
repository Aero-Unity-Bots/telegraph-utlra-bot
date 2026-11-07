# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

import asyncio
import html
import logging
import config

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

from pyrogram import Client, filters, enums, StopPropagation
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.errors import UserNotParticipant
from database import users, add_user, force_sub_channels
from plugins.start import START_IMAGE, START_TEXT, start_buttons

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

LOGGER = logging.getLogger(__name__)
USERS_PER_PAGE = 10
FORCE_SUB_IMAGE = "https://telegra.ph/file/a75b699f1c0bf97686112-fb32d8e37cf37ea9c0.jpg"

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def is_owner(user_id):
    return user_id == int(config.OWNER_ID)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def small_caps(text):
    normal = "abcdefghijklmnopqrstuvwxyz"
    small = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ"
    return str(text).translate(str.maketrans(normal, small))

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_join_url(chat):
    if chat.get("invite_link"):
        return chat["invite_link"]

    if chat.get("username"):
        return f"https://t.me/{chat['username']}"

    return None

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def join_keyboard(channels):
    buttons = []

    for channel in channels:
        url = get_join_url(channel)

        if url:
            title = channel.get("title", "Join Chat")
            buttons.append([
                InlineKeyboardButton(
                    f"• Jᴏɪɴ {title[:30]}",
                    url=url
                )
            ])

    buttons.append([
        InlineKeyboardButton(
            "• Tʀʏ Aɢᴀɪɴ •",
            callback_data="check_fsub"
        )
    ])

    return InlineKeyboardMarkup(buttons)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def check_force_sub(client, user_id):

    if is_owner(user_id):
        return True

    channels = list(force_sub_channels.find())

    for channel in channels:
        try:
            member = await client.get_chat_member(
                channel["chat_id"],
                user_id
            )

            status = member.status

            if status in (
                enums.ChatMemberStatus.MEMBER,
                enums.ChatMemberStatus.ADMINISTRATOR,
                enums.ChatMemberStatus.OWNER
            ):
                continue

            if (
                status == enums.ChatMemberStatus.RESTRICTED
                and getattr(member, "is_member", False)
            ):
                continue

            return False

        except UserNotParticipant:
            return False

        except Exception as e:
            LOGGER.warning(
                "Force sub check failed for %s: %s",
                channel.get("chat_id"),
                e
            )
            return False

    return True

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def send_force_sub(client, message):

    channels = list(force_sub_channels.find())

    text = (
        "<b>⚠️ ᴊᴏɪɴ ʀᴇǫᴜɪʀᴇᴅ ᴄʜᴀɴɴᴇʟs</b>\n\n"
        "ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴀʟʟ ᴛʜᴇ ᴄʜᴀɴɴᴇʟs "
        "ᴀɴᴅ ɢʀᴏᴜᴘs ʙᴇʟᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ "
        "ᴀғᴛᴇʀ ᴊᴏɪɴɪɴɢ, ᴄʟɪᴄᴋ ᴛʀʏ ᴀɢᴀɪɴ."
    )

    await message.reply_text(
        text,
        reply_markup=join_keyboard(channels),
        disable_web_page_preview=True
    )
    
# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_message(
    filters.private & filters.incoming,
    group=-1
)
async def force_sub_middleware(client, message):

    if not message.from_user:
        return

    if is_owner(message.from_user.id):
        return

    if not force_sub_channels.count_documents({}):
        return

    if await check_force_sub(client, message.from_user.id):
        return

    await send_force_sub(client, message)

    raise StopPropagation
    
# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #


@Client.on_callback_query(
    filters.regex("^check_fsub$")
)
async def check_fsub_callback(client, query):

    user_id = query.from_user.id

    if not await check_force_sub(client, user_id):
        return await query.answer(
            "Join all required channels and groups first.",
            show_alert=True
        )

    await query.answer("✅ Subscription verified!")

    try:
        add_user(user_id)
    except Exception as error:
        LOGGER.warning("Add user error: %s", error)

    try:
        await query.message.delete()
    except Exception:
        pass
        
    try:
        await client.send_photo(
            chat_id=user_id,
            photo=START_IMAGE,
            caption=START_TEXT,
            reply_markup=start_buttons()
        )

    except Exception as error:
        LOGGER.warning("Welcome photo error: %s", error)

        await client.send_message(
            chat_id=user_id,
            text=START_TEXT,
            reply_markup=start_buttons()
        )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_message(
    filters.command("addfsub") & filters.private
)
async def add_fsub(client, message):

    if not message.from_user or not is_owner(message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "<b>ᴜsᴀɢᴇ:</b>\n\n"
            "<code>/addfsub @channel</code>\n"
            "<code>/addfsub -1001234567890</code>\n"
            "<code>/addfsub -1001234567890 https://t.me/+invite</code>"
        )

    target = message.command[1]
    invite_link = (
        message.command[2]
        if len(message.command) >= 3
        else None
    )

    status = await message.reply_text(
        "<b>Aᴅᴅɪɴɢ Fᴏʀᴄᴇ Sᴜʙsᴄʀɪᴘᴛɪᴏɴ, ᴡᴀɪᴛ ᴀ sᴇᴄ...</b>"
    )

    try:
        chat = await client.get_chat(target)
        bot = await client.get_me()
        bot_member = await client.get_chat_member(
            chat.id,
            bot.id
        )

        if bot_member.status not in (
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER
        ):
            return await status.edit_text(
                "<b>‼️ Mᴀᴋᴇ ᴛʜᴇ ʙᴏᴛ ᴀɴ ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ/ɢʀᴏᴜᴘ ғɪʀsᴛ .</b>"
            )

        if not invite_link and not chat.username:
            try:
                link = await client.create_chat_invite_link(
                    chat_id=chat.id,
                    name="Force Subscription"
                )
                invite_link = link.invite_link

            except Exception as e:
                LOGGER.warning("Invite link creation failed: %s", e)

                return await status.edit_text(
                    "<b> Could not create an invite link.\n"
                    "Provide a valid invite link with the command</b>"
                )

        force_sub_channels.update_one(
            {"chat_id": chat.id},
            {
                "$set": {
                    "chat_id": chat.id,
                    "title": chat.title or chat.first_name or str(chat.id),
                    "username": chat.username,
                    "invite_link": invite_link
                }
            },
            upsert=True
        )

        await status.edit_text(
            f"""
<b>✅ Fᴏʀᴄᴇ Sᴜʙsᴄʀɪᴘᴛɪᴏɴ Aᴅᴅᴇᴅ</b>

<b>Cʜᴀᴛ :</b> {html.escape(chat.title or str(chat.id))}
<b>Cʜᴀᴛ ID :</b> <code>{chat.id}</code>
<b>Tʏᴘᴇ :</b> {html.escape(str(chat.type.value))}
"""
        )

    except Exception as e:
        LOGGER.exception("Add force sub error")

        await status.edit_text(
            "❌ Failed to add channel/group.\n\n"
            f"<code>{html.escape(str(e))[:1000]}</code>"
        )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_message(
    filters.command("delfsub") & filters.private
)
async def del_fsub(client, message):

    if not message.from_user or not is_owner(message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "<b>ᴜsᴀɢᴇ:</b>\n\n"
            "<code>/delfsub @channel</code>\n"
            "<code>/delfsub -1001234567890</code>"
        )

    target = message.command[1]

    try:
        try:
            chat = await client.get_chat(target)
            chat_id = chat.id
        except Exception:
            chat_id = int(target)

        result = force_sub_channels.delete_one(
            {"chat_id": chat_id}
        )

        if result.deleted_count:
            await message.reply_text(
                "✅ <b>Fᴏʀᴄᴇ Sᴜʙsᴄʀɪᴘᴛɪᴏɴ Rᴇᴍᴏᴠᴇᴅ</b>\n\n"
                f"🆔 Cʜᴀɴɴᴇʟ ID : <code>{chat_id}</code>"
            )
        else:
            await message.reply_text(
                "<b>Tʜɪs ᴄʜᴀɴɴᴇʟ/ɢʀᴏᴜᴘ ɪs ɴᴏᴛ ɪɴ ᴛʜᴇ ғᴏʀᴄᴇ-sᴜʙ ʟɪsᴛ</b>."
            )

    except Exception as e:
        await message.reply_text(
            f"❌ Error: <code>{html.escape(str(e))}</code>"
        )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_message(
    filters.command("fsublist") & filters.private
)
async def fsub_list(client, message):

    if not message.from_user or not is_owner(message.from_user.id):
        return

    channels = list(force_sub_channels.find())

    if not channels:
        return await message.reply_text(
            "<b>Nᴏ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs ᴏʀ ɢʀᴏᴜᴘs ᴀᴅᴅᴇᴅ</b>  ."
        )

    text = "<b>Fᴏʀᴄᴇ Sᴜʙsᴄʀɪᴘᴛɪᴏɴ ʟɪsᴛ</b>\n\n"

    for index, channel in enumerate(channels, start=1):

        title = html.escape(channel.get("title", "Unknown"))
        chat_id = channel.get("chat_id")
        text += (
            f"<b>{index}. {title}</b>\n"
            f"<b> Cʜᴀɴɴᴇʟ ID</b> : <code>{chat_id}</code>\n\n"
        )

    text += f"<b>Tᴏᴛᴀʟ Cʜᴀɴɴᴇʟs :</b> {len(channels)}"

    await message.reply_text(
        text,
        disable_web_page_preview=True
    )
    
# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def status_keyboard(page, total_pages):

    buttons = []
    navigation = []

    if page > 0:
        navigation.append(
            InlineKeyboardButton(
                "• Pʀᴇᴠɪᴏᴜs •",
                callback_data=f"status_page_{page - 1}"
            )
        )

    if page + 1 < total_pages:
        navigation.append(
            InlineKeyboardButton(
                "• Nᴇxᴛ •",
                callback_data=f"status_page_{page + 1}"
            )
        )

    if navigation:
        buttons.append(navigation)

    buttons.append([
        InlineKeyboardButton(
            "• Cʟᴏsᴇ •",
            callback_data="close_fsub_status"
        )
    ])

    return InlineKeyboardMarkup(buttons)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def get_status_text(client, page):

    total_users = users.count_documents({})
    total_channels = force_sub_channels.count_documents({})

    total_pages = max(
        1,
        (total_users + USERS_PER_PAGE - 1) // USERS_PER_PAGE
    )

    page = max(0, min(page, total_pages - 1))

    user_list = list(
        users.find(
            {},
            {"user_id": 1, "_id": 0}
        )
        .sort("user_id", 1)
        .skip(page * USERS_PER_PAGE)
        .limit(USERS_PER_PAGE)
    )

    text = (
        "<b>📊 Bᴏᴛ sᴛᴀᴛᴜs</b>\n\n"
        f"👥 <b>Tᴏᴛᴀʟ Usᴇʀs :</b> <code>{total_users}</code>\n"
        f"📢 <b>Fᴏʀᴄᴇ Sᴜʙ Cʜᴀᴛs :</b> <code>{total_channels}</code>\n"
        "<b>👤 Rᴇɢɪsᴛᴇʀᴇᴅ Usᴇʀs</b>\n\n"
    )

    for index, data in enumerate(
        user_list,
        start=page * USERS_PER_PAGE + 1
    ):

        user_id = data.get("user_id")

        try:
            telegram_user = await client.get_users(user_id)

            name = html.escape(
                telegram_user.first_name or "Unknown"
            )

            username = (
                f"@{html.escape(telegram_user.username)}"
                if telegram_user.username
                else "No Username"
            )

        except Exception:
            name = "Unknown"
            username = "Unavailable"

        text += (
            f"<b>{index}. {name}</b>\n"
            f"<b>Usᴇʀɴᴀᴍᴇ :</b> {username}\n"
            f"<b>ID :</b> <code>{user_id}</code>\n\n"
        )

    text += f"<b>Pᴀɢᴇ :</b> {page + 1}/{total_pages}"

    return text, page, total_pages
    
# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_message(
    filters.command("status") & filters.private
)
async def bot_status(client, message):

    if not message.from_user or not is_owner(message.from_user.id):
        return

    text, page, total_pages = await get_status_text(
        client,
        0
    )

    keyboard = status_keyboard(page, total_pages)

    image = FORCE_SUB_IMAGE

    if image:
        try:
            return await message.reply_photo(
                photo=image,
                caption=text,
                reply_markup=keyboard
            )
        except Exception as e:
            LOGGER.warning("Status image failed: %s", e)

    await message.reply_text(
        text,
        reply_markup=keyboard
    )
    
# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_callback_query(
    filters.regex(r"^status_page_(\d+)$")
)
async def status_pagination(client, query):

    if not is_owner(query.from_user.id):
        return await query.answer(
            "‼️ Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ!",
            show_alert=True
        )

    page = int(query.data.split("_")[-1])

    text, page, total_pages = await get_status_text(
        client,
        page
    )

    keyboard = status_keyboard(page, total_pages)

    try:
        if query.message.photo:
            await query.message.edit_caption(
                caption=text,
                reply_markup=keyboard
            )
        else:
            await query.message.edit_text(
                text,
                reply_markup=keyboard
            )

        await query.answer()

    except Exception as e:
        await query.answer(
            str(e)[:150],
            show_alert=True
        )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_callback_query(
    filters.regex("^close_fsub_status$")
)
async def close_status(client, query):

    if not is_owner(query.from_user.id):
        return await query.answer(
            "‼️ Yᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ sᴇɴᴘᴀɪ!",
            show_alert=True
        )

    await query.answer()

    try:
        await query.message.delete()
    except Exception:
        pass

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #
