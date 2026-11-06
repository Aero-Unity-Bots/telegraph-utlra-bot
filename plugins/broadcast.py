
# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity
# Support : @Coders_Grp
# ------------------------ #

import asyncio
import config

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity
# Support : @Coders_Grp
# ------------------------ #

from pyrogram import Client, filters
from pyrogram.errors import (
    FloodWait,
    UserIsBlocked,
    InputUserDeactivated,
    PeerIdInvalid,
    RPCError
)

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
    return str(text).translate(str.maketrans(normal, small))

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity
# Support : @Coders_Grp
# ------------------------ #

@Client.on_message(filters.command("broadcast"))
async def broadcast(client, message):

    if not message.from_user:
        return

    if message.from_user.id != int(config.OWNER_ID):
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

    try:
        user_list = list(
            users.find(
                {"user_id": {"$exists": True}},
                {"user_id": 1, "_id": 0}
            )
        )
    except Exception as e:
        print(f"[Broadcast Database Error] {e}", flush=True)
        return await message.reply_text(
            "❌ Database error while loading users."
        )

    total = len(user_list)

    if total == 0:
        return await message.reply_text(
            "❌ No registered users found."
        )

    status = await message.reply_text(
        small_caps("📢 Broadcast started...")
    )

    sent = 0
    failed = 0
    blocked = 0
    invalid = 0
    errors = []

    for index, user in enumerate(user_list, start=1):

        user_id = user.get("user_id")

        if not user_id:
            failed += 1
            continue

        try:
            while True:
                try:

                    await client.copy_message(
                        chat_id=int(user_id),
                        from_chat_id=source.chat.id,
                        message_id=source.id,
                        reply_markup=source.reply_markup
                    )

                    sent += 1
                    break

                except FloodWait as e:
                    print(
                        f"[Broadcast] FloodWait: sleeping {e.value}s",
                        flush=True
                    )
                    await asyncio.sleep(e.value + 1)

            await asyncio.sleep(0.15)

        except (UserIsBlocked, InputUserDeactivated):
            failed += 1
            blocked += 1

        except PeerIdInvalid as e:
            failed += 1
            invalid += 1
            print(
                f"[Broadcast Peer Error] {user_id}: {e}",
                flush=True
            )

        except RPCError as e:
            failed += 1

            error_text = str(e)
            errors.append(error_text)

            print(
                f"[Broadcast Telegram Error] {user_id}: {error_text}",
                flush=True
            )

        except Exception as e:
            failed += 1

            error_text = str(e)
            errors.append(error_text)

            print(
                f"[Broadcast Error] {user_id}: {error_text}",
                flush=True
            )

        if index % 10 == 0 or index == total:
            try:
                await status.edit_text(
                    f"""
{small_caps("📢 Broadcasting in progress")}

{small_caps("👥 Total users")}: <b>{total}</b>
{small_caps("✅ Successfully sent")}: <b>{sent}</b>
{small_caps("❌ Failed")}: <b>{failed}</b>
{small_caps("🚫 Blocked")}: <b>{blocked}</b>
{small_caps("⚠️ Invalid peer")}: <b>{invalid}</b>

{small_caps("⏳ Progress")}: <b>{index}/{total}</b>
"""
                )
            except Exception:
                pass

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity
# Support : @Coders_Grp
# ------------------------ #

    report = f"""
{small_caps("📢 Broadcast completed")}

{small_caps("👥 Total users")}: <b>{total}</b>
{small_caps("✅ Successfully sent")}: <b>{sent}</b>
{small_caps("❌ Failed")}: <b>{failed}</b>
{small_caps("🚫 Blocked")}: <b>{blocked}</b>
{small_caps("⚠️ Invalid peer")}: <b>{invalid}</b>
"""

    if errors:
        report += (
            f"\n{small_caps('⚠️ Other errors')}: "
            f"<b>{len(errors)}</b>"
        )

    try:
        await status.edit_text(report)
    except Exception as e:
        print(f"[Broadcast Report Error] {e}", flush=True)

    print(
        f"[Broadcast Completed] Total={total}, "
        f"Sent={sent}, Failed={failed}, "
        f"Blocked={blocked}, Invalid={invalid}",
        flush=True
    )


# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity
# Support : @Coders_Grp
# ------------------------ #