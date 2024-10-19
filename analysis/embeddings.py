from sentence_transformers import SentenceTransformer
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
#attrs = ['low', 'medium', 'high']
#attrs = ['traffic', 'fire', 'electrical', 'fall']
attrs = ['ppe', 'documentation', 'equipment']

# are we running on the entire dataset?
entire_dataset = False

# if we're not running everything, how many descriptions are we running
n_descriptions = 100

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
model = SentenceTransformer("jxm/cde-small-v1", trust_remote_code=True)
#model = AutoModel.from_pretrained('jinaai/jina-embeddings-v3', trust_remote_code=True)

descriptions = fetcher.get_descriptions(cursor)

denormalized: dict[str, list[tuple[float, str, str]]] = {}

for attr in attrs:
    t = time.time()

    denormalized[attr] = []

    file_path = os.path.join(data_folder, f'{attr}.txt')
    
    with open(file_path, 'r') as input:
        phrases = input.read().lower().split("\n")
        #embeddings = model.encode(phrases, task='classification')
        embeddings = model.encode(phrases, convert_to_tensor=True)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        for (i, desc) in enumerate(descriptions):
            if i >= n_descriptions and not entire_dataset: break

            description_embedding = model.encode(desc.text)
            D, I = index.search(description_embedding.reshape(1, -1), k=1)

            denormalized[attr].append((float(D[0][0]), desc.pk1, desc.pk2))

    print(f'{attr} took {time.time() - t} seconds')

lists: list[list[tuple[float, str, str]]] = list(denormalized.values())

update_commands = [sql.update_score(attr) for attr in attrs]

for t in zip(*lists):
    total = sum(inner_tuple[0] for inner_tuple in t)

    for (command, inner_tuple) in zip(update_commands, t):
        denorm, pk1, pk2 = inner_tuple
        normalized = denorm / total
        cursor.execute(command, (normalized, pk1, pk2))
    
con.commit()
con.close()

print(f'\ntotal time: {time.time() - total_t} seconds\n')