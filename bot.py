import random
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters

# Replace with your Telegram bot token
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Replace with your AI voice API key and base URL (e.g., ElevenLabs or Google TTS)
VOICE_API_URL = "https://api.elevenlabs.io/v1/text-to-speech/your_voice_id"
VOICE_API_KEY = "YOUR_VOICE_API_KEY"

# List of companies to pose as
COMPANIES = [
    "PayPal",
    "Amazon",
    "Walmart",
    "Netflix",
    "Apple"
]

# Generate a random 6-digit OTP
def generate_otp():
    return "".join(str(random.randint(0, 9)) for _ in range(6))

# Handle /start command
def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(company, callback_data=company.lower())] for company in COMPANIES]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Select a company to generate an OTP:", reply_markup=reply_markup)

# Handle company selection (e.g., /paypal, /amazon)
def select_company(update: Update, context: CallbackContext):
    query = update.callback_query
    company = query.data
    query.answer()
    otp = generate_otp()
    query.message.reply_text(
        f"Your {company} OTP is: **{otp}**\n\n"
        f"Use this to log into your account. Keep it secure!"
    )
    # Trigger AI voice command
    voice_text = f"Your {company} OTP is {otp}."
    voice_response = requests.post(
        VOICE_API_URL,
        headers={"Authorization": VOICE_API_KEY},
        json={"text": voice_text}
    )
    if voice_response.status_code == 200:
        with open("otp_voice.mp3", "wb") as f:
            f.write(voice_response.content)
        context.bot.send_voice(chat_id=query.message.chat_id, voice=open("otp_voice.mp3", "rb"))
    else:
        context.bot.send_message(chat_id=query.message.chat_id, text="Failed to generate voice command.")

# Handle /2fa command
def two_factor_auth(update: Update, context: CallbackContext):
    update.message.reply_text("Triggering 2FA voice command...")
    # Generate a random OTP
    otp = generate_otp()
    # Create a voice message
    voice_text = f"2FA code: {otp}. Verify your identity."
    voice_response = requests.post(
        VOICE_API_URL,
        headers={"Authorization": VOICE_API_KEY},
        json={"text": voice_text}
    )
    if voice_response.status_code == 200:
        with open("2fa_voice.mp3", "wb") as f:
            f.write(voice_response.content)
        context.bot.send_voice(chat_id=update.message.chat_id, voice=open("2fa_voice.mp3", "rb"))
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Failed to generate 2FA voice command.")

# Handle other options (e.g., /help, /settings)
def handle_options(update: Update, context: CallbackContext):
    update.message.reply_text("Options:\n"
                              "/start - Start the bot\n"
                              "/2fa - Trigger 2FA voice command\n"
                              "/otp - Generate OTP manually\n"
                              "/help - List all commands")

# Main function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(select_company))
    dp.add_handler(CommandHandler("2fa", two_factor_auth))
    dp.add_handler(CommandHandler("otp", lambda u, c: u.message.reply_text(f"Your OTP is: {generate_otp()}")))
    dp.add_handler(CommandHandler("help", handle_options))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
