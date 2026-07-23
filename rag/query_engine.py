import os
from dotenv import load_dotenv
from groq import Groq
from rag.retriever import retrieve

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
from groq import Groq
import os

from rag.retriever import retrieve

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ask_rag(question: str):

    docs = retrieve(question)

    context = "\n\n".join(docs)

    prompt = f"""
You are SmartMeetingAI.

Answer ONLY using the context below.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content