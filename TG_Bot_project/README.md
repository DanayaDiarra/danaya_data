# Telegram Translation Bot

This bot translates text and voice messages sent in Telegram groups to English automatically.

## Features

- Translates any text message to English
- Transcribes and translates voice messages (e.g., .ogg files) using Whisper
- Deployable on Render, Railway, or Heroku

## Requirements

- Python 3.8+
- ffmpeg installed and available in PATH
- Telegram bot token

## Setup

1. Clone or download the project
2. Install dependencies:

   pip install -r requirements.txt

3. Replace TOKEN in bot.py with your actual Telegram Bot token.
4. Run the bot:

   python bot.py

## Deployment

Use the provided `Procfile` and `runtime.txt` to deploy to Heroku, Render, or Railway.

