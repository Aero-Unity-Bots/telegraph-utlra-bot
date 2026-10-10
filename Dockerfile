
# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

FROM python:3.11-slim

WORKDIR /app

# Install FFmpeg, FFprobe, MediaInfo, and CA certificates
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        mediainfo \
        ca-certificates \
        grep \
    && rm -rf /var/lib/apt/lists/*

# Verify required FFmpeg components
RUN set -eu; \
    ffmpeg -hide_banner -encoders 2>&1 | grep -qE '[[:space:]]png[[:space:]]'; \
    ffmpeg -hide_banner -encoders 2>&1 | grep -qE '[[:space:]]libx264[[:space:]]'; \
    ffmpeg -hide_banner -filters 2>&1 | grep -qE '[[:space:]]showspectrumpic[[:space:]]'; \
    ffprobe -version >/dev/null; \
    mediainfo --Version >/dev/null

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
