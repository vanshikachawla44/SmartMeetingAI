import json
import chromadb

from rag.embedding import create_embedding

client = chromadb.PersistentClient(path="./chroma_db")

try:
    client.delete_collection("meeting_history")
except Exception:
    pass

collection = client.get_or_create_collection(
    name="meeting_history"
)


def build_vector_store():

    with open("data/meeting_history.json", "r") as f:
        meetings = json.load(f)

    

    for i, meeting in enumerate(meetings):

        text = f"""
Intent: {meeting.get("intent")}
Topic: {meeting.get("topic")}
Participants: {meeting.get("participants")}
Best Slot: {meeting.get("best_slot")}
Timestamp: {meeting.get("timestamp")}
"""

        embedding = create_embedding(text)

        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[text],
        )

    print("Vector Database Created Successfully!")