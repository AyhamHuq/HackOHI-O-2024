from transformers import AutoModel
import faiss
import os
import sys
import time
from fetcher import fetcher
import sqlite3

#region settings

# which columns are we running the analysis on?
# names must match a .txt file in ../data/keywords
attrs = ['low', 'medium', 'high']

# are we running on the entire dataset?
entire_dataset = False

# if we're not running everything, how many descriptions are we running
n_descriptions = 30

#endregion

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "../processing"))
from sql import sql

data_folder = '../data/keywords'

# directory check
script_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = os.getcwd()
assert current_dir == script_dir, (f"script must be run from {script_dir}")

total_t = time.time()

con = sqlite3.connect(sql.db_name)
cursor = con.cursor()

for attr in attrs: sql.add_score(cursor, attr)

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
model = AutoModel.from_pretrained('jinaai/jina-embeddings-v3', trust_remote_code=True)

descriptions = fetcher.get_descriptions(cursor)

# for file in os.listdir(data_folder):
for attr in attrs:
    t = time.time()

    file_path = os.path.join(data_folder, f'{attr}.txt')
    
    with open(file_path, 'r') as input:
        phrases = input.read().lower().split("\n")
        embeddings = model.encode(phrases, task='classification')
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        for (i, desc) in enumerate(descriptions):
            if i >= n_descriptions and not entire_dataset: break

            description_embedding = model.encode(desc.text)
            D, I = index.search(description_embedding.reshape(1, -1), k=1)

            cursor.execute(sql.update_score(attr), (float(D[0][0]), desc.pk1, desc.pk2))

    print(f'{attr} took {time.time() - t} seconds')

con.commit()
con.close()

print(f'\ntotal time: {time.time() - total_t} seconds\n')