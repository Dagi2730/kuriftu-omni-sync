import pandas as pd
import json
import os
from sentence_transformers import SentenceTransformer, util
import torch

# 1. Setup paths to be "Environment Proof"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "mock_hotel_data.json")

print("--- Initializing Kuriftu Semantic AI ---")

# 2. Load the Embedding Model (The 'Brain')
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_data():
    # Load the JSON file
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Could not find {DATA_PATH}. Make sure the JSON is in the root folder!")
        
    with open(DATA_PATH, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data['rooms'])
    
    # 3. Data Enrichment: This helps the AI understand 'Vibes'
    def enrich_description(row):
        desc = f"This is a {row['type']} featuring a {row['view']} view for ${row['price']}. "
        
        # Add 'Luxury' keywords based on price
        if row['price'] > 300:
            desc += "An ultra-luxury, high-end executive suite with premium finishes. "
        elif row['price'] > 200:
            desc += "A comfortable, high-quality deluxe stay. "
            
        # Add 'Spa/Relaxation' keywords based on amenities
        if "Spa Access" in row['amenities'] or "Jacuzzi" in row['amenities']:
            desc += "Includes world-class spa facilities, deep-tissue massage options, and total relaxation. "
        
        # Add 'Nature' keywords
        if "Garden" in row['view'] or "Lake" in row['view']:
            desc += "Perfect for nature lovers seeking a peaceful, scenic retreat. "
            
        return desc

    df['combined_info'] = df.apply(enrich_description, axis=1)
    return df

# 4. The Semantic Search Function
def search_rooms_semantic(user_query, top_k=3):
    df = load_data()
    
    # Transform rooms and query into math vectors (Embeddings)
    room_embeddings = model.encode(df['combined_info'].tolist(), convert_to_tensor=True)
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    
    # Calculate Similarity (Cosine Similarity)
    cosine_scores = util.cos_sim(query_embedding, room_embeddings)[0]
    
    # Grab the top matches using PyTorch
    top_results = torch.topk(cosine_scores, k=top_k)
    
    results = []
    for score, idx in zip(top_results[0], top_results[1]):
        room = df.iloc[idx.item()].to_dict()
        # Format the score as a percentage for humans to read
        room['match_score'] = f"{float(score):.2%}"
        results.append(room)
        
    return results

# 5. Execution Block
if __name__ == "__main__":
    # Test it with a natural, human sentence
    test_query = "I'm looking for a luxury experience with a spa feel"
    print(f"Searching for: {test_query}...")
    
    try:
        matches = search_rooms_semantic(test_query) 
        
        print("\n--- Best Matches Found ---")
        for m in matches:
            print(f"[{m['match_score']}] Room {m['id']}: {m['type']} - {m['view']} view (${m['price']})")
    except Exception as e:
        print(f"An error occurred: {e}")