from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Step 1: Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 2: Define high-energy reference sentences
high_energy_phrases = [
    "Explosion in the factory", 
    "Rapid chemical reaction", 
    "High-speed collision"
]

# Step 3: Encode reference phrases
high_energy_embeddings = model.encode(high_energy_phrases)

# Step 4: Create FAISS index
dimension = high_energy_embeddings.shape[1]  # Dimensions of the embeddings
index = faiss.IndexFlatL2(dimension)  # Using L2 distance (cosine similarity can also be used)
index.add(high_energy_embeddings)  # Add the high-energy embeddings to the index

# Step 5: New description to classify
new_description = "There was a huge explosion in the factory with many members present"
new_description_embedding = model.encode([new_description])

# Step 6: Perform similarity search
D, I = index.search(new_description_embedding, k=1)  # Find the top 1 closest match

# Step 7: Output similarity score
print(f"Similarity score: {D[0][0]}")  # Lower distance means higher similarity
