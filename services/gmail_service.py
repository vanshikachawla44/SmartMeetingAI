from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import pickle
import os
import base64

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar"
]
def gmail_login():

    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if creds is None:

        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service


def get_latest_email():

    service = gmail_login()

    results = service.users().messages().list(
        userId="me",
    
        maxResults=1
    ).execute()

    return results.get("messages", [])
def get_unread_email():

    service = gmail_login()

    results = service.users().messages().list(
        userId="me",
        q='is:unread -from:me',
        maxResults=1
    ).execute()

    messages = results.get("messages", [])
    if not messages:
        return None
    message_id = messages[0]["id"]

    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    return message



def read_latest_email():

    service = gmail_login()

    results = service.users().messages().list(
        userId="me",
        maxResults=1
    ).execute()

    messages = results.get("messages", [])
    if not messages:
        return None

    message_id = messages[0]["id"]

    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    return message


def extract_text(parts):

    for part in parts:

        mime_type = part.get("mimeType")

        if mime_type == "text/plain":

            data = part["body"].get("data")

            if data:
                return base64.urlsafe_b64decode(
                    data.encode("UTF-8")
                ).decode(
                    "utf-8",
                    errors="ignore"
                )

        if mime_type == "text/html":

            data = part["body"].get("data")

            if data:
                return base64.urlsafe_b64decode(
                    data.encode("UTF-8")
                ).decode(
                    "utf-8",
                    errors="ignore"
                )

        if "parts" in part:

            text = extract_text(part["parts"])

            if text:
                return text

    return None


def get_email_text():

    message = read_latest_email()

    if message is None:
        return "No Emails Found"

    payload = message.get("payload", {})

    if "parts" in payload:

        text = extract_text(payload["parts"])

        if text:
            return text

    data = payload.get("body", {}).get("data")

    if data:
        return base64.urlsafe_b64decode(
            data.encode("UTF-8")
        ).decode(
            "utf-8",
            errors="ignore"
        )

    return "Email body not found."


def get_unread_email_text():

    message = get_unread_email()

    if message is None:
        return None

    payload = message.get("payload", {})
    text = None 

    if "parts" in payload:
        text = extract_text(payload["parts"])

    if text:

        # Remove quoted conversation
        if "On " in text:
            text = text.split("On ")[0].strip()

        if "From:" in text:
            text = text.split("From:")[0].strip()

        return text

    data = payload.get("body", {}).get("data")

    if data:
        text = base64.urlsafe_b64decode(
            data.encode("UTF-8")
            ).decode(
                "utf-8",
                errors="ignore"
    )

    if "On " in text:
        text = text.split("On ")[0].strip()

    if "From:" in text:
        text = text.split("From:")[0].strip()

    return text
    return None


def send_email(to, subject, body):

    service = gmail_login()

    message = MIMEText(body)

    message["to"] = to
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    send_body = {
        "raw": raw_message
    }

    service.users().messages().send(
        userId="me",
        body=send_body
    ).execute()

    print("Email sent successfully.")


def get_sender_email():

    message = get_unread_email()

    if message is None:
        return None

    headers = message["payload"].get("headers", [])

    for header in headers:

        if header["name"] == "From":

            sender = header["value"]

            if "<" in sender:
                return sender.split("<")[1].replace(">", "")

            return sender

    return None
def get_email_subject():

    message = get_unread_email()

    if message is None:
        return ""

    headers = message["payload"].get("headers", [])

    for header in headers:

        if header["name"] == "Subject":
            return header["value"].strip()

    return ""
def mark_as_read():

    service = gmail_login()

    message = get_unread_email()

    if message is None:
        return

    message_id = message["id"]

    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={
            "removeLabelIds": ["UNREAD"]
        }
    ).execute()

    print("Email marked as read.")


def get_message_id():

    message = get_unread_email()

    if message is None:
        return None

    return message["id"]