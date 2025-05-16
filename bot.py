# Telegram Multilingual Translator Bot
# This bot receives text and voice messages from a Telegram group,
# translates them to English, and sends the translated text back.

import os
import logging
import tempfile
import subprocess
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from googletrans import Translator
import whisper

# Load Whisper model
whisper_model = whisper.load_model("tiny")


# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Google Translator
translator = Translator()

# Telegram bot token
TOKEN = "YOUR_BOT_TOKEN_HERE"

# Handle /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm a translator bot. Send me a message or voice note.")

# Handle text messages
def translate_text(update: Update, context: CallbackContext):
    original_text = update.message.text
    translated = translator.translate(original_text, dest='en')
    update.message.reply_text(f"Translation: {translated.text}")

# Handle voice messages
def handle_voice(update: Update, context: CallbackContext):
    voice = update.message.voice.get_file()
    with tempfile.TemporaryDirectory() as tmpdir:
        ogg_path = os.path.join(tmpdir, "voice.ogg")
        wav_path = os.path.join(tmpdir, "voice.wav")
        
        # Download and convert to wav
        voice.download(ogg_path)
        subprocess.run(["ffmpeg", "-i", ogg_path, wav_path])

        # Transcribe audio to text
        result = whisper_model.transcribe(wav_path)
        text = result['text']

        # Translate to English
        translated = translator.translate(text, dest='en')
        update.message.reply_text(f"Voice Translation: {translated.text}")

# Main function to start the bot
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, translate_text))
    dp.add_handler(MessageHandler(Filters.voice, handle_voice))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
