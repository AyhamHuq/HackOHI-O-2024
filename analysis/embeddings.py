from transformers import AutoModel
import faiss
import os
import sys
import time
from fetcher import fetcher
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "../processing"))
from sql import sql
sql.add_scores()

data_folder = '../data/keywords'

# directory check
script_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = os.getcwd()
assert current_dir == script_dir, (f"script must be run from {script_dir}")

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
model = AutoModel.from_pretrained('jinaai/jina-embeddings-v3', trust_remote_code=True)

# TODO: get data from database
descriptions = fetcher.get_descriptions()

for file in os.listdir(data_folder):
    t = time.time()

    file_path = os.path.join(data_folder, file)
    
    i = 0
    with open(file_path, 'r') as input:
        if i < 20:
            break
        i += 1
        phrases = input.read().lower().split("\n")
        embeddings = model.encode(phrases, task='classification')
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        descriptions_embeddings = model.encode(descriptions)

        for desc, embedding in zip(descriptions, descriptions_embeddings):
            D, I = index.search(embedding.reshape(1, -1), k=1)

            # D[0][0] to get distance, phrases[I[0][0]] to get matched phrase

            
            if "low" in file_path: print(D[0][0])#sql.update_low_sql(D[0][0])
            elif "medium" in file_path: print(D[0][0]) #sql.update_med_sql(D[0][0])
            elif "high" in file_path: print(D[0][0])#sql.update_high_sql(D[0][0])


    print(f'took {time.time() - t} seconds\n')
