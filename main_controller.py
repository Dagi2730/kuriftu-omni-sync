import os
import sys
import csv
from datetime import datetime

# Ensure local modules are accessible
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_engine.smart_engine import search_rooms_semantic
from ai_engine.llm_tutor import generate_hotel_response

# --- 1. SIGNALS ---

def trigger_power_sync(status, source="MANUAL"):
    print("\n" + "⚡" * 35)
    print(f"OMNI-SYNC [ENERGY]: Targeting {source}")
    print(f"ACTION: Room Power -> {status}")
    print("⚡" * 35 + "\n")

def trigger_kitchen_sync(guest_id, action):
    print("\n" + "🥗" * 35)
    print(f"OMNI-SYNC [KITCHEN]: {guest_id} {action}")
    print(f"IMPACT: Reducing buffet waste.")
    print("🥗" * 35 + "\n")

# --- 2. DATA LOGGING ---

def save_booking_to_csv(user_identity, user_input):
    root_dir = os.getcwd() 
    csv_path = os.path.join(root_dir, 'bookings.csv')
    
    try:
        file_exists = os.path.isfile(csv_path)
        with open(csv_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Timestamp', 'Identity', 'Request/Intent'])
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, user_identity, user_input])
        print(f"✅ LOG SUCCESS: Recorded lead for {user_identity}")
    except Exception as e:
        print(f"❌ CSV ERROR: {e}")

# --- 3. MAIN LOGIC ---

def get_omni_sync_response(user_input, user_identity="Guest"):
    try:
        input_lower = user_input.lower()

        # A. FOOD WASTE LOGIC
        if any(word in input_lower for word in ["sleep in", "no breakfast", "skip breakfast"]):
            trigger_kitchen_sync(user_identity, "SKIPPING BREAKFAST")

        # B. LEAD CAPTURE
        booking_keywords = ["book", "reserve", "want", "stay", "villa", "room", "price"]
        if any(word in input_lower for word in booking_keywords):
             save_booking_to_csv(user_identity, user_input)

        # C. AI RESPONSE
        matches = search_rooms_semantic(user_input, top_k=2)
        raw_message = generate_hotel_response(user_input, matches)
        
        # D. ENERGY LOGIC
        if "[ACTION:POWER_OFF]" in raw_message:
            trigger_power_sync("OFF", source=user_identity)
            return raw_message.replace("[ACTION:POWER_OFF]", "").strip()
        
        return raw_message
        
    except Exception as e:
        print(f"❌ CONTROLLER ERROR: {e}")
        return "Welcome to Kuriftu! We are optimizing our systems for you."