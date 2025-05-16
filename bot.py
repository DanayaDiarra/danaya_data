# Telegram Multilingual Translator Bot
# This bot receives text and voice messages from a Telegram group,
# translates them to English, and sends the translated text back.

import os
import logging
import tempfile
import requests
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from googletrans import Translator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Translator
translator = Translator()

# Your Telegram Bot Token
TOKEN = os.getenv("7884468418:AAH2hQcZ43ABqqcKEEviXrFEw31mQt5gOeY")  # use env variable

# Hugging Face Whisper API
HF_API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"
HF_API_KEY = os.getenv("HF_API_KEY")  # Add your Hugging Face token to the env

headers = {"Authorization": f"Bearer {HF_API_KEY}"}


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm a multilingual translator bot. Send a message or voice note.")


def translate_text(update: Update, context: CallbackContext):
    original_text = update.message.text
    translated = translator.translate(original_text, dest='en')
    update.message.reply_text(f"Translation: {translated.text}")


def handle_voice(update: Update, context: CallbackContext):
    file = update.message.voice.get_file()
    with tempfile.TemporaryDirectory() as tmpdir:
        ogg_path = os.path.join(tmpdir, "voice.ogg")
        wav_path = os.path.join(tmpdir, "voice.wav")

        file.download(ogg_path)
        subprocess.run(["ffmpeg", "-i", ogg_path, wav_path])

        with open(wav_path, "rb") as audio_file:
            response = requests.post(HF_API_URL, headers=headers, data=audio_file)

        if response.status_code == 200:
            result = response.json()
            text = result.get("text", "")
            translated = translator.translate(text, dest='en')
            update.message.reply_text(f"Voice Translation: {translated.text}")
        else:
            update.message.reply_text("Sorry, I couldn't transcribe the voice message.")


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_text))
    dp.add_handler(MessageHandler(Filters.voice, handle_voice))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
