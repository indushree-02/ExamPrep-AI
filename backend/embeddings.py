import os

from sentence_transformers import SentenceTransformer
from database import get_collection

DATA_FOLDER = "../data"

model = SentenceTransformer("all-MiniLM-L6-v2")


def split_text(text, chunk_size=500):
    """
    Split long text into smaller chunks.
    """

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])

    return chunks


def build_database():

    collection = get_collection()

    # Remove previous data
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    current_id = 0

    for filename in os.listdir(DATA_FOLDER):

        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(DATA_FOLDER, filename)

        with open(filepath, "r", encoding="utf-8") as file:

            text = file.read()

        chunks = split_text(text)

        for chunk in chunks:

            embedding = model.encode(chunk).tolist()

            collection.add(
                ids=[str(current_id)],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[
                    {
                        "source": filename
                    }
                ]
            )

            current_id += 1

    return current_id