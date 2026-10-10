
# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

import asyncio
import html
import os
import tempfile

from pyrogram import Client, filters
from pyrogram.types import Message

# ------------------------- #
# SETTINGS
# ------------------------- #

SAMPLE_DURATION = 15
MAX_UPLOAD_SIZE = 2 * 1024 * 1024 * 1024


async def run_ffmpeg(*args):
    """Run FFmpeg asynchronously and report errors."""

    process = await asyncio.create_subprocess_exec(
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-y",
        *map(str, args),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    if process.returncode != 0:
        raise RuntimeError(
            stderr.decode(errors="replace")[-1500:]
            or "FFmpeg processing failed."
        )

    return stdout


async def download_replied_media(client, message, folder):
    """Download media from the replied-to message."""

    replied = message.reply_to_message

    if not replied:
        await message.reply_text(
            "⚠️ Reply to a video, audio, or media file with this command."
        )
        return None

    media = (
        replied.video
        or replied.document
        or replied.audio
        or replied.voice
        or replied.animation
    )

    if not media:
        await message.reply_text("⚠️ No supported media found.")
        return None

    if media.file_size and media.file_size > MAX_UPLOAD_SIZE:
        await message.reply_text("⚠️ File exceeds the configured 2 GB limit.")
        return None

    status = await message.reply_text("📥 Downloading media...")

    try:
        path = await client.download_media(
            replied,
            file_name=os.path.join(folder, "input_media"),
        )
    except Exception as error:
        await show_error(status, "Download failed", error)
        return None

    if not path or not os.path.isfile(path):
        await status.edit_text("❌ Download failed.")
        return None

    return path, status


def check_output(path):
    """Check that an output file exists and is not empty."""

    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        raise RuntimeError("FFmpeg did not generate a valid output file.")


async def show_error(status, title, error):
    """Show HTML-safe error details in Telegram."""

    try:
        await status.edit_text(
            f"❌ {title}:\n"
            f"<code>{html.escape(str(error)[:700])}</code>"
        )
    except Exception:
        pass


# ------------------------- #
# SCREENSHOT COMMAND
# Reply to a video with /screenshot
# ------------------------- #

@Client.on_message(filters.command("screenshot"))
async def screenshot_command(client: Client, message: Message):
    with tempfile.TemporaryDirectory() as folder:
        result = await download_replied_media(client, message, folder)

        if not result:
            return

        input_path, status = result
        output_path = os.path.join(folder, "screenshots.jpg")

        try:
            await status.edit_text("🖼 Generating screenshots...")

            await run_ffmpeg(
                "-i", input_path,
                "-vf",
                "fps=1/5,"
                "scale=320:180:force_original_aspect_ratio=decrease,"
                "pad=320:180:(ow-iw)/2:(oh-ih)/2,"
                "tile=3x3",
                "-frames:v", "1",
                "-an",
                "-c:v", "mjpeg",
                "-f", "image2",
                output_path,
            )

            check_output(output_path)

            await message.reply_photo(
                photo=output_path,
                caption="<b>🖼 Video Screenshot Sheet</b>",
            )

            await status.delete()

        except Exception as error:
            await show_error(status, "Screenshot generation failed", error)


# ------------------------- #
# SAMPLE COMMAND
# Reply to a video with /sample
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

            # Keep the original scene and audio for the first 15 seconds.
            # If the source has no audio, the optional audio map is ignored.
            await run_ffmpeg(
                "-i", input_path,
                "-t", str(SAMPLE_DURATION),
                "-map", "0:v:0",
                "-map", "0:a:0?",
                "-c:v", "libx264",
                "-preset", "ultrafast",
                "-crf", "23",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-b:a", "128k",
                "-movflags", "+faststart",
                "-f", "mp4",
                output_path,
            )

            check_output(output_path)

            await message.reply_video(
                video=output_path,
                caption=(
                    "🎬 <b>Video Sample</b>\n"
                    f"Duration: Up to {SAMPLE_DURATION} seconds"
                ),
            )

            await status.delete()

        except Exception as error:
            await show_error(status, "Sample generation failed", error)


# ------------------------- #
# SPEK COMMAND
# Reply to audio/video with /spek
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

            # Map the generated spectrogram as a video/image stream.
            # Explicitly select the PNG encoder and image2 output format.
            await run_ffmpeg(
                "-i", input_path,
                "-filter_complex",
                "[0:a:0]showspectrumpic="
                "s=1600x900:legend=1:scale=log[spec]",
                "-map", "[spec]",
                "-frames:v", "1",
                "-c:v", "png",
                "-f", "image2",
                output_path,
            )

            check_output(output_path)

            await message.reply_photo(
                photo=output_path,
                caption="<b>🎵 Audio Spectrogram</b>",
            )

            await status.delete()

        except Exception as error:
            await show_error(status, "Spectrogram generation failed", error)


# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #
