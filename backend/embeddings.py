import os

from sentence_transformers import SentenceTransformer
from database import get_collection

# Folder containing study material
DATA_FOLDER = "../data"

# Load embedding model (loads only once)
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_documents():
    """
    Read all text files from the data folder.
    """

    documents = []

    for filename in os.listdir(DATA_FOLDER):

        if filename.endswith(".txt"):

            path = os.path.join(DATA_FOLDER, filename)

            with open(path, "r", encoding="utf-8") as file:
                text = file.read()

            documents.append({
                "filename": filename,
                "content": text
            })

    return documents


def split_documents(documents):
    """
    Split documents into meaningful chunks.
    """

    chunks = []

    separator = "=================================================="

    for doc in documents:

        sections = doc["content"].split(separator)

        for section in sections:

            section = section.strip()

            if section:

                chunks.append({
                    "source": doc["filename"],
                    "content": section
                })

    return chunks


def store_embeddings(chunks):
    """
    Generate embeddings and store them in ChromaDB.
    """

    collection = get_collection()

    # Delete old data
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        embedding = model.encode(chunk["content"]).tolist()

        ids.append(str(i))
        documents.append(chunk["content"])
        embeddings.append(embedding)

        metadatas.append({
            "source": chunk["source"]
        })

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(ids)


def build_database():
    """
    Complete pipeline:
    Read → Split → Embed → Store
    """

    documents = load_documents()

    chunks = split_documents(documents)

    total = store_embeddings(chunks)

    return total


if __name__ == "__main__":

    total = build_database()

    print("\nKnowledge Base Created Successfully!")
    print(f"Stored {total} chunks.")