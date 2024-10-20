from transformers import AutoModel
import faiss
import os
import sys
import time
import sqlite3

from fetcher import fetcher

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "../processing"))
from sql import sql

RUN_ALL = -1
N_ROWS = 20000

class embeddings:
    def analyze(attrs: list[str], n_descriptions: int):
        if (n_descriptions > N_ROWS): n_descriptions = RUN_ALL
    
        data_folder = '../data/keywords'

        total_t = time.time()

        con = sqlite3.connect(sql.db_name)
        cursor = con.cursor()

        for attr in attrs: sql.add_score(cursor, attr)

        if os.name == 'posix': os.environ['TOKENIZERS_PARALLELISM'] = 'FALSE'
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
        model = AutoModel.from_pretrained('jinaai/jina-embeddings-v3', trust_remote_code=True)

        descriptions = fetcher.get_descriptions(cursor)

        denormalized: dict[str, list[tuple[float, str, str]]] = {}

        for attr in attrs:
            t = time.time()

            denormalized[attr] = []

            file_path = os.path.join(data_folder, f'{attr}.txt')
            
            with open(file_path, 'r') as input:
                phrases = input.read().lower().split("\n")
                embeddings = model.encode(phrases, task='classification')
                dimension = embeddings.shape[1]
                index = faiss.IndexFlatL2(dimension)
                index.add(embeddings)
                
                ds = [d.text for d in descriptions]
                selected_ds = ds if n_descriptions == RUN_ALL else ds[:n_descriptions]
                
                x = time.time()
                description_embeddings = model.encode(selected_ds)
                print(time.time() - x)

                for desc, emb in zip(descriptions, description_embeddings):
                    D, _ = index.search(emb.reshape(1, -1), k=1)
                    denormalized[attr].append((float(D[0][0]), desc.pk1, desc.pk2))

            print(f'{attr}: {(time.time() - t):.3f} seconds')

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

        print(f'\ntotal: {(time.time() - total_t):.3f} seconds\n')


if __name__ == '__main__':
    #region settings

    # which columns are we running the analysis on?
    # names must match a .txt file in ../data/keywords

    attrs = ['low', 'medium', 'high']

    # how many descriptions are we running? -1 to run all
    n_descriptions = 20

    #endregion

    embeddings.analyze(attrs, n_descriptions)