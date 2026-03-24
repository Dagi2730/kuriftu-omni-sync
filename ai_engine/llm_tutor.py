import os
from google import genai
    
def generate_hotel_response(user_query, room_matches):
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    # ... (your prompt code) ...
    prompt = f"""
    You are the lead digital concierge for Kuriftu Resort & Spa. 
    User Query: "{user_query}"
    Data found in our system: {room_matches}
    
    Instructions:
    1. Warm Ethiopian hospitality.
    2. Be specific to their query. Mention 'Kuriftu'. 
    3. If they mention leaving for an activity, suggest saving energy by syncing their room AC.
    Max 3 sentences.
    """

    try:
        response = client.models.generate_content(
            model='models/gemini-2.0-flash-lite', 
            contents=prompt
        )
        return response.text
    except Exception as e:
        # THIS IS THE MAGIC LINE:
        print(f"❌ GEMINI ERROR: {e}") 
        
        if room_matches:
            return f"Welcome to Kuriftu! I found a perfect room for two. How can I help further?"
        return "I'm having a bit of trouble reaching the concierge. Please try again in a moment!"