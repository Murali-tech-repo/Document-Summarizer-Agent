
import os
import uuid

os.environ["TOKENIZERS_PARALLELISM"] = "false"

import chromadb
from sentence_transformers import SentenceTransformer

# =========================================
# CHROMADB SETUP
# =========================================

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)

# =========================================
# LIGHTWEIGHT EMBEDDING MODEL
# =========================================

embedding_model = SentenceTransformer(
    "paraphrase-MiniLM-L3-v2"
)

print("Model Loaded")

# =========================================
# STORE CHUNKS
# =========================================

def store_chunks(chunks):

    for chunk in chunks:

        embedding = embedding_model.encode(
            chunk,
            convert_to_numpy=True
        ).tolist()

        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[chunk],
            embeddings=[embedding]
        )

# =========================================
# SEARCH CHUNKS
# =========================================

def search_chunks(query, top_k=5):

    query_embedding = embedding_model.encode(
        query,
        convert_to_numpy=True
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]

