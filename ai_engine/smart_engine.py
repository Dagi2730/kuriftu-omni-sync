import json
import os

def search_rooms_semantic(query, top_k=2):
    """
    Enhanced Search: Looks through both Rooms and Services 
    to provide the LLM with full resort context.
    """
    file_path = os.path.join(os.path.dirname(__file__), '..', 'rooms.json')
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Combine Rooms and Services into one searchable list
        all_options = []
        
        for r in data.get("rooms", []):
            all_options.append(f"ROOM: {r['name']} (${r['price']}). View: {r['view']}. {r['description']}")
            
        for s in data.get("services", []):
            all_options.append(f"SERVICE: {r['name']}. Hours: {s['hours']}. {s['description']}")

        query_lower = query.lower()
        
        # Simple but effective keyword matching for the demo
        # If you have time later, you can upgrade this to actual embeddings
        matches = [opt for opt in all_options if any(word in opt.lower() for word in query_lower.split())]
        
        # If no direct matches, return the first few items as general context
        return matches[:top_k] if matches else all_options[:top_k]

    except Exception as e:
        print(f"❌ SEARCH ERROR: {e}")
        return []