from services.gmail_service import get_email_subject
from utils.date_parser import get_datetime
from agents.calendar_agent import (
    get_available_slots,
    get_alternative_slots
)
from services.gmail_service import get_sender_email
from services.pending_meeting_service import save_pending_meeting
from agents.logger_agent import save_meeting

from agents.decision_agent import choose_slot, explain_decision
from agents.reply_agent import generate_reply
from agents.memory_agent import get_preferences


def schedule_meeting(email_data):

    # Check if it is a meeting request
    if "meeting" not in email_data["intent"].lower():
        return {
            "message": "Not a meeting request"
        }

    # Get available slots
    slots = get_available_slots()

    # User preferences
    preferences = get_preferences()
    email_subject = get_email_subject()
    print(email_data)
    print("Parsed Email Data:", email_data)
    # Choose best slot
    best_slot = choose_slot(
        email_data,
        slots,
        preferences
    )
    if best_slot.get("needs_clarification"):
        return {
        "reply": """
Hello,

I'd be happy to schedule your meeting.

Could you please specify:

• Preferred day
• Preferred time

Examples:

• Next Tuesday 3 PM
• Friday 11 AM

Regards,
SmartMeetingAI
"""
    }
    
    from services.gmail_service import get_email_subject
from utils.date_parser import get_datetime
from agents.calendar_agent import (
    get_available_slots,
    get_alternative_slots
)
from services.gmail_service import get_sender_email
from services.pending_meeting_service import save_pending_meeting
from agents.logger_agent import save_meeting

from agents.decision_agent import choose_slot, explain_decision
from agents.reply_agent import generate_reply
from agents.memory_agent import get_preferences


def schedule_meeting(email_data):

    # Check if it is a meeting request
    if "meeting" not in email_data["intent"].lower():
        return {
            "message": "Not a meeting request"
        }

    # Get available slots
    slots = get_available_slots()

    # User preferences
    preferences = get_preferences()
    email_subject = get_email_subject()
    print(email_data)
    print("Parsed Email Data:", email_data)
    # Choose best slot
    best_slot = choose_slot(
        email_data,
        slots,
        preferences
    )
    if best_slot.get("needs_clarification"):
        return {
        "reply": """
Hello,

I'd be happy to schedule your meeting.

Could you please specify:

• Preferred day
• Preferred time

Examples:

• Next Tuesday 3 PM
• Friday 11 AM

Regards,
SmartMeetingAI
"""
    }
    
    
    if best_slot.get("outside_working_hours"):
        return {
             "reply": f"""
Hello,

The requested meeting time ({email_data['time']}) is outside the configured working hours.

Working Hours:
9:00 AM – 6:00 PM

Please choose another time.

Regards,
SmartMeetingAI
"""

    }
        if best_slot.get("no_slot_available"):
            return {
            "reply": """
Hello,

Unfortunately,

No meeting slot is available for the requested day.

Please choose another date or time.

Regards,
SmartMeetingAI
"""
        }

    requested_date = email_data.get("date", "").strip()
    requested_time = email_data.get("time", "").strip()
    # ------------------------------------
    # Working Hours Validation (Quick Check)
    # ------------------------------------
    from datetime import datetime

    if requested_time:

        temp_time = None

        for fmt in (
            "%I %p",
            "%I:%M %p",
            "%I%p",
            "%I:%M%p"
        ):

            try:
                temp_time = datetime.strptime(
                    requested_time.upper(),
                    fmt
                )
                break

            except ValueError:
                pass

        if temp_time is not None:

            if (
                temp_time.hour < 9
                or temp_time.hour >= 18
            ):

                return {
                    "reply": f"""
Hello,

The requested meeting time ({requested_time}) is outside the configured working hours.

Working Hours:
9:00 AM – 6:00 PM

Please choose another time.

Regards,
SmartMeetingAI
"""
                }

    meeting_datetime = get_datetime(
            requested_date,
            best_slot["time"]
    )
    

    formatted_date = meeting_datetime.strftime("%A, %d %B %Y")

    print("\n===== DATE DEBUG =====")
    print("Original Request :", requested_date)
    print("Final Date       :", formatted_date)
    print("======================\n")
    # Alternative slots
    alternatives = get_alternative_slots(
        best_slot["slot"],
        slots
    )

    print("BEST SLOT:", best_slot)
    

    formatted_date = meeting_datetime.strftime("%A, %d %B %Y")

    # Generate reply
    reply = generate_reply(
    best_slot["slot"],
    alternatives,
    formatted_date,
    best_slot["time"],
    best_slot["requested_slot_available"]
)
    # Explain decision
    reason = explain_decision(best_slot["slot"])

    # Get attendee email
    attendee = get_sender_email()

    if attendee is None:
        attendee = ""

    print("Saving pending meeting:")
    print(email_data)
        # Save pending meeting

    topic = email_subject.strip()

    if topic == "":
        topic = email_data.get("topic", "").strip()

    if topic == "":
        topic = "Meeting"
    print("Participants being saved:", email_data["participants"])
    print("\n===== DATA TO SAVE =====")
    print({
        "status": "waiting_confirmation",
        "sender": attendee,
        "participants": email_data["participants"],
        "topic": topic,
        "day": best_slot["day"],
     "date": formatted_date,
        "time": best_slot["time"]
})
    print("========================\n")
    save_pending_meeting({
    "status": "waiting_confirmation",
    "sender": attendee,

    # NEW
    "participants": email_data["participants"],

    "topic": topic,
    "day": best_slot["day"],
    "date": formatted_date,
    "time": best_slot["time"]
})

    # Save meeting history
    save_meeting({
        "intent": email_data["intent"],
        "topic": topic,
        "participants": email_data["participants"],
        "best_slot": best_slot["slot"],
        "available_slots": slots
    })
    return {
        "intent": email_data["intent"],
        "meeting_details": email_data,
        "available_slots": slots,
        "best_slot": best_slot["slot"],
        "alternative_slots": alternatives,
        "reason": reason,
        "reply": reply
    }
    # ------------------------------------
    # Working Hours Validation (Quick Check)
    # ------------------------------------
    from datetime import datetime

    if requested_time:

        temp_time = None

        for fmt in (
            "%I %p",
            "%I:%M %p",
            "%I%p",
            "%I:%M%p"
        ):

            try:
                temp_time = datetime.strptime(
                    requested_time.upper(),
                    fmt
                )
                break

            except ValueError:
                pass

        if temp_time is not None:

            if (
                temp_time.hour < 9
                or temp_time.hour >= 18
            ):

                return {
                    "reply": f"""
Hello,

The requested meeting time ({requested_time}) is outside the configured working hours.

Working Hours:
9:00 AM – 6:00 PM

Please choose another time.

Regards,
SmartMeetingAI
"""
                }

    meeting_datetime = get_datetime(
            requested_date,
            best_slot["time"]
    )
    

    formatted_date = meeting_datetime.strftime("%A, %d %B %Y")

    print("\n===== DATE DEBUG =====")
    print("Original Request :", requested_date)
    print("Final Date       :", formatted_date)
    print("======================\n")
    # Alternative slots
    alternatives = get_alternative_slots(
        best_slot["slot"],
        slots
    )

    print("BEST SLOT:", best_slot)
    

    formatted_date = meeting_datetime.strftime("%A, %d %B %Y")

    # Generate reply
    reply = generate_reply(
    best_slot["slot"],
    alternatives,
    formatted_date,
    best_slot["time"],
    best_slot["requested_slot_available"]
)
    # Explain decision
    reason = explain_decision(best_slot["slot"])

    # Get attendee email
    attendee = get_sender_email()

    if attendee is None:
        attendee = ""

    print("Saving pending meeting:")
    print(email_data)
        # Save pending meeting

    topic = email_subject.strip()

    if topic == "":
        topic = email_data.get("topic", "").strip()

    if topic == "":
        topic = "Meeting"
    print("Participants being saved:", email_data["participants"])
    print("\n===== DATA TO SAVE =====")
    print({
        "status": "waiting_confirmation",
        "sender": attendee,
        "participants": email_data["participants"],
        "topic": topic,
        "day": best_slot["day"],
     "date": formatted_date,
        "time": best_slot["time"]
})
    print("========================\n")
    save_pending_meeting({
    "status": "waiting_confirmation",
    "sender": attendee,

    # NEW
    "participants": email_data["participants"],

    "topic": topic,
    "day": best_slot["day"],
    "date": formatted_date,
    "time": best_slot["time"]
})

    # Save meeting history
    save_meeting({
        "intent": email_data["intent"],
        "topic": topic,
        "participants": email_data["participants"],
        "best_slot": best_slot["slot"],
        "available_slots": slots
    })
    return {
        "intent": email_data["intent"],
        "meeting_details": email_data,
        "available_slots": slots,
        "best_slot": best_slot["slot"],
        "alternative_slots": alternatives,
        "reason": reason,
        "reply": reply
    }