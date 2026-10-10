
# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

FROM python:3.11-slim

WORKDIR /app

# Install MediaInfo CLI and FFmpeg/FFprobe
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        mediainfo \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

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