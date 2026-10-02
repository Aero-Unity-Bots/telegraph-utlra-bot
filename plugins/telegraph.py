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
    "AnimeBot"
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
# TELEGRAPH INIT
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
# HELPERS
# ============================================================

def escape_html(text: str) -> str:
    """Escape text safely for Telegraph HTML."""
    return html.escape(str(text), quote=True)


def clean_filename(filename: str) -> str:
    """Clean filename for Telegraph title."""
    if not filename:
        return "MediaInfo"

    filename = os.path.basename(filename).strip()

    # Telegraph title must be reasonably sized.
    if len(filename) > 250:
        filename = filename[:247] + "..."

    return filename


def get_media_filename(message):
    """Get the original filename from a Telegram message."""

    if message.document:
        return message.document.file_name or "MediaInfo"

    if message.video:
        return message.video.file_name or "Video"

    if message.audio:
        return message.audio.file_name or "Audio"

    if message.animation:
        return message.animation.file_name or "Animation"

    return "MediaInfo"


def get_audio_languages(media_info: str):
    """
    Extract unique Language values from Audio sections.
    Example:
        Language : Japanese
        Language : English
    """

    languages = []

    current_section = None

    for line in media_info.splitlines():

        stripped = line.strip()

        # Detect MediaInfo section.
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

            if language and language not in languages:
                languages.append(language)

    return languages


def split_mediainfo_sections(media_info: str):
    """
    Split MediaInfo text into sections.

    Example:
        General
        ...
        Video
        ...
        Audio
        ...

    Returns:
        [
            ("General", "..."),
            ("Video", "..."),
            ("Audio", "...")
        ]
    """

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

        # MediaInfo section headers normally have no ":".
        if (
            stripped in known_sections
            and not line.startswith(" ")
            and ":" not in stripped
        ):
            if current_name is not None:
                sections.append(
                    (
                        current_name,
                        "\n".join(current_lines).strip()
                    )
                )

            current_name = stripped
            current_lines = []
            continue

        if current_name is not None:
            current_lines.append(line)

    if current_name is not None:
        sections.append(
            (
                current_name,
                "\n".join(current_lines).strip()
            )
        )

    return [
        (name, content)
        for name, content in sections
        if content
    ]


def section_icon(section_name: str) -> str:
    """Return an emoji for each MediaInfo section."""

    icons = {
        "General": "📁",
        "Video": "🎞️",
        "Audio": "🔊",
        "Text": "💬",
        "Image": "🖼️",
        "Menu": "📋",
        "Other": "📦",
    }

    return icons.get(section_name, "📄")


def run_mediainfo(file_path: str) -> str:
    """
    Run the MediaInfo CLI.

    MediaInfo is installed by the Dockerfile.
    """

    try:
        process = awaitable_subprocess(file_path)

        if process.returncode != 0:
            error = (
                process.stderr.strip()
                if process.stderr
                else "Unknown MediaInfo error."
            )

            raise RuntimeError(error)

        output = process.stdout.strip()

        if not output:
            raise RuntimeError(
                "MediaInfo returned empty output."
            )

        return output

    except FileNotFoundError:
        raise RuntimeError(
            "MediaInfo is not installed. "
            "Make sure the Dockerfile installs the "
            "`mediainfo` package."
        )


def awaitable_subprocess(file_path: str):
    """
    Synchronous subprocess wrapper.

    Keeping this separate makes error handling cleaner.
    """

    return subprocess.run(
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


def build_mediainfo_html(filename: str, media_info: str):
    """
    Build the Telegraph page.

    Layout:

    [filename]

    AnimeBot
    October 02, 2026

    🔊 AUDIOS
    Japanese

    📁 General
    <pre>...</pre>

    🎞️ Video
    <pre>...</pre>

    🔊 Audio
    <pre>...</pre>

    Report content on this page
    """

    safe_filename = escape_html(filename)

    today = datetime.now().strftime("%B %d, %Y")

    languages = get_audio_languages(media_info)

    sections = split_mediainfo_sections(media_info)

    content = []

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    content.append(
        f"<h3>{safe_filename}</h3>"
    )

    content.append(
        f"<p><b>{escape_html(TELEGRAPH_AUTHOR_NAME)}</b><br>"
        f"{escape_html(today)}</p>"
    )

    # --------------------------------------------------------
    # AUDIO SUMMARY
    # --------------------------------------------------------

    if languages:
        content.append("<p><b>🔊 𝗔𝗨𝗗𝗜𝗢𝗦</b></p>")

        for language in languages:
            content.append(
                f"<p>{escape_html(language)}</p>"
            )

    # --------------------------------------------------------
    # MEDIAINFO SECTIONS
    # --------------------------------------------------------

    for section_name, section_content in sections:

        icon = section_icon(section_name)

        content.append(
            f"<p><b>{icon} {escape_html(section_name)}</b></p>"
        )

        # Keep MediaInfo alignment exactly as much as possible.
        content.append(
            "<pre>"
            + escape_html(section_content)
            + "</pre>"
        )

    # --------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------

    content.append("<hr>")

    content.append(
        "<p><b>Report content on this page</b></p>"
    )

    content.append(
        f'<p><b>ᴄʜᴀɴɴᴇʟ :</b> '
        f'<a href="{escape_html(TELEGRAPH_AUTHOR_URL)}">'
        f'{escape_html(TELEGRAPH_CHANNEL)}</a></p>'
    )

    content.append(
        f'<p><b>ᴅᴇᴠᴇʟᴏᴘᴇʀ :</b> '
        f'<a href="{escape_html(TELEGRAPH_DEVELOPER_URL)}">'
        f'{escape_html(TELEGRAPH_DEVELOPER)}</a></p>'
    )

    return "\n".join(content)


def trim_telegraph_content(content: str):
    """
    Telegraph has a 64 KB content limit.

    Keep a little safety margin for JSON/API overhead.
    """

    if len(content.encode("utf-8")) <= MAX_TELEGRAPH_CONTENT:
        return content

    # Keep UTF-8 safe.
    encoded = content.encode("utf-8")[:MAX_TELEGRAPH_CONTENT]

    trimmed = encoded.decode(
        "utf-8",
        errors="ignore"
    )

    trimmed += (
        "\n<hr>"
        "<p><b>MediaInfo output was shortened "
        "because the Telegraph page reached its "
        "content limit.</b></p>"
    )

    return trimmed


def create_page(title: str, content: str):
    """Create Telegraph page."""

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

@Client.on_message(filters.command("tgm"))
async def telegraph(_, message):

    # --------------------------------------------------------
    # CASE 1: REPLIED MEDIA
    # --------------------------------------------------------

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
                "⏳ <b>Downloading media...</b>"
            )

            temp_dir = tempfile.mkdtemp(
                prefix="telegraph_"
            )

            file_path = None

            try:

                filename = get_media_filename(reply)

                file_path = await reply.download(
                    file_name=os.path.join(
                        temp_dir,
                        filename
                    )
                )

                await status.edit_text(
                    "🔎 <b>Reading MediaInfo...</b>"
                )

                # Run MediaInfo outside the event loop.
                media_info = await asyncio.to_thread(
                    run_mediainfo,
                    file_path
                )

                await status.edit_text(
                    "📝 <b>Creating Telegraph page...</b>"
                )

                content = build_mediainfo_html(
                    filename,
                    media_info
                )

                content = trim_telegraph_content(
                    content
                )

                title = clean_filename(filename)

                url = await asyncio.to_thread(
                    create_page,
                    title,
                    content
                )

                # Save post using existing database function.
                try:
                    if message.from_user:
                        save_post(
                            message.from_user.id,
                            url,
                            title
                        )
                except Exception:
                    pass

                await status.edit_text(
                    "✅ <b>Telegraph Created</b>\n\n"
                    f"📄 <b>File:</b> "
                    f"<code>{escape_html(filename)}</code>\n\n"
                    f"🔗 <b>Link:</b> {url}",
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

            except subprocess.TimeoutExpired:

                await status.edit_text(
                    "❌ <b>MediaInfo timed out.</b>\n\n"
                    "The file took too long to analyze."
                )

            except Exception as e:

                error = str(e)

                if len(error) > 1000:
                    error = error[:1000] + "..."

                await status.edit_text(
                    "❌ <b>Failed to create Telegraph page.</b>\n\n"
                    f"<code>{escape_html(error)}</code>"
                )

            finally:

                # ------------------------------------------------
                # CLEAN TEMP FILE
                # ------------------------------------------------

                try:
                    if file_path and os.path.exists(file_path):
                        os.remove(file_path)
                except Exception:
                    pass

                try:
                    if os.path.isdir(temp_dir):
                        os.rmdir(temp_dir)
                except Exception:
                    pass

            return

    # --------------------------------------------------------
    # CASE 2: /tgm TITLE | TEXT
    # --------------------------------------------------------

    title = "Telegraph Post"
    text = None

    if "|" in (message.text or ""):

        try:

            title, text = message.text.split(
                "|",
                1
            )

            title = title.split(
                None,
                1
            )[1].strip()

            text = text.strip()

        except Exception:
            pass

    # --------------------------------------------------------
    # CASE 3: REPLY TO TEXT
    # --------------------------------------------------------

    elif message.reply_to_message:

        reply = message.reply_to_message

        text = (
            reply.text
            or reply.caption
        )

    # --------------------------------------------------------
    # CASE 4: DIRECT TEXT
    # --------------------------------------------------------

    elif len(message.command) > 1:

        text = message.text.split(
            None,
            1
        )[1]

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not text:

        return await message.reply_text(
            "❌ <b>Send some text or reply to a "
            "text/media message.</b>\n\n"
            "For MediaInfo:\n"
            "1. Send a video/document\n"
            "2. Reply to it with <code>/tgm</code>"
        )

    # --------------------------------------------------------
    # NORMAL TEXT TELEGRAPH
    # --------------------------------------------------------

    safe_text = escape_html(text)

    content = (
        f"<p>{safe_text.replace(chr(10), '<br>')}</p>"
    )

    content += """
<hr>
<p><b>ᴄʜᴀɴɴᴇʟ :</b>
<a href="https://t.me/Aero_Unity">ᴀᴇʀᴏ ᴜɴɪᴛʏ</a></p>

<p><b>ᴅᴇᴠᴇʟᴏᴘᴇʀ :</b>
<a href="https://t.me/Mr_Mohammed_29">ᴍᴏʜᴀᴍᴍᴇᴅ</a></p>
"""

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
            f"✅ <b>Telegraph Created</b>\n\n"
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
            "❌ <b>Failed to create Telegraph page.</b>\n\n"
            f"<code>{escape_html(str(e))}</code>"
        )


# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #