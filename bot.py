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
# COMMANDS
# ======================
def start(update, context):
    update.message.reply_text(
        "Hey I’m Joh, what’s up? 😎"
    )

def handle_message(update, context):
    user_text = update.message.text

    try:
        # This is the MOST reliable OpenAI call
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_text
        )

        reply = response.output_text

        if not reply or reply.strip() == "":
            reply = "I didn’t get a response. Try again."

        update.message.reply_text(reply)

    except Exception as e:
        print("OPENAI ERROR:", e)
        update.message.reply_text(
            "⚠️ Something went wrong.\n"
            "If this keeps happening, contact @johhek on Instagram."
        )

# ======================
# BOT SETUP
# ======================
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(
    MessageHandler(Filters.text & ~Filters.command, handle_message)
)

print("🤖 Bot started and listening...")

updater.start_polling()
updater.idle()
