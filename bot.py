import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from openai import OpenAI

# ======================
# ENVIRONMENT VARIABLES
# ======================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing")

# ======================
# OPENAI CLIENT
# ======================
client = OpenAI(api_key=OPENAI_API_KEY)

# ======================
# TELEGRAM COMMANDS
# ======================
def start(update, context):
    update.message.reply_text(
        "🤖 Bot is online.\n"
        "Send a message and I’ll respond."
    )

def help_command(update, context):
    update.message.reply_text(
        "Just send a message.\n"
        "Later this will become an options bot."
    )

def handle_message(update, context):
    user_text = update.message.text

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_text
        )

        reply = response.output_text.strip()
        if not reply:
            reply = "I didn’t get a response. Try again."

        update.message.reply_text(reply)

    except Exception as e:
        print("ERROR:", e)
        update.message.reply_text(
            "⚠️ Error talking to OpenAI.\n"
            "Try again in a moment."
        )

# ======================
# BOT SETUP
# ======================
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(
    MessageHandler(Filters.text & ~Filters.command, handle_message)
)

print("🤖 Bot started and listening...")

updater.start_polling()
updater.idle()  # 🚨 DO NOT REMOVE
