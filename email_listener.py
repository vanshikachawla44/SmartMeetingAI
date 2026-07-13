import time

from services.gmail_service import (
    get_unread_email_text,
    get_sender_email,
    send_email,
    mark_as_read,
    get_message_id
)

from workflows.meeting_workflow import run_workflow


processed_ids = set()

try:
    with open("processed_emails.txt", "r") as file:
        for line in file:
            processed_ids.add(line.strip())
except FileNotFoundError:
    pass


print("Listening for new emails...")


while True:

    message_id = get_message_id()

    if message_id is None:
        print("No new unread meeting email found.")
        time.sleep(30)
        continue

    if message_id in processed_ids:
        time.sleep(30)
        continue

    email = get_unread_email_text()
    if email:

        lower_email = email.lower()

    if (
        "invitation from google calendar" in lower_email
        or "calendar.google.com" in lower_email
        or "organiser" in lower_email
        or "google meet" in lower_email
    ):
        print("Ignoring Google Calendar invitation.")

        mark_as_read()

        continue
    if email is None:
        print("Unable to read email.")
        time.sleep(30)
        continue
    sender = get_sender_email()
    print("\n========== NEW UNREAD MEETING EMAIL ==========\n")
    result = run_workflow(email)
    print("\n===== WORKFLOW RESULT =====")
    print(result)
    print("===========================\n")

    intent = result["email_understanding"]["intent"].lower()

    if (
    "schedule_result" in result
    and "reply" in result["schedule_result"]
):

    # Confirmation ke baad Google Calendar invitation hi enough hai
       if intent != "confirmation":

        send_email(
            sender,
            "Meeting Response",
            result["schedule_result"]["reply"]
        )



        mark_as_read()

        processed_ids.add(message_id)

        with open("processed_emails.txt", "a") as file:
            file.write(message_id + "\n")

        print("Reply sent successfully.")

    else:
        print(result["schedule_result"]["message"])

    time.sleep(30)