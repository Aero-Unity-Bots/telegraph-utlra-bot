
# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

FROM python:3.11-slim

WORKDIR /app

# Install FFmpeg, FFprobe, and MediaInfo
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        mediainfo \
    && rm -rf /var/lib/apt/lists/*

# Verify required FFmpeg components
RUN ffmpeg -hide_banner -encoders 2>/dev/null | grep -q 'png' \
    && ffmpeg -hide_banner -encoders 2>/dev/null | grep -q 'libx264' \
    && ffmpeg -hide_banner -filters 2>/dev/null | grep -q 'showspectrumpic'

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot source code
COPY . .

# Start bot
CMD ["python", "bot.py"]

# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #
