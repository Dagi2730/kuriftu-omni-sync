import os
import logging
import csv
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from main_controller import get_omni_sync_response

# --- ROBUST ENV LOADER ---
# This ensures it finds the .env file in the root folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

try:
    with open(ENV_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key] = value.strip()
    
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    if TELEGRAM_TOKEN:
        print(f"✅ Integration Ready: Token loaded (Starts with {TELEGRAM_TOKEN[:5]})")
except Exception as e:
    print(f"❌ Critical Error loading .env: {e}")

# Setup Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def log_booking_lead(user_name, user_id, query):
    file_path = os.path.join(BASE_DIR, 'bookings.csv')
    file_exists = os.path.isfile(file_path)
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Date', 'User Name', 'Telegram ID', 'Interest'])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), user_name, user_id, query])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "🏨 *Welcome to Kuriftu Omni-Sync!* 🇪🇹\n\nI am your AI Concierge. How can I help you find a room today?"
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text
    user = update.message.from_user
    log_booking_lead(user.full_name, user.id, user_query)
    
    await update.message.reply_chat_action(action="typing")
    
    try:
        response = get_omni_sync_response(user_query)
        await update.message.reply_text(response)
    except Exception as e:
        print(f"Integration Error: {e}")
        await update.message.reply_text("I'm having a bit of trouble reaching the concierge. Please try again in a moment!")

if __name__ == '__main__':
    if not TELEGRAM_TOKEN:
        print("❌ ABORT: No TELEGRAM_TOKEN found. Check .env file.")
    else:
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        print("🚀 Kuriftu Bot is LIVE & Ready for Team Integration!")
        app.run_polling()