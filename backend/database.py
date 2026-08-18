import chromadb

DB_PATH = "vector_store"
COLLECTION_NAME = "exam_prep"

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)

def get_collection():
    return collection