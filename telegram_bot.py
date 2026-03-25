import os
import logging
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Import your custom logic
from main_controller import get_omni_sync_response

# --- 1. CONFIG & UTILS ---
load_dotenv() # Crucial: Loads your .env file
logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHECKIN_FILE = os.path.join(BASE_DIR, "check_in.json")

def get_guest_data(telegram_id):
    """Checks if the user is already registered in a room"""
    if os.path.exists(CHECKIN_FILE):
        with open(CHECKIN_FILE, 'r') as f:
            try:
                data = json.load(f)
                return data.get(str(telegram_id))
            except: return None
    return None

def save_guest_data(telegram_id, room, last_name):
    """Saves new registration to the JSON file"""
    data = {}
    if os.path.exists(CHECKIN_FILE):
        with open(CHECKIN_FILE, 'r') as f:
            try: data = json.load(f)
            except: data = {}
    
    data[str(telegram_id)] = {"room": room, "name": last_name}
    with open(CHECKIN_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- 2. COMMAND HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    await update.message.reply_text(
        f"Selam {user_name}! 🏨 Welcome to Kuriftu Resort & Spa.\n\n"
        "To provide secure service, please register your room.\n"
        "Format: [Room Number], [Last Name]\n"
        "Example: 302, Andargachew"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_query = update.message.text
    telegram_id = update.message.from_user.id
    
    # Check if user is registered
    guest_info = get_guest_data(telegram_id)

    # A. REGISTRATION LOGIC
    if not guest_info:
        if "," in user_query:
            try:
                room_num, last_name = [x.strip() for x in user_query.split(",")]
                save_guest_data(telegram_id, room_num, last_name)
                await update.message.reply_text(f"✅ Secure Sync Established! Welcome to Room {room_num}, {last_name}. How can I assist you today?")
                return
            except: pass
        
        await update.message.reply_text("🏨 Please register first. Send your: Room Number, Last Name (e.g., 302, Jhon)")
        return

    # B. AI PROCESSING
    await update.message.reply_chat_action(action="typing")
    try:
        # We pass the Room Number as the 'Identity' to the controller
        target_identity = f"Guest in Room {guest_info['room']}"
        response = get_omni_sync_response(user_query, target_identity)
        await update.message.reply_text(response)
    except Exception as e:
        print(f"❌ BOT ERROR: {e}")
        await update.message.reply_text("🏨 Kuriftu: System syncing... Please try again in a moment!")

if __name__ == '__main__':
    print("🔍 Initializing Kuriftu Omni-Sync...")
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    if not TOKEN:
        print("❌ ERROR: TELEGRAM_TOKEN not found!")
        sys.exit(1)

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🚀 KURIFTU SECURE OMNI-SYNC IS LIVE!")
    app.run_polling(drop_pending_updates=True)