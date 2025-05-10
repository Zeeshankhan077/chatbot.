import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from functools import lru_cache

EMBEDDING_PATH = os.path.join(os.path.dirname(__file__), 'embeddings/index.faiss')
METADATA_PATH = os.path.join(os.path.dirname(__file__), 'embeddings/metadata.pkl')

# Lazy loading of model and index
_model = None
_index = None
_metadata = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def get_index():
    global _index
    if _index is None:
        _index = faiss.read_index(EMBEDDING_PATH)
    return _index

def get_metadata():
    global _metadata
    if _metadata is None:
        with open(METADATA_PATH, "rb") as f:
            _metadata = pickle.load(f)
    return _metadata

@lru_cache(maxsize=1000)
def retrieve_context(user_input, k=5):
    model = get_model()
    index = get_index()
    metadata = get_metadata()
    
    embedding = model.encode([user_input])
    distances, indices = index.search(np.array(embedding).astype("float32"), k)
    return [metadata[i] for i in indices[0]]