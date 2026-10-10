# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

import asyncio
import os
import tempfile
from pathlib import Path

from pyrogram import Client, filters
from pyrogram.types import Message

# ------------------------- #
# SETTINGS
# ------------------------- #

SAMPLE_DURATION = 10
MAX_UPLOAD_SIZE = 2 * 1024 * 1024 * 1024

async def run_ffmpeg(*args):
    """Run FFmpeg asynchronously and return its result."""
    process = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        *map(str, args),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        error = stderr.decode(errors="replace")[-1500:]
        raise RuntimeError(error or "FFmpeg processing failed.")

    return stdout

async def download_replied_media(client, message, folder):
    """Download media from the replied-to message."""
    replied = message.reply_to_message

    if not replied:
        await message.reply_text(
            "⚠️ Reply to a video, audio, or media file with this command."
        )
        return None

    if not (
        replied.video
        or replied.document
        or replied.audio
        or replied.voice
        or replied.animation
    ):
        await message.reply_text("⚠️ The replied message has no supported media.")
        return None

    media = (
        replied.video
        or replied.document
        or replied.audio
        or replied.voice
        or replied.animation
    )

    if media.file_size and media.file_size > MAX_UPLOAD_SIZE:
        await message.reply_text("⚠️ This file exceeds the configured 2 GB limit.")
        return None

    status = await message.reply_text("📥 Downloading media...")

    path = await client.download_media(
        replied,
        file_name=str(Path(folder) / "input_media"),
    )

    if not path or not os.path.isfile(path):
        await status.edit_text("❌ Download failed.")
        return None

    return path, status

# ------------------------- #
# SCREENSHOT COMMAND
# Usage: Reply to a video with /screenshot
# ------------------------- #

@Client.on_message(filters.command("screenshot"))
async def screenshot_command(client: Client, message: Message):
    async with asyncio.Lock():
        with tempfile.TemporaryDirectory() as folder:
            result = await download_replied_media(client, message, folder)

            if not result:
                return

            input_path, status = result
            output_path = os.path.join(folder, "screenshots.jpg")

            try:
                await status.edit_text("🖼 Generating video screenshots...")

                await run_ffmpeg(
                    "-i", input_path,
                    "-vf",
                    "fps=1/5,scale=320:-1:force_original_aspect_ratio=decrease,"
                    "tile=3x3",
                    "-frames:v", "1",
                    output_path,
                )

                if not os.path.isfile(output_path):
                    raise RuntimeError("No screenshots could be generated.")

                await message.reply_photo(
                    photo=output_path,
                    caption="🖼 <b>Video Screenshot Sheet</b>\n"
                            "Generated from the replied media."
                )
                await status.delete()

            except Exception as error:
                await status.edit_text(
                    f"❌ Screenshot generation failed:\n<code>{str(error)[:700]}</code>"
                )

# ------------------------- #
# SAMPLE COMMAND
# Usage: Reply to a video with /sample
# ------------------------- #

@Client.on_message(filters.command("sample"))
async def sample_command(client: Client, message: Message):
    with tempfile.TemporaryDirectory() as folder:
        result = await download_replied_media(client, message, folder)

        if not result:
            return

        input_path, status = result
        output_path = os.path.join(folder, "sample.mp4")

        try:
            await status.edit_text(
                f"🎬 Creating a {SAMPLE_DURATION}-second video sample..."
            )

            await run_ffmpeg(
                "-i", input_path,
                "-t", str(SAMPLE_DURATION),
                "-map", "0:v:0",
                "-map", "0:a:0?",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-crf", "28",
                "-c:a", "aac",
                "-b:a", "96k",
                "-movflags", "+faststart",
                output_path,
            )

            if not os.path.isfile(output_path) or os.path.getsize(output_path) == 0:
                raise RuntimeError("Could not create a video sample.")

            await message.reply_video(
                video=output_path,
                caption=f"🎬 <b>Video Sample</b>\n"
                        f"Duration: {SAMPLE_DURATION} seconds"
            )
            await status.delete()

        except Exception as error:
            await status.edit_text(
                f"❌ Sample generation failed:\n<code>{str(error)[:700]}</code>"
            )

# ------------------------- #
# SPEK COMMAND
# Usage: Reply to audio/video with /spek
# ------------------------- #

@Client.on_message(filters.command("spek"))
async def spek_command(client: Client, message: Message):
    with tempfile.TemporaryDirectory() as folder:
        result = await download_replied_media(client, message, folder)

        if not result:
            return

        input_path, status = result
        output_path = os.path.join(folder, "spectrogram.png")

        try:
            await status.edit_text("🎵 Generating audio spectrogram...")

            await run_ffmpeg(
                "-i", input_path,
                "-map", "0:a:0",
                "-lavfi",
                "showspectrumpic=s=1600x900:legend=1:scale=log",
                "-frames:v", "1",
                output_path,
            )

            if not os.path.isfile(output_path):
                raise RuntimeError("No audio stream found or spectrogram unavailable.")

            await message.reply_photo(
                photo=output_path,
                caption="🎵 <b>Audio Spectrogram</b>\n"
                        "Generated from the replied media."
            )
            await status.delete()

        except Exception as error:
            await status.edit_text(
                f"❌ Spectrogram generation failed:\n<code>{str(error)[:700]}</code>"
            )

# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #