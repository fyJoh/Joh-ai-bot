import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from openai import OpenAI

# --- Get secrets from Railway ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing")

# --- OpenAI client ---
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Telegram handlers ---
def start(update, context):
    update.message.reply_text(
        "👋 Hi! I'm alive.\nSend me a message and I'll reply."
    )

def handle_message(update, context):
    user_text = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_text},
            ],
        )

        reply = response.choices[0].message.content
        update.message.reply_text(reply)

    except Exception as e:
        update.message.reply_text("⚠️ Something went wrong.")
        print(e)

# --- Start bot ---
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

print("🤖 Bot started and listening...")

updater.start_polling()
updater.idle()  # 🚨 THIS KEEPS THE BOT RUNNING (DO NOT REMOVE)
