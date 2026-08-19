from sentence_transformers import SentenceTransformer
from database import get_collection

# Load the same embedding model used during indexing
model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query, n_results=3):
    """
    Search the vector database for the most relevant chunks.
    """

    collection = get_collection()

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results


if __name__ == "__main__":

    query = input("Ask a question: ")

    results = search(query)

    print("\nResults\n")

    for i, doc in enumerate(results["documents"][0], start=1):

        print("=" * 60)
        print(f"Result {i}\n")
        print(doc)
