from google import genai

API_KEY = "AIzaSyCHJUYb81jU4mVxOk54xKtR-XbGDhg6ASM" 
client = genai.Client(api_key=API_KEY)

print("--- Listing Your Available Gemini Models ---")
try:
    # Simplified loop for the 2026 SDK
    for model in client.models.list():
        print(f"👉 {model.name}")
except Exception as e:
    print(f"❌ Error: {e}")