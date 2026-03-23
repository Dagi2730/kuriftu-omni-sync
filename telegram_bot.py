import logging
import csv
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from main_controller import get_omni_sync_response

# 1. YOUR TOKENS
TELEGRAM_TOKEN = '8622510456:AAFY5VCbdj5hwCJxtyVZnQznxjAoEYSBV08'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def log_booking_lead(user_name, user_id, query):
    """Saves potential customer interest to a CSV file"""
    file_exists = False
    try:
        with open('bookings.csv', 'r') as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open('bookings.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Add header if it's a new file
        if not file_exists:
            writer.writerow(['Date', 'User Name', 'Telegram ID', 'Interest'])
        
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            user_name,
            user_id,
            query
        ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🏨 *Welcome to Kuriftu Omni-Sync!* 🇪🇹\n\n"
        "I am your AI Concierge. How can I help you find a room today?"
    )
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text
    user = update.message.from_user
    
    # 2. LOG THE LEAD (Save to CSV)
    log_booking_lead(user.full_name, user.id, user_query)
    print(f"📈 New Lead Logged: {user.full_name} interested in '{user_query}'")

    await update.message.reply_chat_action(action="typing")
    
    # 3. GET AI RESPONSE
    response = get_omni_sync_response(user_query)
    await update.message.reply_text(response)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🚀 Kuriftu Bot is LIVE & Logging Leads!")
    app.run_polling()