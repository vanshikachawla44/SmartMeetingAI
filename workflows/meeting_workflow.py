from agents.participant_agent import extract_participants
from services.gmail_service import get_sender_email
from agents.email_understanding_agent import understand_email
from agents.memory_agent import get_preferences
from agents.meeting_scheduler_agent import schedule_meeting
from agents.confirmation_agent import confirm_meeting
from services.pending_meeting_service import load_pending_meeting


def run_workflow(email_text):

    print("========== EMAIL TEXT ==========")
    print(email_text)
    print("================================")

    email_data = understand_email(email_text)
    sender = get_sender_email()
    participants = extract_participants(
        email_text,
        sender
)
    email_data["participants"] = participants

    print(email_data)

    preferences = get_preferences()

    # Check if a meeting is already waiting for confirmation
        # Check if a meeting is already waiting for confirmation
    pending = load_pending_meeting()

    print("\n===== PENDING MEETING =====")
    print(pending)
    print("===========================\n")

    print("Pending Exists :", bool(pending))
    print("Intent         :", email_data["intent"])

    # ---------------------------------------------------
    # CASE 1 : User is replying to an existing meeting
    # ---------------------------------------------------
    if pending:

        # User accepted
        if email_data["intent"] == "confirmation":

            result = confirm_meeting(email_data)

        # User suggested another date/time
        elif (
            email_data["intent"] == "reschedule"
            or (
                email_data["intent"] == "meeting_request"
                and (
                    email_data["date"] != ""
                    or email_data["time"] != ""
                )
            )
        ):

            email_data["intent"] = "reschedule"

            result = confirm_meeting(email_data)

        # User simply said No / Not fine
        else:

            result = {
                "reply": """
Hello,

No problem.

Please tell me your preferred date and time.

Examples:

• Tomorrow 6 PM
• Tuesday 11 AM
• Next Monday 2 PM

Regards,
SmartMeetingAI
"""
            }

    # ---------------------------------------------------
    # CASE 2 : Brand new meeting request
    # ---------------------------------------------------
    else:

        if email_data["intent"] == "meeting_request":

            result = schedule_meeting(email_data)

        elif email_data["intent"] in ["confirmation", "reschedule"]:

            result = {
            "reply": """
Hello,

I couldn't find any pending meeting to update.

It looks like the previous meeting has already been scheduled.

If you'd like to change the meeting, please send a new meeting request, for example:

• Can we have meeting on 4 Aug 5 PM
• Reschedule meeting to tomorrow 3 PM

Regards,
SmartMeetingAI
"""
        }

        else:

            result = {
            "message": "Unsupported email."
        }

    return {
        "email_understanding": email_data,
        "user_preferences": preferences,
        "schedule_result": result
    }
