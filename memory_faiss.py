import faiss
import os
from sentence_transformers import SentenceTransformer
import numpy as np

MODEL = SentenceTransformer("all-MiniLM-L6-v2")
INDEX_PATH = "data/index.faiss"

def create_index(texts):
    vectors = MODEL.encode(texts)
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)
    faiss.write_index(index, INDEX_PATH)

def search_index(query, texts, k=3):
    if not os.path.exists(INDEX_PATH) or len(texts) == 0:
        return []

    index = faiss.read_index(INDEX_PATH)
    query_vector = MODEL.encode([query])
    distances, indices = index.search(query_vector, k)
    return [texts[i] for i in indices[0] if i < len(texts)]
