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

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    return documents, metadatas


if __name__ == "__main__":

    question = input("Ask a question: ")

    documents, metadatas = search(question)

    print()

    for i, (document, metadata) in enumerate(
        zip(documents, metadatas),
        start=1
    ):

        print("=" * 60)

        print(f"Result {i}\n")

        print(document)

        print(f"\nSource: {metadata['source']}")