import os
import json

# We'll use a mock function for now so you don't need an API key immediately
# But this is exactly where your LangChain or Google Generative AI code will go!

def process_guest_request(user_input):
    """
    Simulates an AI agent processing a hotel guest's request.
    In a real app, this would call the Gemini API.
    """
    print(f"--- AI Engine Processing: '{user_input}' ---")
    
    # Mocking the AI's "Structured Output"
    structured_data = {
        "intent": "room_service_request",
        "items": ["extra towels"],
        "room_feature_preference": "lake_view",
        "urgency": "medium"
    }
    
    return json.dumps(structured_data, indent=2)

if __name__ == "__main__":
    sample_request = "I'd love a room with a lake view, and could you bring up some extra towels?"
    result = process_guest_request(sample_request)
    print(result)