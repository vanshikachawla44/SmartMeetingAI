from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def extract_meeting_details(email_text):

    prompt = f"""
    Extract meeting details from this email.

    Return ONLY valid JSON in this format:

    {{
        "date": "",
        "time": "",
        "participants": [],
        "topic": ""
    }}

    Email:
    {email_text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    text = response.choices[0].message.content.strip()

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    try:
        return json.loads(text)

    except Exception as e:
        print("JSON Parsing Error:", e)

        return {
            "date": "",
            "time": "",
            "participants": [],
            "topic": ""
        }