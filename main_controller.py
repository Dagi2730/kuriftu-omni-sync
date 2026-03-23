import sys
import os

# This tells Python to look in the current folder for our 'ai_engine' module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_engine.smart_engine import search_rooms_semantic
from ai_engine.llm_tutor import generate_hotel_response

def get_omni_sync_response(user_input):
    print(f"--- Processing Query: {user_input} ---")
    
    # 1. Search the 'Facts'
    matches = search_rooms_semantic(user_input, top_k=3)
    
    # 2. Send to Gemini
    final_reply = generate_hotel_response(user_input, matches)
    
    return final_reply

if __name__ == "__main__":
    sample_query = "I want a quiet place for a honeymoon with a nice view"
    print("\n--- AI Response ---")
    print(get_omni_sync_response(sample_query))