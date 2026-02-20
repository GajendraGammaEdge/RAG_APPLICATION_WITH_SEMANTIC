from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
load_dotenv()

EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")
embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)


def get_embedding(text):
    return embedding_model.encode(text).tolist()
