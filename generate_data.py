import json
import random

# Configuration for Kuriftu Resort
room_types = {
    "Presidential Suite": {"price_range": (400, 600), "views": ["Lake", "Mountain"]},
    "Lakeside Bungalow": {"price_range": (250, 400), "views": ["Lake"]},
    "Garden Room": {"price_range": (150, 250), "views": ["Garden", "Forest"]},
    "Standard Room": {"price_range": (100, 180), "views": ["Courtyard", "Garden"]}
}

statuses = ["available", "occupied", "cleaning", "maintenance"]

def generate_rooms(count=200):
    rooms = []
    for i in range(1, count + 1):
        # Pick a random type
        r_type = random.choice(list(room_types.keys()))
        
        room = {
            "id": 100 + i,
            "type": r_type,
            "view": random.choice(room_types[r_type]["views"]),
            "status": random.choices(statuses, weights=[60, 25, 10, 5])[0], # 60% are available
            "price": random.randint(*room_types[r_type]["price_range"]),
            "amenities": random.sample(["WiFi", "Mini-bar", "AC", "Balcony", "Jacuzzi"], k=random.randint(2, 4))
        }
        rooms.append(room)
    return rooms

# Wrap it in the full resort structure
full_data = {
    "resort_name": "Kuriftu Resort & Spa",
    "location": "Bishoftu, Ethiopia",
    "rooms": generate_rooms(200),
    "services": ["Spa", "Swimming Pool", "Kayaking", "Cinema", "Gym"],
    "restaurants": ["The Lakeview Grill", "Traditional Hut"]
}

# Save to your existing mock_hotel_data.json
with open('ai-engine/mock_hotel_data.json', 'w') as f:
    json.dump(full_data, f, indent=2)

print("Successfully generated 200 rooms in ai-engine/mock_hotel_data.json!")