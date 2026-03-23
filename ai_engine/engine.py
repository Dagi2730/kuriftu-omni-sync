import json
import os

def load_hotel_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "mock_hotel_data.json")
    with open(file_path, 'r') as file:
        return json.load(file)

def smart_sync_engine(query):
    """
    This is the 'Brain'. It filters the 200 rooms based on 
    keywords in the guest's request.
    """
    data = load_hotel_data()
    all_rooms = data['rooms']
    query = query.lower()
    
    # 1. Start with all available rooms
    matches = [r for r in all_rooms if r['status'] == 'available']
    
    # 2. Filter by View
    if "lake" in query:
        matches = [r for r in matches if r['view'] == 'Lake']
    elif "garden" in query:
        matches = [r for r in matches if r['view'] == 'Garden']
        
    # 3. Filter by Amenities (Jacuzzi, WiFi, etc.)
    if "jacuzzi" in query:
        matches = [r for r in matches if "Jacuzzi" in r['amenities']]
    if "balcony" in query:
        matches = [r for r in matches if "Balcony" in r['amenities']]

    # 4. Filter by Price (Budget logic)
    if "cheap" in query or "budget" in query:
        matches = [r for r in matches if r['price'] < 200]
    elif "luxury" in query or "expensive" in query:
        matches = [r for r in matches if r['price'] > 400]

    return matches

if __name__ == "__main__":
    # Test it with a complex request!
    test_query = "I want a cheap room with a garden view"
    results = smart_sync_engine(test_query)
    
    print(f"\n--- Kuriftu AI Search: '{test_query}' ---")
    print(f"Found {len(results)} matches.")
    for res in results[:3]: # Show first 3 matches
        print(f"- Room {res['id']}: {res['type']} (${res['price']}) - View: {res['view']}")