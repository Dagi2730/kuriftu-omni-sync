import os
from groq import Groq

def generate_hotel_response(user_query, room_matches):
    """
    MULTI-INTENT ENGINE: 
    Handles information requests + Hardware triggers simultaneously.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return "Welcome to Kuriftu! AI Syncing..."

    client = Groq(api_key=api_key)
    context_str = "\n".join(room_matches) if room_matches else "General Resort Info"

    # THE BRAIN: Specifically instructed to handle 'Double Intents'
    system_instruction = (
        "You are the Kuriftu Omni-Sync AI Concierge. You are highly intelligent. "
        "STRICT OPERATIONAL RULES:\n"
        "1. INFORMATION: If the guest asks about prices/rooms/spa, give accurate data from the context.\n"
        "2. HARDWARE TRIGGER: If the guest mentions leaving (spa, pool, tour, checkout), "
        "you MUST append the tag [ACTION:POWER_OFF] at the end of your message.\n"
        "3. MULTI-INTENT: If they ask a question AND mention leaving (e.g., 'How much is spa? I'm going there now'), "
        "answer the question FIRST, then confirm you are syncing their room, then add the tag.\n"
        "4. TONE: Warm, Ethiopian hospitality, professional, and under 3 sentences."
        "5. DO NOT say 'Welcome to Kuriftu' or 'How can I assist you' if the guest is already in the middle of a booking or asking a follow-up question. Just give the answer.\n"
        "6. LANGUAGE MATCH: If the guest speaks Amharic, reply in Amharic. If they speak English, reply in English.\n"
        "7. TONE: Warm, Ethiopian hospitality (ሰላም). Under 3 sentences.\n"
        "8. DATA ACCURACY: Use the provided JSON data for prices ($500) and details.\n"
        "9. HARDWARE TAGS: Even if you speak Amharic, you MUST keep the tag [ACTION:POWER_OFF] exactly in English at the end of the message if the guest is leaving."
        
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": f"DATA: {context_str}\n\nGUEST: {user_query}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3 # Lower temperature for higher reliability on tags
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"❌ GROQ ERROR: {e}")
        return "I've processed your request. Have a wonderful time! [ACTION:POWER_OFF]"