from google import genai

API_KEY = "AIzaSyCHJUYb81jU4mVxOk54xKtR-XbGDhg6ASM" 
client = genai.Client(api_key=API_KEY)

def generate_hotel_response(user_query, room_matches):
    # This is the dynamic prompt that changes based on what the user asks!
    prompt = f"""
    You are the lead digital concierge for Kuriftu Resort & Spa. 
    User Query: "{user_query}"
    Data found in our system: {room_matches}
    
    Instructions:
    1. Warm Ethiopian hospitality.
    2. Be specific to their query: if they ask for a date, suggest one.
    3. Mention 'Kuriftu'. Max 3 sentences.
    """
    
    try:
        # Use the 'Lite' version - it's much more reliable on Free Tier
        response = client.models.generate_content(
            model='models/gemini-2.0-flash-lite', 
            contents=prompt
        )
        return response.text
    except Exception as e:
        # If it's a quota error, we show a 'loading' message
        if "429" in str(e):
            return "🏨 Kuriftu: Our systems are a bit busy! Please wait 15 seconds and ask again."
        return f"Front Desk Error: {str(e)}"