from transformers import AutoModel
import faiss
import os
import sys
import time
from fetcher import fetcher
import sqlite3

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "../processing"))
from sql import sql

data_folder = '../data/keywords'

# directory check
script_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = os.getcwd()
assert current_dir == script_dir, (f"script must be run from {script_dir}")

con = sqlite3.connect(sql.db_name)
cursor = con.cursor()

attrs = ['low', 'medium', 'high']
for attr in attrs: sql.add_score(cursor, attr)

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
model = AutoModel.from_pretrained('jinaai/jina-embeddings-v3', trust_remote_code=True)

descriptions = fetcher.get_descriptions(cursor)

# for file in os.listdir(data_folder):
for file in attrs:
    t = time.time()

    file_path = os.path.join(data_folder, f'{file}.txt')
    
    with open(file_path, 'r') as input:
        phrases = input.read().lower().split("\n")
        embeddings = model.encode(phrases, task='classification')
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)

        i = 0
        # for desc, embedding in zip(descriptions, descriptions_embeddings):
        for desc in descriptions:
            if i > 20:
                break
            i += 1

            description_embedding = model.encode(desc.text)
            D, I = index.search(description_embedding.reshape(1, -1), k=1)

            print(D[0][0])
            cursor.execute(sql.update_score(file), (D[0][0], desc.pk1, desc.pk2))




    print(f'took {time.time() - t} seconds\n')

con.commit()
con.close()