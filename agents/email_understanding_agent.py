from groq import Groq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def understand_email(email_text):

    # Large HTML emails ko limit kar do
    email_text = email_text[:3000]

    prompt = f"""
You are an AI assistant that extracts meeting information from emails.

Your job is to return ONLY valid JSON.

Possible intents:

1. meeting_request
   - User is asking to schedule a meeting.

2. confirmation
   - User is accepting the proposed meeting.
   Examples:
   Yes
   Sure
   That works
   Tuesday works
   Confirmed

   3. reschedule

The sender rejects the proposed meeting and suggests a NEW preferred date and/or time.

Examples:

No, Tuesday 5 PM works.
No, Tuesday 6 PM works instead.
No, can we meet on Friday at 3 PM?
Wednesday 6 PM is better.
Can we do Thursday 11 AM instead?
Monday won't work. Tuesday 6 PM works.
I am not available at that time. Friday 4 PM works.
Tuesday afternoon is better.

Rules:
Participants Rules:

- Extract every email address mentioned in the email.
- Store all email addresses in the "participants" array.
- If no participant email is mentioned, return an empty array [].
- Never invent email addresses.
- Do not include the sender's email unless it is explicitly written in the email body.

Example:

Email:

Can we have a meeting tomorrow with

rahul@gmail.com

aman@gmail.com

Return:

"participants": [
    "rahul@gmail.com",
    "aman@gmail.com"
]

- Return ONLY valid JSON.
- Never return markdown.
- Never explain.
- Never guess.
- If date is not mentioned, return "".
- If time is not mentioned, return "".
- If topic is not mentioned, return "".
- Do NOT invent values like Sunday or 12:00 AM.
- Extract the exact day and time mentioned in the email.
- For confirmation emails like "Yes" or "Sure", keep date and time empty unless they are explicitly written.

If the sender rejects the proposed meeting and includes a NEW date or time,
always return:

intent = "reschedule"

Extract the NEW proposed date and time exactly as written.

Never reuse the old meeting date or time.

Examples:

"No, Tuesday 6 PM works instead."

returns

{{
    "intent":"reschedule",
    "date":"Tuesday",
    "time":"6 PM",
    "participants":[],
    "topic":""
}}

"Wednesday 3 PM is better."

returns

{{
    "intent":"reschedule",
    "date":"Wednesday",
    "time":"3 PM",
    "participants":[],
    "topic":""
}}
Example

Email:

Subject: Project Discussion

Can we have a meeting tomorrow at 4 PM with

rahul@gmail.com

aman@gmail.com

Return

Return

{{
    "intent":"meeting_request",
    "date":"tomorrow",
    "time":"4 PM",
    "participants":[
        "person1@example.com",
        "person2@example.com"
    ],
    "topic":"Project Discussion"
}}
Return this JSON format exactly:

{{
    "intent": "",
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
        temperature=0,
        max_tokens=200
    )

    text = response.choices[0].message.content.strip()
    print("\n===== EMAIL SENT TO GROQ =====")
    print(email_text)
    print("\n===== RAW GROQ RESPONSE =====")
    print(text)
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    try:
        parsed = json.loads(text)
       
        lower = email_text.lower()

        if parsed["intent"] == "":
            if (
                "not available" in lower
                or "not ok" in lower
                or "not okay" in lower
                or "won't work" in lower
                or "will not work" in lower
                or "instead" in lower
                or "better" in lower
            ):
                parsed["intent"] = "reschedule"

        return parsed

    except Exception as e:

        print("JSON Parsing Error:", e)

        return {
            "intent": "other",
            "date": "",
            "time": "",
            "participants": [],
            "topic": ""
        }
    