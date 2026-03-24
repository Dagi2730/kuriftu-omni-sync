import sys
import os

# Ensure the root directory is in the path for module imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from ai_engine.smart_engine import search_rooms_semantic
from ai_engine.llm_tutor import generate_hotel_response

def get_omni_sync_response(user_input):
    print(f"--- Processing Query: {user_input} ---")
    
    # 1. Search Local Semantic Database
    matches = search_rooms_semantic(user_input, top_k=3)
    
    # 2. Generate the AI Response
    final_reply = generate_hotel_response(user_input, matches)
    
    return final_reply