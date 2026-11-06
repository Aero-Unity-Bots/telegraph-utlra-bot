
# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

import asyncio
import html
import json
import os
import tempfile

from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import Message

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

SAMPLE_DURATION = 15
MAX_UPLOAD_SIZE = 2 * 1024 * 1024 * 1024
SCREENSHOT_WIDTH = 480
SCREENSHOT_HEIGHT = 270
SPEK_MAX_DURATION = 300
SPEK_TIMEOUT = 240

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def run_process(*args, timeout=600):

    process = await asyncio.create_subprocess_exec(
        *map(str, args),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    try:
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=timeout
        )

    except asyncio.TimeoutError:

        try:
            process.kill()
        except ProcessLookupError:
            pass

        await process.communicate()

        raise RuntimeError(
            f"Processing timed out after {timeout} seconds."
        )

    if process.returncode != 0:

        error = stderr.decode(
            "utf-8",
            errors="replace"
        ).strip()

        raise RuntimeError(
            error[-3000:] or "Processing failed."
        )

    return stdout

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def run_ffmpeg(*args, timeout=600):

    return await run_process(
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "error",
        "-y",
        *args,
        timeout=timeout
    )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def probe_media(path):

    output = await run_process(
        "ffprobe",
        "-v", "error",
        "-show_format",
        "-show_streams",
        "-of", "json",
        path,
        timeout=60
    )

    try:
        return json.loads(output.decode("utf-8"))

    except json.JSONDecodeError:
        raise RuntimeError(
            "Could not read media information."
        )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def get_video_duration(path):

    output = await run_process(
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path,
        timeout=60
    )

    try:
        duration = float(output.decode().strip())

    except (ValueError, TypeError):
        raise RuntimeError(
            "Unable to determine video duration."
        )

    if duration <= 0:
        raise RuntimeError("Invalid video duration.")

    return duration

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_streams(data):
    return data.get("streams", [])

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def has_video(data):

    return any(
        stream.get("codec_type") == "video"
        for stream in get_streams(data)
    )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def has_audio(data):

    return any(
        stream.get("codec_type") == "audio"
        for stream in get_streams(data)
    )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def download_replied_media(client, message, folder):

    replied = message.reply_to_message

    if not replied:

        await message.reply_text(
            "⚠️ Reply to a video or audio file with this command."
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

        await message.reply_text(
            "⚠️ No supported media found."
        )

        return None

    if media.file_size and media.file_size > MAX_UPLOAD_SIZE:

        await message.reply_text(
            "⚠️ File exceeds the configured 2 GB limit."
        )

        return None

    mime_type = getattr(media, "mime_type", "") or ""

    if (
        replied.document
        and not mime_type.startswith(("video/", "audio/"))
    ):

        await message.reply_text(
            "⚠️ This document does not appear to be an audio or video file."
        )

        return None

    status = await message.reply_text(
        "📥 <b>Downloading media...</b>"
    )

    last_error = None

    for attempt in range(1, 4):

        download_path = os.path.join(
            folder,
            f"input_media_{attempt}"
        )

        try:

            if os.path.exists(download_path):
                os.remove(download_path)

            await status.edit_text(
                f"📥 <b>Downloading media...</b>\n\n"
                f"Attempt: {attempt}/3"
            )

            path = await client.download_media(
                replied,
                file_name=download_path
            )

            if not path or not os.path.isfile(path):
                raise RuntimeError(
                    "Telegram download returned no file."
                )

            actual_size = os.path.getsize(path)

            if actual_size <= 0:
                raise RuntimeError(
                    "Downloaded file is empty."
                )

            expected_size = media.file_size or 0

            if expected_size and actual_size != expected_size:

                raise RuntimeError(
                    f"Incomplete download: expected "
                    f"{expected_size} bytes, received "
                    f"{actual_size} bytes."
                )

            print(
                f"[Media Download Success] "
                f"{actual_size / (1024 * 1024):.2f} MB"
            )

            return path, status

        except Exception as error:

            last_error = error

            print(
                f"[Media Download Error] "
                f"Attempt {attempt}/3: {error}"
            )

            if attempt < 3:
                await asyncio.sleep(attempt * 5)

    await show_error(
        status,
        "Download failed after 3 attempts",
        last_error
    )

    return None

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def show_error(status, title, error):

    try:

        error_text = html.escape(
            str(error)[-2500:]
        )

        await status.edit_text(
            f"❌ <b>{html.escape(title)}</b>\n\n"
            f"<code>{error_text}</code>"
        )

    except Exception:
        pass

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def check_output(path):

    if not os.path.isfile(path):
        raise RuntimeError(
            "Output file was not created."
        )

    if os.path.getsize(path) <= 0:
        raise RuntimeError(
            "Output file is empty."
        )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def generate_screenshots(video_path, output_path, folder):

    duration = await get_video_duration(video_path)

    timestamps = [
        duration * 0.10,
        duration * 0.20,
        duration * 0.30,
        duration * 0.40,
        duration * 0.50,
        duration * 0.60,
        duration * 0.70,
        duration * 0.80,
        duration * 0.90
    ]

    frames = []

    for index, timestamp in enumerate(timestamps):

        frame_path = os.path.join(
            folder,
            f"frame_{index}.jpg"
        )

        try:

            await run_ffmpeg(
                "-ss", str(timestamp),
                "-i", video_path,
                "-frames:v", "1",
                "-vf",
                (
                    f"scale={SCREENSHOT_WIDTH}:{SCREENSHOT_HEIGHT}:"
                    "force_original_aspect_ratio=decrease,"
                    f"pad={SCREENSHOT_WIDTH}:{SCREENSHOT_HEIGHT}:"
                    "(ow-iw)/2:(oh-ih)/2"
                ),
                "-q:v", "3",
                "-f", "image2",
                frame_path,
                timeout=120
            )

            check_output(frame_path)

            with Image.open(frame_path) as image:
                frames.append(
                    image.convert("RGB").copy()
                )

        except Exception as error:

            print(
                f"[Screenshot Frame {index + 1} Error] {error}"
            )

            continue

    if not frames:

        raise RuntimeError(
            "Could not extract any screenshots from this video."
        )

    while len(frames) < 9:
        frames.append(frames[-1].copy())

    frames = frames[:9]

    collage = Image.new(
        "RGB",
        (
            SCREENSHOT_WIDTH * 3,
            SCREENSHOT_HEIGHT * 3
        ),
        "black"
    )

    try:

        for index, frame in enumerate(frames):

            x = (index % 3) * SCREENSHOT_WIDTH
            y = (index // 3) * SCREENSHOT_HEIGHT

            collage.paste(frame, (x, y))

        collage.save(
            output_path,
            "JPEG",
            quality=90,
            optimize=True
        )

    finally:

        for frame in frames:
            frame.close()

        collage.close()

    check_output(output_path)

    return output_path

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def generate_sample(video_path, output_path):
    duration = await get_video_duration(video_path)
    sample_duration = min(
        SAMPLE_DURATION,
        duration
    )

    start_time = max(
        0,
        (duration - sample_duration) / 2
    )

    data = await probe_media(video_path)

    if not has_video(data):
        raise RuntimeError(
            "No video stream found in this file."
        )

    arguments = [
        "-ss", str(start_time),
        "-i", video_path,
        "-t", str(sample_duration),
        "-map", "0:v:0",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-pix_fmt", "yuv420p"
    ]

    audio_present = has_audio(data)

    if audio_present:

        arguments.extend([
            "-map", "0:a:0",
            "-c:a", "aac",
            "-b:a", "128k"
        ])

    else:

        arguments.append("-an")

    arguments.extend([
        "-movflags", "+faststart",
        "-f", "mp4",
        output_path
    ])

    await run_ffmpeg(
        *arguments,
        timeout=900
    )

    check_output(output_path)

    return sample_duration, start_time, audio_present

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def build_sample_caption(replied, sample_duration, start_time, audio_present):
    original_caption = (
        replied.caption
        or replied.text
        or ""
    ).strip()

    original_caption = html.escape(original_caption)
    max_original_length = 650

    if len(original_caption) > max_original_length:

        original_caption = (
            original_caption[:max_original_length]
            + "..."
        )

    parts = [
        "🎬 <b>Video Sample</b>"
    ]

    if original_caption:

        parts.extend([
            "",
            "📄 <b>Original Caption:</b>",
            original_caption
        ])

    parts.extend([
        "",
        f"⏱ <b>Duration:</b> {int(sample_duration)} seconds",
        f"📍 <b>Starting at:</b> {int(start_time)} seconds",
        (
            "🔊 <b>Audio:</b> Original audio preserved"
            if audio_present
            else "🔇 <b>Audio:</b> No audio track found"
        )
    ])

    return "\n".join(parts)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def generate_spectrogram(input_path, output_path):

    data = await probe_media(input_path)

    if not has_audio(data):

        raise RuntimeError(
            "No audio stream found. Cannot generate a spectrogram."
        )
        
    duration = data.get("format", {}).get("duration")

    try:
        duration = float(duration)
    except (ValueError, TypeError):
        duration = SPEK_MAX_DURATION

    processing_duration = min(
        duration,
        SPEK_MAX_DURATION
    )

    if processing_duration <= 0:
        processing_duration = SPEK_MAX_DURATION

    print(
        f"[Spek] Processing {processing_duration:.1f} seconds of audio."
    )

    filter_complex = (
        "[0:a:0]"
        "aresample=11025,"
        "aformat=channel_layouts=mono,"
        "showspectrumpic="
        "s=1600x900:"
        "legend=1:"
        "scale=log:"
        "color=intensity"
        "[spec]"
    )

    await run_ffmpeg(
        "-i", input_path,
        "-t", str(processing_duration),
        "-filter_complex", filter_complex,
        "-map", "[spec]",
        "-frames:v", "1",
        "-c:v", "png",
        "-f", "image2",
        output_path,
        timeout=SPEK_TIMEOUT
    )

    check_output(output_path)

    return output_path

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_message(filters.command("screenshot"))
async def screenshot_command(client: Client, message: Message):

    with tempfile.TemporaryDirectory(
        prefix="screenshot_"
    ) as folder:

        result = await download_replied_media(
            client,
            message,
            folder
        )

        if not result:
            return

        input_path, status = result

        try:

            await status.edit_text(
                "🖼 <b>Generating video screenshots...</b>"
            )

            data = await probe_media(input_path)

            if not has_video(data):
                raise RuntimeError(
                    "No video stream found."
                )

            output_path = os.path.join(
                folder,
                "screenshots.jpg"
            )

            await generate_screenshots(
                input_path,
                output_path,
                folder
            )

            await status.edit_text(
                "📤 <b>Uploading screenshot sheet...</b>"
            )

            await message.reply_photo(
                photo=output_path,
                caption=(
                    "🖼 <b>Video Screenshot Sheet</b>\n\n"
                    "📸 9 extracted frames"
                )
            )

            await status.delete()

        except Exception as error:

            await show_error(
                status,
                "Screenshot generation failed",
                error
            )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_message(filters.command("sample"))
async def sample_command(client: Client, message: Message):

    with tempfile.TemporaryDirectory(
        prefix="sample_"
    ) as folder:

        result = await download_replied_media(
            client,
            message,
            folder
        )

        if not result:
            return

        input_path, status = result

        try:

            await status.edit_text(
                "🎬 <b>Analyzing video...</b>"
            )

            output_path = os.path.join(
                folder,
                "sample.mp4"
            )

            sample_duration, start_time, audio_present = (
                await generate_sample(
                    input_path,
                    output_path
                )
            )

            await status.edit_text(
                "📤 <b>Uploading video sample...</b>"
            )

            caption = build_sample_caption(
                message.reply_to_message,
                sample_duration,
                start_time,
                audio_present
            )

            await message.reply_video(
                video=output_path,
                caption=caption,
                supports_streaming=True
            )

            await status.delete()

        except Exception as error:

            await show_error(
                status,
                "Sample generation failed",
                error
            )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_message(filters.command("spek"))
async def spek_command(client: Client, message: Message):

    with tempfile.TemporaryDirectory(
        prefix="spek_"
    ) as folder:

        result = await download_replied_media(
            client,
            message,
            folder
        )

        if not result:
            return

        input_path, status = result

        try:
            
            await status.edit_text(
                "🔎 <b>Checking audio stream...</b>"
            )

            data = await probe_media(input_path)

            if not has_audio(data):

                raise RuntimeError(
                    "No audio stream found in this file."
                )

            duration = data.get(
                "format", {}
            ).get("duration", "Unknown")

            try:
                duration = int(float(duration))
            except (ValueError, TypeError):
                duration = "Unknown"
                
            await status.edit_text(
                "🎵 <b>Generating audio spectrogram...</b>\n\n"
                f"⏱ Audio duration: "
                f"{duration if duration != 'Unknown' else 'Unknown'} seconds\n"
                f"⚙️ Processing maximum: {SPEK_MAX_DURATION} seconds\n\n"
                "Please wait..."
            )

            output_path = os.path.join(
                folder,
                "spectrogram.png"
            )

            await generate_spectrogram(
                input_path,
                output_path
            )

            check_output(output_path)

            await status.edit_text(
                "📤 <b>Uploading spectrogram...</b>"
            )

            await message.reply_photo(
                photo=output_path,
                caption="<b>🎵 Audio Spectrogram</b>"
            )

            await status.delete()

        except Exception as error:

            await show_error(
                status,
                "Spectrogram generation failed",
                error
            )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #