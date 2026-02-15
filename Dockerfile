FROM python:3.9-slim

# Install FFmpeg (Voicegram needs this engine)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all files
COPY . .

# Install dependencies including voicegram
RUN pip install --no-cache-dir flask gunicorn voicegram

# Run the app
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
