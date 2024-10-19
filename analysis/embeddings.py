from sentence_transformers import SentenceTransformer
import faiss
import os
import time

t = time.time()

# directory check
script_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = os.getcwd()
assert current_dir == script_dir, (f"script must be run from {script_dir}")

# Step 1: Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 2: Define high-energy reference sentences
with open('../data/high_energy.txt') as input:
    phrases = input.read().split("\n")

# Step 3: Encode reference phrases
high_energy_embeddings = model.encode(phrases)

# Step 4: Create FAISS index
dimension = high_energy_embeddings.shape[1]  # Dimensions of the embeddings
index = faiss.IndexFlatL2(dimension)  # Using L2 distance (cosine similarity can also be used)
index.add(high_energy_embeddings)  # Add the high-energy embeddings to the index

# Step 5: New description to classify
new_descriptions = [
    "There was a huge explosion in the factory with many members present",
    '[NAME] tender was not wearing his Hardhat. I recommended they discuss PPE use during the after lunch briefing.',
    'No [NAME] version available. [NAME] went over briefing with us. Explained the need for and purpose of [NAME] briefing. Need more detail on ATE fire briefing; no assignments, water source, or humidity.',
    'Three of the four [NAME] members were not wearing hard hats. The [NAME] Lead was provided some coaching on this, and agreed that they should have had hard hats on, while completing the task they were working on.',
    '[NAME] member was observed working without safety glasses. I spoke to and coached the team member about the importance of proper PPE. The matter was corrected. PPE Required [NAME] - T & C 8. 1. 1, 8. 1. 3, 8. 1. 6, 8. 3. 1 ( [NAME] Protection )',
    '[NAME] rail blocked by blanket container, had crew remove and spoke to them importance on three points contact, clutter in belly of truck at entrance, coached and corrected',
    '[NAME] needed flagger due to curve and being on a double yellow, they only had work area ahead sign out and traffic cones were not the kind with the reflective tape, which are required. I did have crews move due to not having the proper signage, cones, or flaggers.',
    'PJB was missing upon my arrival. [NAME] was unsure what happened to it, but assured myself that it was completed.',
    '[NAME] had a good briefing except for a good location to provide to emergency responders. I coached the crew on the importance of having a location / address easily available if needed.',
    'Briefing was given, but the electronic tablet when refreshed deleted the briefing, so the crew re - briefed me, but wouldn\'t show up on the tablet.'
]
new_descriptions_embeddings = model.encode(new_descriptions)

# Step 6: Perform similarity search

for desc, embedding in zip(new_descriptions, new_descriptions_embeddings):
    D, I = index.search(embedding.reshape(1, -1), k=1)  # Find the top 1 closest match
    # Step 8: Output similarity score and corresponding phrase
    print(f"Description: '{desc}'")
    print(f"Similarity score: {D[0][0]}")  # Lower distance means higher similarity
    print(f"Matched phrase: '{phrases[I[0][0]]}'\n")  # Output the matched high-energy phrase


print(time.time() - t)