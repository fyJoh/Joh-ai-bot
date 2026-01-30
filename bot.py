import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from openai import OpenAI

# ======================
# ENV VARIABLES
# ======================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

if not OPENAI_API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY")

# ======================
# OPENAI CLIENT
# ======================
client = OpenAI(api_key=OPENAI_API_KEY)

# ======================
# COMMANDS
# ======================
def start(update, context):
    update.message.reply_text(
        "🤖 Bot is online.\n"
        "Send any message and I will reply."
    )

def help_command(update, context):
    update.message.reply_text(
        "Just send text.\n"
        "This bot uses OpenAI to respond."
    )

def handle_message(update, context):
    user_text = update.message.text

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "You are a helpful, friendly assistant. "
                "Answer clearly and concisely."
            ),
            input=user_text
        )

        reply = response.output_text

        if not reply:
            reply = "No response received. Try again."

        update.message.reply_text(reply)

    except Exception as e:
        print("OPENAI ERROR:", e)
        update.message.reply_text(str(e))


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
updater.idle()
