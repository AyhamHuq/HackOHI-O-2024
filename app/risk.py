from sentence_transformers import SentenceTransformer
import os
import sys
import faiss
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../analysis'))

from fetcher import fetcher

def get_risk(desc: str) -> str:
    attrs = ['low', 'medium', 'high']

    filtered_desc = fetcher.filter_stop_words(desc)

    model = SentenceTransformer("jxm/cde-small-v1", trust_remote_code=True)
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

    denormalized = []

    for attr in attrs:
        file_path = os.path.join('../data/keywords', f'{attr}.txt')

        with open(file_path, 'r') as input:
            phrases = input.read().lower().split("\n")
            embeddings = model.encode(phrases, convert_to_tensor=True)
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            embeddings_cpu = embeddings.cpu().detach().numpy()

            # Add the embeddings to the FAISS index
            index.add(np.ascontiguousarray(embeddings_cpu, dtype='float32'))
            
            description_embedding = model.encode(filtered_desc)
            D, _ = index.search(description_embedding.reshape(1, -1), k=1)

            denormalized.append(float(D[0][0]))

    return attrs[denormalized.index(min(denormalized))]

