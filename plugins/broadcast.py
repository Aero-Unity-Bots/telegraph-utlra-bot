# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

import asyncio
import html
import config

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from database import users

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def small_caps(text):
    normal = "abcdefghijklmnopqrstuvwxyz"
    small = "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢ"
    return text.translate(str.maketrans(normal, small))

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def make_bold(text):
    return f"<b>{html.escape(text)}</b>"

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_message(filters.command("broadcast"))
async def broadcast(client, message):

    if not message.from_user or message.from_user.id != config.OWNER_ID:
        return await message.reply_text(
            small_caps("❌ You are not my senpai.")
        )

    if not message.reply_to_message:
        return await message.reply_text(
            small_caps("❌ Reply to a message to broadcast.")
        )

    source = message.reply_to_message

    if not source.text and not source.media:
        return await message.reply_text(
            small_caps("❌ Unsupported message type.")
        )

    status = await message.reply_text(
        small_caps("Broadcasting started...")
    )

    sent = 0
    failed = 0
    user_list = list(
        users.find({}, {"user_id": 1, "_id": 0})
    )

    total = len(user_list)

    for user in user_list:

        user_id = user.get("user_id")

        if not user_id:
            failed += 1
            continue

        try:
            while True:
                try:

                    if source.text is not None:

                        await client.send_message(
                            chat_id=user_id,
                            text=make_bold(source.text),
                            parse_mode="html",
                            reply_markup=source.reply_markup
                        )

                    else:

                        caption = None

                        if source.caption:
                            caption = make_bold(source.caption)

                        await client.copy_message(
                            chat_id=user_id,
                            from_chat_id=source.chat.id,
                            message_id=source.id,
                            caption=caption,
                            parse_mode="html",
                            reply_markup=source.reply_markup
                        )

                    sent += 1
                    break

                except FloodWait as e:
                    await asyncio.sleep(e.value + 1)


            await asyncio.sleep(0.05)

        except (UserIsBlocked, InputUserDeactivated):
            failed += 1

        except Exception as e:
            failed += 1
            print(f"[Broadcast Error] {user_id}: {e}")

        processed = sent + failed

        if processed % 100 == 0:
            try:
                await status.edit_text(
                    f"""
{small_caps("📢 Broadcasting in progress")}

{small_caps("👥 Total users")}: <b>{total}</b>
{small_caps("✅ Sent")}: <b>{sent}</b>
{small_caps("❌ Failed")}: <b>{failed}</b>
"""
                )
            except Exception:
                pass

    await status.edit_text(
        f"""
{small_caps("📢 Broadcast completed")}

{small_caps("👥 Total users")}: <b>{total}</b>
{small_caps("✅ Successfully sent")}: <b>{sent}</b>
{small_caps("❌ Failed")}: <b>{failed}</b>
"""
    )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #