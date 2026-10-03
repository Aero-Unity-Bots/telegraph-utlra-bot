# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

import asyncio
import html
import os
import re
import subprocess
import tempfile
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegraph import Telegraph

from database import save_post


# ============================================================
# TELEGRAPH CONFIG
# ============================================================

TELEGRAPH_AUTHOR_NAME = os.getenv(
    "TELEGRAPH_AUTHOR_NAME",
    "Aero Unity"
)

TELEGRAPH_AUTHOR_URL = os.getenv(
    "TELEGRAPH_AUTHOR_URL",
    "https://t.me/Aero_Unity"
)

TELEGRAPH_CHANNEL = os.getenv(
    "TELEGRAPH_CHANNEL",
    "Aero Unity"
)

TELEGRAPH_DEVELOPER = os.getenv(
    "TELEGRAPH_DEVELOPER",
    "Mohammed"
)

TELEGRAPH_DEVELOPER_URL = os.getenv(
    "TELEGRAPH_DEVELOPER_URL",
    "https://t.me/Mr_Mohammed_29"
)

MAX_TELEGRAPH_CONTENT = 62000


# ============================================================
# TELEGRAPH ACCOUNT
# ============================================================

tg = Telegraph()

try:

    tg.create_account(
        short_name="ultra-bot",
        author_name=TELEGRAPH_AUTHOR_NAME,
        author_url=TELEGRAPH_AUTHOR_URL
    )

except Exception:
    pass


# ============================================================
# HTML
# ============================================================

def escape_html(text):

    return html.escape(
        str(text),
        quote=True
    )


# ============================================================
# FILE NAME
# ============================================================

def clean_filename(filename):

    if not filename:
        return "MediaInfo"

    filename = os.path.basename(
        filename
    ).strip()

    if len(filename) > 250:

        filename = (
            filename[:247]
            + "..."
        )

    return filename


def get_media_filename(message):

    if message.document:

        return (
            message.document.file_name
            or "MediaInfo"
        )

    if message.video:

        return (
            message.video.file_name
            or "Video"
        )

    if message.audio:

        return (
            message.audio.file_name
            or "Audio"
        )

    if message.animation:

        return (
            message.animation.file_name
            or "Animation"
        )

    return "MediaInfo"


# ============================================================
# MEDIAINFO
# ============================================================

def run_mediainfo(file_path):

    try:

        result = subprocess.run(
            [
                "mediainfo",
                "--Output=Text",
                file_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180
        )

    except FileNotFoundError:

        raise RuntimeError(
            "MediaInfo is not installed."
        )

    except subprocess.TimeoutExpired:

        raise RuntimeError(
            "MediaInfo analysis timed out."
        )

    if result.returncode != 0:

        error = (
            result.stderr.strip()
            or "Unknown MediaInfo error."
        )

        raise RuntimeError(error)

    output = result.stdout.strip()

    if not output:

        raise RuntimeError(
            "MediaInfo returned empty output."
        )

    return output


# ============================================================
# AUDIO LANGUAGES
# ============================================================

def get_audio_languages(media_info):

    languages = []

    current_section = None

    for line in media_info.splitlines():

        stripped = line.strip()

        if stripped in {
            "General",
            "Video",
            "Audio",
            "Text",
            "Menu",
            "Image",
            "Other"
        }:

            current_section = stripped

            continue

        if current_section != "Audio":
            continue

        match = re.match(
            r"^\s*Language\s*:\s*(.+?)\s*$",
            line,
            re.IGNORECASE
        )

        if match:

            language = match.group(1).strip()

            if (
                language
                and language not in languages
            ):

                languages.append(
                    language
                )

    return languages


# ============================================================
# MEDIAINFO SECTIONS
# ============================================================

def split_mediainfo_sections(media_info):

    known_sections = {
        "General",
        "Video",
        "Audio",
        "Text",
        "Image",
        "Menu",
        "Other"
    }

    sections = []

    current_name = None
    current_lines = []

    for raw_line in media_info.splitlines():

        line = raw_line.rstrip()
        stripped = line.strip()

        if (
            stripped in known_sections
            and not line.startswith(" ")
            and ":" not in stripped
        ):

            if current_name is not None:

                sections.append(
                    (
                        current_name,
                        "\n".join(
                            current_lines
                        ).strip()
                    )
                )

            current_name = stripped
            current_lines = []

            continue

        if current_name is not None:

            current_lines.append(
                line
            )

    if current_name is not None:

        sections.append(
            (
                current_name,
                "\n".join(
                    current_lines
                ).strip()
            )
        )

    return [
        (
            name,
            content
        )
        for name, content in sections
        if content
    ]


# ============================================================
# SECTION ICON
# ============================================================

def section_icon(section_name):

    icons = {

        "General": "📁",
        "Video": "🎞️",
        "Audio": "🔊",
        "Text": "💬",
        "Image": "🖼️",
        "Menu": "📋",
        "Other": "📦"

    }

    return icons.get(
        section_name,
        "📄"
    )


# ============================================================
# BUILD TELEGRAPH PAGE
# ============================================================

def build_mediainfo_html(
    filename,
    media_info
):

    safe_filename = escape_html(
        filename
    )

    today = datetime.now().strftime(
        "%B %d, %Y"
    )

    languages = get_audio_languages(
        media_info
    )

    sections = split_mediainfo_sections(
        media_info
    )

    content = []

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    content.append(
        f"<h3>{safe_filename}</h3>"
    )

    content.append(
        f"<p>"
        f"<b>{escape_html(TELEGRAPH_AUTHOR_NAME)}</b>"
        f"<br>"
        f"{escape_html(today)}"
        f"</p>"
    )

    # --------------------------------------------------------
    # AUDIO SUMMARY
    # --------------------------------------------------------

    if languages:

        content.append(
            "<p><b>🔊 𝗔𝗨𝗗𝗜𝗢𝗦</b></p>"
        )

        for language in languages:

            content.append(
                f"<p>"
                f"{escape_html(language)}"
                f"</p>"
            )

    # --------------------------------------------------------
    # FULL MEDIAINFO
    # --------------------------------------------------------

    for (
        section_name,
        section_content
    ) in sections:

        icon = section_icon(
            section_name
        )

        content.append(
            f"<p>"
            f"<b>{icon} "
            f"{escape_html(section_name)}"
            f"</b>"
            f"</p>"
        )

        content.append(
            "<pre>"
            + escape_html(
                section_content
            )
            + "</pre>"
        )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    content.append(
        "<hr>"
    )

    content.append(
        "<p>"
        "<b>Report content on this page</b>"
        "</p>"
    )

    content.append(
        f'<p>'
        f'<b>ᴄʜᴀɴɴᴇʟ :</b> '
        f'<a href="{escape_html(TELEGRAPH_AUTHOR_URL)}">'
        f'{escape_html(TELEGRAPH_CHANNEL)}'
        f'</a>'
        f'</p>'
    )

    content.append(
        f'<p>'
        f'<b>ᴅᴇᴠᴇʟᴏᴘᴇʀ :</b> '
        f'<a href="{escape_html(TELEGRAPH_DEVELOPER_URL)}">'
        f'{escape_html(TELEGRAPH_DEVELOPER)}'
        f'</a>'
        f'</p>'
    )

    return "\n".join(
        content
    )


# ============================================================
# TELEGRAPH SIZE LIMIT
# ============================================================

def trim_telegraph_content(content):

    if (
        len(
            content.encode("utf-8")
        )
        <= MAX_TELEGRAPH_CONTENT
    ):

        return content

    encoded = content.encode(
        "utf-8"
    )[:MAX_TELEGRAPH_CONTENT]

    trimmed = encoded.decode(
        "utf-8",
        errors="ignore"
    )

    trimmed += (
        "\n<hr>"
        "<p><b>"
        "MediaInfo output was shortened "
        "because the Telegraph page reached "
        "its content limit."
        "</b></p>"
    )

    return trimmed


# ============================================================
# CREATE TELEGRAPH PAGE
# ============================================================

def create_page(
    title,
    content
):

    response = tg.create_page(
        title=title,
        html_content=content,
        author_name=TELEGRAPH_AUTHOR_NAME,
        author_url=TELEGRAPH_AUTHOR_URL,
        return_content=False
    )

    return response["url"]


# ============================================================
# /TGM
# ============================================================

@Client.on_message(
    filters.command("tgm")
)
async def telegraph(
    _,
    message
):

    # ========================================================
    # REPLIED MEDIA
    # ========================================================

    if message.reply_to_message:

        reply = message.reply_to_message

        is_media = any(
            [
                reply.document,
                reply.video,
                reply.audio,
                reply.animation
            ]
        )

        if is_media:

            status = await message.reply_text(
                "⏳ <b>Downloading current file...</b>"
            )

            temp_dir = tempfile.mkdtemp(
                prefix="telegraph_"
            )

            file_path = None

            try:

                # ------------------------------------------------
                # GET THE EXACT FILE FROM THE REPLIED MESSAGE
                # ------------------------------------------------

                filename = get_media_filename(
                    reply
                )

                safe_download_name = (
                    os.path.basename(
                        filename
                    )
                )

                file_path = os.path.join(
                    temp_dir,
                    safe_download_name
                )

                await reply.download(
                    file_name=file_path
                )

                # ------------------------------------------------
                # VERIFY DOWNLOAD
                # ------------------------------------------------

                if not os.path.exists(
                    file_path
                ):

                    raise RuntimeError(
                        "Downloaded file was not found."
                    )

                file_size = os.path.getsize(
                    file_path
                )

                if file_size <= 0:

                    raise RuntimeError(
                        "Downloaded file is empty."
                    )

                await status.edit_text(
                    "🔎 <b>Reading metadata from "
                    "the current file...</b>"
                )

                # ------------------------------------------------
                # IMPORTANT:
                #
                # MediaInfo reads ONLY the downloaded file.
                # Nothing is changed or written to the file.
                # ------------------------------------------------

                media_info = await asyncio.to_thread(
                    run_mediainfo,
                    file_path
                )

                await status.edit_text(
                    "📝 <b>Creating Telegraph page...</b>"
                )

                # ------------------------------------------------
                # BUILD PAGE FROM CURRENT MEDIAINFO
                # ------------------------------------------------

                content = build_mediainfo_html(
                    filename,
                    media_info
                )

                content = trim_telegraph_content(
                    content
                )

                title = clean_filename(
                    filename
                )

                url = await asyncio.to_thread(
                    create_page,
                    title,
                    content
                )

                # ------------------------------------------------
                # SAVE POST
                # ------------------------------------------------

                try:

                    if message.from_user:

                        save_post(
                            message.from_user.id,
                            url,
                            title
                        )

                except Exception:
                    pass

                # ------------------------------------------------
                # SUCCESS
                # ------------------------------------------------

                await status.edit_text(
                    "✅ <b>Telegraph Created</b>\n\n"
                    f"📄 <b>File:</b>\n"
                    f"<code>"
                    f"{escape_html(filename)}"
                    f"</code>\n\n"
                    f"🔗 <b>Link:</b>\n"
                    f"{url}",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "• Open Telegraph •",
                                    url=url
                                )
                            ]
                        ]
                    )
                )

            except Exception as e:

                error = str(e)

                if len(error) > 1000:

                    error = (
                        error[:1000]
                        + "..."
                    )

                await status.edit_text(
                    "❌ <b>Failed to create "
                    "Telegraph page.</b>\n\n"
                    f"<code>"
                    f"{escape_html(error)}"
                    f"</code>"
                )

            finally:

                # ------------------------------------------------
                # DELETE TEMP FILE
                # ------------------------------------------------

                try:

                    if (
                        file_path
                        and os.path.exists(
                            file_path
                        )
                    ):

                        os.remove(
                            file_path
                        )

                except Exception:
                    pass

                try:

                    if os.path.isdir(
                        temp_dir
                    ):

                        os.rmdir(
                            temp_dir
                        )

                except Exception:
                    pass

            return

    # ========================================================
    # /TGM TITLE | TEXT
    # ========================================================

    title = "Telegraph Post"
    text = None

    if "|" in (
        message.text or ""
    ):

        try:

            title_part, text = (
                message.text.split(
                    "|",
                    1
                )
            )

            command_parts = (
                title_part.split(
                    None,
                    1
                )
            )

            if len(command_parts) > 1:

                title = command_parts[
                    1
                ].strip()

            text = text.strip()

        except Exception:
            pass

    # ========================================================
    # REPLY TO TEXT
    # ========================================================

    elif message.reply_to_message:

        reply = message.reply_to_message

        text = (
            reply.text
            or reply.caption
        )

    # ========================================================
    # DIRECT TEXT
    # ========================================================

    elif len(
        message.command
    ) > 1:

        text = message.text.split(
            None,
            1
        )[1]

    # ========================================================
    # NO TEXT
    # ========================================================

    if not text:

        return await message.reply_text(
            "❌ <b>Send some text or reply "
            "to a text/media message.</b>\n\n"
            "For MediaInfo:\n"
            "1. Send your file\n"
            "2. Reply to that exact file "
            "with <code>/tgm</code>"
        )

    # ========================================================
    # NORMAL TEXT PAGE
    # ========================================================

    safe_text = escape_html(
        text
    )

    content = (
        "<p>"
        + safe_text.replace(
            "\n",
            "<br>"
        )
        + "</p>"
    )

    content += (
        "<hr>"
        "<p>"
        "<b>ᴄʜᴀɴɴᴇʟ :</b> "
        '<a href="https://t.me/Aero_Unity">'
        "ᴀᴇʀᴏ ᴜɴɪᴛʏ"
        "</a>"
        "</p>"
        "<p>"
        "<b>ᴅᴇᴠᴇʟᴏᴘᴇʀ :</b> "
        '<a href="https://t.me/Mr_Mohammed_29">'
        "ᴍᴏʜᴀᴍᴍᴇᴅ"
        "</a>"
        "</p>"
    )

    content = trim_telegraph_content(
        content
    )

    try:

        url = await asyncio.to_thread(
            create_page,
            title,
            content
        )

        try:

            if message.from_user:

                save_post(
                    message.from_user.id,
                    url,
                    title
                )

        except Exception:
            pass

        await message.reply_text(
            "✅ <b>Telegraph Created</b>\n\n"
            f"{url}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "• Open •",
                            url=url
                        )
                    ]
                ]
            )
        )

    except Exception as e:

        await message.reply_text(
            "❌ <b>Failed to create "
            "Telegraph page.</b>\n\n"
            f"<code>"
            f"{escape_html(str(e))}"
            f"</code>"
        )


# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #