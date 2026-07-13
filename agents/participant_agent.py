import re


def extract_participants(email_text, sender_email=None):
    """
    Extract all valid email addresses from the email body.
    Removes duplicates and optionally removes the sender.
    """

    participants = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        email_text
    )

    # lowercase + remove spaces
    participants = [email.strip().lower() for email in participants]

    # remove duplicates
    participants = list(dict.fromkeys(participants))

    # remove sender if present
    if sender_email:
        sender_email = sender_email.lower().strip()
        participants = [
            email
            for email in participants
            if email != sender_email
        ]
        print("Participants:", participants)
    return participants
