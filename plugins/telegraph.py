
# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

import requests
import asyncio
import html
import json
import os
import re
import shutil
import subprocess
import tempfile

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

from datetime import datetime
from database import save_post
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegraph import Telegraph

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

TELEGRAPH_AUTHOR_NAME = os.getenv("TELEGRAPH_AUTHOR_NAME", "Aero Unity")
TELEGRAPH_AUTHOR_URL = os.getenv(
    "TELEGRAPH_AUTHOR_URL",
    "https://t.me/Aero_Unity"
)

TELEGRAPH_CHANNEL = os.getenv("TELEGRAPH_CHANNEL", "Aero Unity")
TELEGRAPH_DEVELOPER = os.getenv("TELEGRAPH_DEVELOPER", "Mohammed")
TELEGRAPH_DEVELOPER_URL = os.getenv(
    "TELEGRAPH_DEVELOPER_URL",
    "https://t.me/Mr_Mohammed_29"
)

MAX_TELEGRAPH_CONTENT = 62000
PREVIEW_WIDTH = 640
PREVIEW_HEIGHT = 360
PREVIEW_COUNT = 4

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

LANGUAGE_NAMES = {
    "aa": "Afar",
    "ab": "Abkhazian",
    "af": "Afrikaans",
    "ak": "Akan",
    "am": "Amharic",
    "ar": "Arabic",
    "as": "Assamese",
    "ay": "Aymara",
    "az": "Azerbaijani",
    "ba": "Bashkir",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "bh": "Bihari",
    "bn": "Bengali",
    "bo": "Tibetan",
    "br": "Breton",
    "bs": "Bosnian",
    "ca": "Catalan",
    "co": "Corsican",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "dv": "Divehi",
    "dz": "Dzongkha",
    "el": "Greek",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "eu": "Basque",
    "fa": "Persian",
    "fi": "Finnish",
    "fj": "Fijian",
    "fo": "Faroese",
    "fr": "French",
    "fy": "Frisian",
    "ga": "Irish",
    "gd": "Scottish Gaelic",
    "gl": "Galician",
    "gn": "Guarani",
    "gu": "Gujarati",
    "ha": "Hausa",
    "he": "Hebrew",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "ig": "Igbo",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "jv": "Javanese",
    "ka": "Georgian",
    "kk": "Kazakh",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "ks": "Kashmiri",
    "ku": "Kurdish",
    "ky": "Kyrgyz",
    "la": "Latin",
    "lb": "Luxembourgish",
    "ln": "Lingala",
    "lo": "Lao",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "mg": "Malagasy",
    "mi": "Maori",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mn": "Mongolian",
    "mr": "Marathi",
    "ms": "Malay",
    "mt": "Maltese",
    "my": "Burmese",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "oc": "Occitan",
    "or": "Odia",
    "pa": "Punjabi",
    "pl": "Polish",
    "ps": "Pashto",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "rw": "Kinyarwanda",
    "sa": "Sanskrit",
    "sd": "Sindhi",
    "si": "Sinhala",
    "sk": "Slovak",
    "sl": "Slovenian",
    "sm": "Samoan",
    "sn": "Shona",
    "so": "Somali",
    "sq": "Albanian",
    "sr": "Serbian",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tk": "Turkmen",
    "tl": "Tagalog",
    "tr": "Turkish",
    "tt": "Tatar",
    "ug": "Uyghur",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "uz": "Uzbek",
    "vi": "Vietnamese",
    "wo": "Wolof",
    "xh": "Xhosa",
    "yi": "Yiddish",
    "yo": "Yoruba",
    "zh": "Chinese",
    "zu": "Zulu",

    # ISO-639-2 / ISO-639-3 common codes
    "aar": "Afar",
    "afr": "Afrikaans",
    "amh": "Amharic",
    "ara": "Arabic",
    "asm": "Assamese",
    "aze": "Azerbaijani",
    "bel": "Belarusian",
    "ben": "Bengali",
    "bod": "Tibetan",
    "bos": "Bosnian",
    "bul": "Bulgarian",
    "cat": "Catalan",
    "ces": "Czech",
    "chi": "Chinese",
    "zho": "Chinese",
    "dan": "Danish",
    "deu": "German",
    "ger": "German",
    "ell": "Greek",
    "gre": "Greek",
    "eng": "English",
    "est": "Estonian",
    "eus": "Basque",
    "fas": "Persian",
    "per": "Persian",
    "fin": "Finnish",
    "fra": "French",
    "fre": "French",
    "guj": "Gujarati",
    "heb": "Hebrew",
    "hin": "Hindi",
    "hrv": "Croatian",
    "hun": "Hungarian",
    "hye": "Armenian",
    "arm": "Armenian",
    "ind": "Indonesian",
    "isl": "Icelandic",
    "ice": "Icelandic",
    "ita": "Italian",
    "jpn": "Japanese",
    "jav": "Javanese",
    "kat": "Georgian",
    "kaz": "Kazakh",
    "khm": "Khmer",
    "kan": "Kannada",
    "kor": "Korean",
    "kur": "Kurdish",
    "lao": "Lao",
    "lit": "Lithuanian",
    "lav": "Latvian",
    "mal": "Malayalam",
    "mar": "Marathi",
    "mkd": "Macedonian",
    "mac": "Macedonian",
    "msa": "Malay",
    "may": "Malay",
    "mya": "Burmese",
    "bur": "Burmese",
    "nep": "Nepali",
    "nld": "Dutch",
    "dut": "Dutch",
    "nor": "Norwegian",
    "ori": "Odia",
    "pan": "Punjabi",
    "pol": "Polish",
    "por": "Portuguese",
    "ron": "Romanian",
    "rum": "Romanian",
    "rus": "Russian",
    "san": "Sanskrit",
    "sin": "Sinhala",
    "slk": "Slovak",
    "slo": "Slovak",
    "slv": "Slovenian",
    "spa": "Spanish",
    "srp": "Serbian",
    "swe": "Swedish",
    "tam": "Tamil",
    "tel": "Telugu",
    "tha": "Thai",
    "tgl": "Tagalog",
    "tur": "Turkish",
    "ukr": "Ukrainian",
    "urd": "Urdu",
    "uzb": "Uzbek",
    "vie": "Vietnamese",
    "yid": "Yiddish",
    "yor": "Yoruba",
    "zul": "Zulu",
}

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

tg = Telegraph()

try:
    tg.create_account(
        short_name="ultra-bot",
        author_name=TELEGRAPH_AUTHOR_NAME,
        author_url=TELEGRAPH_AUTHOR_URL
    )
except Exception as error:
    print(f"[Telegraph Account Error] {error}")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def escape_html(text):
    return html.escape(str(text), quote=True)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def clean_filename(filename):
    if not filename:
        return "MediaInfo"

    filename = os.path.basename(filename).strip()

    return filename[:247] + "..." if len(filename) > 250 else filename

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_media_filename(message):

    if message.document:
        return message.document.file_name or "MediaInfo"

    if message.video:
        return message.video.file_name or "Video"

    if message.audio:
        return message.audio.file_name or "Audio"

    if message.animation:
        return message.animation.file_name or "Animation"

    return "MediaInfo"

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def normalize_language(language):

    if not language:
        return "Unknown"

    language = str(language).strip()

    if not language:
        return "Unknown"

    language = language.split("(")[0].strip()
    language = language.replace("_", "-")
    lowered = language.lower()

    if lowered in ("und", "unknown", "undefined", "un"):
        return "Unknown"

    for name in LANGUAGE_NAMES.values():
        if lowered == name.lower():
            return name

    code = lowered.split("-")[0].strip()

    if code in LANGUAGE_NAMES:
        return LANGUAGE_NAMES[code]

    return language.title()

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_track_language(track):
    preferred_keys = [
        "Language/String1",
        "Language/String",
        "Language_String",
        "Language",
        "Language/String2",
        "Language/String3",
        "Language/String4",
    ]

    candidates = []

    for key in preferred_keys:
        value = track.get(key)

        if value not in (None, ""):
            candidates.append(str(value).strip())

    for candidate in candidates:

        normalized = normalize_language(candidate)

        if normalized != "Unknown":
            return normalized

    return "Unknown"

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def run_command(command, timeout=180):

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout
        )

    except FileNotFoundError:
        raise RuntimeError(
            f"Required program not installed: {command[0]}"
        )

    except subprocess.TimeoutExpired:
        raise RuntimeError(
            f"{command[0]} operation timed out."
        )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip() or "Command failed."
        )

    return result.stdout.strip()

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def run_mediainfo(file_path):

    output = run_command([
        "mediainfo",
        "--Output=Text",
        file_path
    ])

    if not output:
        raise RuntimeError("MediaInfo returned empty output.")

    return output

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def run_mediainfo_json(file_path):

    output = run_command([
        "mediainfo",
        "--Output=JSON",
        file_path
    ])

    try:
        return json.loads(output)

    except json.JSONDecodeError:
        return {}

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_json_tracks(data):

    try:
        return data["media"]["track"]

    except (KeyError, TypeError):
        return []


# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def track_value(track, *keys, default=None):

    for key in keys:

        value = track.get(key)

        if value not in (None, ""):
            return str(value).strip()

    return default

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_audio_tracks(data):

    audio_tracks = []

    for track in get_json_tracks(data):

        if str(track.get("@type", "")).lower() != "audio":
            continue

        language = get_track_language(track)

        codec = track_value(
            track,
            "Format",
            "CodecID/Hint",
            "CodecID",
            default="Unknown"
        )

        channels = track_value(
            track,
            "Channel(s)/String",
            "Channel(s)_String",
            "Channel(s)",
            default=None
        )

        title = track_value(
            track,
            "Title",
            default=None
        )

        details = f"{language} ({codec})"

        if channels:
            details += f" - {channels}"

        if title:
            details += f" - {title}"

        audio_tracks.append(details)

    return audio_tracks

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_subtitle_tracks(data):

    subtitles = []

    for track in get_json_tracks(data):

        if str(track.get("@type", "")).lower() != "text":
            continue

        language = get_track_language(track)

        subtitle_format = track_value(
            track,
            "Format",
            "CodecID/Hint",
            "CodecID",
            default="Unknown"
        )

        title = track_value(
            track,
            "Title",
            default=None
        )

        item = {
            "language": language,
            "format": subtitle_format,
            "title": title
        }

        if item not in subtitles:
            subtitles.append(item)

    return subtitles

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def split_mediainfo_sections(media_info):

    sections = []
    current_name = None
    current_lines = []

    def save_section():

        if current_name is not None:

            body = "\n".join(current_lines).strip()

            if body:
                sections.append((current_name, body))

    for raw_line in media_info.splitlines():

        line = raw_line.rstrip()
        stripped = line.strip()

        match = re.fullmatch(
            r"(General|Video|Audio|Text|Image|Menu|Other)(?:\s+#?\d+)?",
            stripped,
            re.IGNORECASE
        )

        if match and not line.startswith((" ", "\t")):

            save_section()

            current_name = match.group(1).title()
            current_lines = []

        elif current_name is not None:

            current_lines.append(line)

    save_section()

    return sections

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def section_icon(name):

    icons = {
        "General": "📁",
        "Video": "🎞️",
        "Audio": "🔊",
        "Text": "💬",
        "Image": "🖼️",
        "Menu": "📋",
        "Other": "📦"
    }

    return icons.get(name, "📄")

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def get_video_duration(file_path):

    output = run_command([
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ], timeout=60)

    try:
        return max(0, float(output))

    except (ValueError, TypeError):
        return 0

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def has_video_stream(file_path, data=None):

    for track in get_json_tracks(data or {}):

        if str(track.get("@type", "")).lower() == "video":
            return True

    try:

        output = run_command([
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=codec_type",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ], timeout=60)

        return "video" in output.lower()

    except Exception:
        return False

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def generate_preview_collage(video_path, output_path, folder):

    duration = get_video_duration(video_path)

    if duration <= 0:
        raise RuntimeError("Could not read video duration.")

    timestamps = [
        duration * 0.10,
        duration * 0.35,
        duration * 0.60,
        duration * 0.85
    ]

    frames = []

    for index, timestamp in enumerate(timestamps):

        frame_path = os.path.join(
            folder,
            f"preview_{index}.jpg"
        )

        try:

            run_command([
                "ffmpeg",
                "-hide_banner",
                "-loglevel", "error",
                "-y",
                "-ss", str(timestamp),
                "-i", video_path,
                "-frames:v", "1",
                "-vf",
                (
                    f"scale={PREVIEW_WIDTH}:{PREVIEW_HEIGHT}:"
                    "force_original_aspect_ratio=decrease,"
                    f"pad={PREVIEW_WIDTH}:{PREVIEW_HEIGHT}:"
                    "(ow-iw)/2:(oh-ih)/2"
                ),
                "-q:v", "3",
                "-f", "image2",
                frame_path
            ], timeout=120)

            if os.path.isfile(frame_path):

                with Image.open(frame_path) as image:

                    frames.append(
                        image.convert("RGB").copy()
                    )

        except Exception as error:
            print(f"[Preview Frame {index + 1} Error] {error}")
            continue

    if not frames:
        raise RuntimeError(
            "Could not generate episode preview frames."
        )

    while len(frames) < PREVIEW_COUNT:
        frames.append(frames[-1].copy())

    frames = frames[:PREVIEW_COUNT]

    collage = Image.new(
        "RGB",
        (
            PREVIEW_WIDTH * 2,
            PREVIEW_HEIGHT * 2
        ),
        "black"
    )

    positions = [
        (0, 0),
        (PREVIEW_WIDTH, 0),
        (0, PREVIEW_HEIGHT),
        (PREVIEW_WIDTH, PREVIEW_HEIGHT)
    ]

    try:

        for frame, position in zip(frames, positions):
            collage.paste(frame, position)

        collage.save(
            output_path,
            format="JPEG",
            quality=88,
            optimize=True
        )

    finally:

        for frame in frames:
            frame.close()

        collage.close()

    if not os.path.isfile(output_path) or os.path.getsize(output_path) == 0:
        raise RuntimeError("Preview collage was not created.")

    return output_path

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def upload_telegraph_image(image_path):

    if not os.path.isfile(image_path):
        raise RuntimeError("Preview image file does not exist.")

    if os.path.getsize(image_path) <= 0:
        raise RuntimeError("Preview image is empty.")

    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")

    if not all([cloud_name, api_key, api_secret]):
        raise RuntimeError(
            "Cloudinary credentials are missing. "
            "Please configure Render environment variables."
        )

    try:
        import cloudinary
        import cloudinary.uploader

        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True
        )

        result = cloudinary.uploader.upload(
            image_path,
            resource_type="image",
            folder="telegraph_previews"
        )

        image_url = result.get("secure_url")

        if not image_url:
            raise RuntimeError(
                "Cloudinary did not return a public image URL."
            )

        print(
            f"[Cloudinary Preview Uploaded] {image_url}"
        )

        return image_url

    except Exception as error:
        raise RuntimeError(
            f"Cloudinary upload failed: {error}"
        )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def format_mediainfo_section(section_content):

    formatted_lines = []

    for raw_line in section_content.splitlines():

        match = re.match(
            r"^(\s*)(.*?)(\s*:\s*)(.*)$",
            raw_line
        )

        if match:

            indent, label, separator, value = match.groups()
            formatted_lines.append(
                f"{indent}{label.strip()} : {value.strip()}"
            )

        else:

            formatted_lines.append(raw_line.rstrip())

    return "\n".join(formatted_lines)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def build_mediainfo_html(
    filename,
    media_info,
    mediainfo_json=None,
    preview_url=None
):

    today = datetime.now().strftime("%B %d, %Y")

    audio_tracks = get_audio_tracks(
        mediainfo_json or {}
    )

    subtitles = get_subtitle_tracks(
        mediainfo_json or {}
    )

    sections = split_mediainfo_sections(media_info)
    content = []
    content.append(
        f"<h3>{escape_html(filename)}</h3>"
    )

    content.append(
        "<p>"
        f"<b>{escape_html(TELEGRAPH_AUTHOR_NAME)}</b>"
        "<br>"
        f"{escape_html(today)}"
        "</p>"
    )

    if preview_url:

        content.append(
            "<p><b>Eᴘɪsᴏᴅᴇ Pʀᴇᴠɪᴇᴡ</b></p>"
        )

        content.append(
            "<figure>"
            f'<img src="{escape_html(preview_url)}"/>'
            "<figcaption>"
            "Eᴘɪsᴏᴅᴇ Sᴄʀᴇᴇɴsʜᴏᴛs Fʀᴏᴍ Fɪʟᴇ"
            "</figcaption>"
            "</figure>"
        )

    content.append(
        "<p><b>🔊 Aᴜᴅɪᴏs</b></p>"
    )

    if audio_tracks:

        for audio in audio_tracks:

            content.append(
                f"<p>• {escape_html(audio)}</p>"
            )

    else:

        content.append(
            "<p>• Nᴏ ᴀᴜᴅɪᴏ ᴛʀᴀᴄᴋs ғᴏᴜɴᴅ</p>"
        )

    content.append(
        "<p><b>💬 Sᴜʙᴛɪᴛʟᴇs</b></p>"
    )

    if subtitles:

        for subtitle in subtitles:

            subtitle_text = (
                f"{subtitle['language']} "
                f"({subtitle['format']})"
            )

            if subtitle["title"]:
                subtitle_text += f" - {subtitle['title']}"

            content.append(
                f"<p>• {escape_html(subtitle_text)}</p>"
            )

    else:

        content.append(
            "<p>• Nᴏ Sᴜʙᴛɪᴛʟᴇs Fᴏᴜɴᴅ</p>"
        )

    for section_name, section_content in sections:

        icon = section_icon(section_name)

        formatted = format_mediainfo_section(
            section_content
        )

        content.append(
            "<p>"
            f"<b>{icon} {escape_html(section_name)}</b>"
            "</p>"
        )

        content.append(
            f"<pre>{escape_html(formatted)}</pre>"
        )

    content.append("<hr>")

    content.append(
        "<p><b>Rᴇᴘᴏʀᴛ Cᴏɴᴛᴇɴᴛ Iɴ Tʜɪs Pᴀɢᴇ, Rᴇᴘᴏʀᴛ Oɴ Bᴇʟᴏᴡ</b></p>"
    )

    content.append(
        "<p>"
        "<b>ᴄʜᴀɴɴᴇʟ :</b> "
        f'<a href="{escape_html(TELEGRAPH_AUTHOR_URL)}">'
        f"{escape_html(TELEGRAPH_CHANNEL)}"
        "</a>"
        "</p>"
    )

    content.append(
        "<p>"
        "<b>ᴅᴇᴠᴇʟᴏᴘᴇʀ :</b> "
        f'<a href="{escape_html(TELEGRAPH_DEVELOPER_URL)}">'
        f"{escape_html(TELEGRAPH_DEVELOPER)}"
        "</a>"
        "</p>"
    )

    return "\n".join(content)

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def trim_telegraph_content(content):

    if len(content.encode("utf-8")) <= MAX_TELEGRAPH_CONTENT:
        return content

    notice = (
        "<hr>"
        "<p><b>"
        "MediaInfo output was shortened because "
        "the Telegraph page reached its content limit."
        "</b></p>"
    )

    while len((content + notice).encode("utf-8")) > MAX_TELEGRAPH_CONTENT:

        match = re.search(
            r"<p><b>[^<]*</b></p>\s*<pre>.*?</pre>",
            content,
            flags=re.DOTALL
        )

        if not match:
            break

        content = content[:match.start()] + content[match.end():]

    if len((content + notice).encode("utf-8")) > MAX_TELEGRAPH_CONTENT:
        raise RuntimeError(
            "The page content is too large for Telegraph."
        )

    return content + notice

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

def create_page(title, content):

    response = tg.create_page(
        title=title,
        html_content=content,
        author_name=TELEGRAPH_AUTHOR_NAME,
        author_url=TELEGRAPH_AUTHOR_URL,
        return_content=False
    )

    return response["url"]

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

async def download_media_with_retry(client, message, folder, filename):
    os.makedirs(folder, exist_ok=True)

    media = (
        message.document
        or message.video
        or message.audio
        or message.animation
    )

    expected_size = getattr(media, "file_size", 0) or 0
    last_error = None

    for attempt in range(1, 4):
        download_path = os.path.join(
            folder,
            f"download_{attempt}_{filename}"
        )

        try:

            if os.path.exists(download_path):
                os.remove(download_path)

            print(
                f"[Telegraph Download] Attempt "
                f"{attempt}/3 | Expected size: {expected_size} bytes"
            )

            downloaded_path = await client.download_media(
                message,
                file_name=download_path
            )

            if not downloaded_path:
                raise RuntimeError(
                    "Telegram returned no download path."
                )

            if not os.path.isfile(downloaded_path):
                raise RuntimeError(
                    f"Downloaded file does not exist: {downloaded_path}"
                )

            actual_size = os.path.getsize(downloaded_path)

            if actual_size <= 0:
                raise RuntimeError(
                    "Downloaded file is empty (0 bytes)."
                )

            if expected_size and actual_size != expected_size:
                raise RuntimeError(
                    f"Incomplete download: expected "
                    f"{expected_size} bytes, received {actual_size} bytes."
                )

            print(
                f"[Telegraph Download Success] "
                f"{actual_size / (1024 * 1024):.2f} MB"
            )

            return downloaded_path

        except Exception as error:
            last_error = error

            print(
                f"[Telegraph Download Error] "
                f"Attempt {attempt}/3: {error}"
            )

            for path in (download_path, locals().get("downloaded_path")):
                if path and os.path.isfile(path):
                    try:
                        os.remove(path)
                    except OSError:
                        pass

            if attempt < 3:
                await asyncio.sleep(attempt * 5)

    raise RuntimeError(
        f"Download failed after 3 attempts: {last_error}"
    )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

@Client.on_message(filters.command("tgm"))
async def telegraph(_, message):

    if message.reply_to_message:
        reply = message.reply_to_message
        is_media = any([
            reply.document,
            reply.video,
            reply.audio,
            reply.animation
        ])

        if is_media:
            status = await message.reply_text(
                "⏳ <b>Dᴏᴡɴʟᴏᴀᴅɪɴɢ Cᴜʀʀᴇɴᴛ Fɪʟᴇ...</b>"
            )
            temp_dir = tempfile.mkdtemp(
                prefix="telegraph_"
            )
            try:

                filename = get_media_filename(reply)
                safe_name = (
                    os.path.basename(filename)
                    or "MediaInfo"
                )
                await status.edit_text(
                    " <b>Dᴏᴡɴʟᴏᴀᴅɪɴɢ ᴍᴇᴅɪᴀ ғʀᴏᴍ Tᴇʟᴇɢʀᴀᴍ..</b>"
                )
                file_path = await download_media_with_retry(
                    _,
                    reply,
                    temp_dir,
                    safe_name
                )
                await status.edit_text(
                    "🔎 <b>Rᴇᴀᴅɪɴɢ MᴇᴅɪᴀIɴғᴏ ᴀɴᴅ ᴅᴇᴛᴇᴄᴛɪɴɢ ᴛʀᴀᴄᴋs...</b>"
                )
                media_info, mediainfo_json = await asyncio.gather(

                    asyncio.to_thread(
                        run_mediainfo,
                        file_path
                    ),

                    asyncio.to_thread(
                        run_mediainfo_json,
                        file_path
                    )

                )

                preview_url = None

                if has_video_stream(file_path, mediainfo_json):

                    await status.edit_text(
                        " <b>Gᴇɴᴇʀᴀᴛɪɴɢ ᴇᴘɪsᴏᴅᴇ ᴘʀᴇᴠɪᴇᴡ sᴄʀᴇᴇɴsʜᴏᴛs...</b>"
                    )

                    collage_path = os.path.join(
                        temp_dir,
                        "episode_preview.jpg"
                    )

                    await asyncio.to_thread(
                        generate_preview_collage,
                        file_path,
                        collage_path,
                        temp_dir
                    )

                    if not os.path.isfile(collage_path):
                        raise RuntimeError(
                            "Preview collage generation failed."
                        )

                    if os.path.getsize(collage_path) <= 0:
                        raise RuntimeError(
                            "Generated preview collage is empty."
                        )

                    await status.edit_text(
                        "☁️ <b>Uᴘʟᴏᴀᴅɪɴɢ ᴇᴘɪsᴏᴅᴇ ᴘʀᴇᴠɪᴇᴡ ᴛᴏ Cʟᴏᴜᴅɪɴᴀʀʏ...</b>"
                    )

                    preview_url = await asyncio.to_thread(
                        upload_telegraph_image,
                        collage_path
                    )

                    if not preview_url:
                        raise RuntimeError(
                            "Telegraph preview URL was not generated."
                        )

                    print(
                        f"[Telegraph Preview Ready] {preview_url}"
                    )

                await status.edit_text(
                    "📝 <b>Cʀᴇᴀᴛɪɴɢ Tᴇʟᴇɢʀᴀᴘʜ Pᴀɢᴇ...</b>"
                )

                content = build_mediainfo_html(
                    filename,
                    media_info,
                    mediainfo_json=mediainfo_json,
                    preview_url=preview_url
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

                try:

                    if message.from_user:

                        save_post(
                            message.from_user.id,
                            url,
                            title
                        )

                except Exception as error:
                    print(
                        f"[Telegraph Save Error] {error}"
                    )

                preview_status = (
                    "✅ Preview images added"
                    if preview_url
                    else "⚠️ Preview images unavailable"
                )

                await status.edit_text(

                    "✅ <b>Tᴇʟᴇɢʀᴀᴘʜ Pᴀɢᴇ Cʀᴇᴀᴛᴇᴅ</b>\n\n"

                    f"✦ <b>Fɪʟᴇ Nᴀᴍᴇ : </b> <code>{escape_html(filename)}</code>\n"
                    f"✦ <b>Lɪɴᴋ :</b> {escape_html(url)}",

                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(
                                "• Oᴘᴇɴ Tᴇʟᴇɢʀᴀᴘʜ Pᴀɢᴇ •",
                                url=url
                            )
                        ]
                    ])

                )

            except Exception as error:

                error_text = str(error)

                if len(error_text) > 1000:
                    error_text = error_text[:1000] + "..."

                await status.edit_text(
                    "❌ <b>Failed to create Telegraph page.</b>\n\n"
                    f"<code>{escape_html(error_text)}</code>"
                )

            finally:

                shutil.rmtree(
                    temp_dir,
                    ignore_errors=True
                )

            return

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #

    title = "Telegraph Post"
    text = None

    if "|" in (message.text or ""):

        try:

            title_part, text = message.text.split(
                "|",
                1
            )

            command_parts = title_part.split(
                None,
                1
            )

            if len(command_parts) > 1:
                title = command_parts[1].strip()

            text = text.strip()

        except Exception:
            pass

    elif message.reply_to_message:

        reply = message.reply_to_message

        text = reply.text or reply.caption

    elif len(message.command) > 1:

        text = message.text.split(
            None,
            1
        )[1]

    if not text:

        return await message.reply_text(
            "❌ <b>Send some text or reply to a text/media message.</b>\n\n"

            "For MediaInfo:\n"
            "1. Send your video or media file\n"
            "2. Reply to file with <code>/tgm</code>"
        )

    content = (
        "<p>"
        + escape_html(text).replace("\n", "<br>")
        + "</p>"
        + "<hr>"
        + (
            "<p><b>ᴄʜᴀɴɴᴇʟ :</b> "
            '<a href="https://t.me/Aero_Unity">'
            "ᴀᴇʀᴏ ᴜɴɪᴛʏ</a></p>"
        )
        + (
            "<p><b>ᴅᴇᴠᴇʟᴏᴘᴇʀ :</b> "
            '<a href="https://t.me/Mr_Mohammed_29">'
            "ᴍᴏʜᴀᴍᴍᴇᴅ</a></p>"
        )
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

        except Exception as error:
            print(f"[Telegraph Save Error] {error}")

        await message.reply_text(

            "✅ <b>Tᴇʟᴇɢʀᴀᴘʜ Pᴀɢᴇ Cʀᴇᴀᴛᴇᴅ</b>\n\n"
            f"{escape_html(url)}",

            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "• Oᴘᴇɴ Tᴇʟᴇɢʀᴀᴘʜ Pᴀɢᴇ •",
                        url=url
                    )
                ]
            ])

        )

    except Exception as error:

        await message.reply_text(
            "❌ <b>Failed to create Telegraph page.</b>\n\n"
            f"<code>{escape_html(str(error))}</code>"
        )

# ------------------------ #
# Don't Remove My Credits
# Owner: @Mr_Mohammed_29
# Updates: @Aero_Unity 
# Support : @Coders_Grp 
# ------------------------ #