import chromadb
from rag.embedding import create_embedding

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("meeting_history")


def retrieve(query: str, n_results: int = 3):
    embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )

    return results["documents"][0]