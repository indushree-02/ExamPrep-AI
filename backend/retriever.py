from sentence_transformers import SentenceTransformer
from database import get_collection

model = SentenceTransformer("all-MiniLM-L6-v2")


def search(query, n_results=3):

    collection = get_collection()

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results["documents"][0]


if __name__ == "__main__":

    question = input("Ask a question: ")

    docs = search(question)

    print()

    for i, doc in enumerate(docs, start=1):
        print("=" * 60)
        print(f"Result {i}\n")
        print(doc)