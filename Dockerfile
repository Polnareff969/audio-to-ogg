FROM python:3.9-slim
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN pip install flask gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
