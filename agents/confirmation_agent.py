from services.pending_meeting_service import (
    load_pending_meeting,
    clear_pending_meeting
)

from services.calendar_service import (
    create_meeting,
    is_slot_free
)


def confirm_meeting(email_data):

    pending = load_pending_meeting()

    if not pending:
        return {
            "message": "No pending meeting found."
        }

    # Default values from pending meeting
    day = pending["day"]
    date = pending["date"]
    time = pending["time"]

    # -----------------------------
    # Handle Reschedule
    # -----------------------------
    if email_data["intent"] == "reschedule":

        # User only said "No"
        if email_data["date"] == "" and email_data["time"] == "":
            return {
                "reply": """
Hello,

No problem.

Please tell me your preferred date and time.

Examples:

• Tomorrow 6 PM
• Tuesday 11 AM
• 10 July 4 PM

Regards,
SmartMeetingAI
"""
            }

        # User changed date
        if email_data["date"]:
            day = email_data["date"].strip().title()
            date = day

        # User changed time
        if email_data["time"]:
            time = email_data["time"].strip().upper()
    print("\n===== UPDATED REQUEST =====")
    print("Pending Time :", pending["time"])
    print("New Time     :", email_data["time"])
    print("Final Time   :", time)
    print("===========================\n")
    print("\n========== USER REQUEST ==========")
    print("Requested Day :", day)
    print("Requested Time:", time)
    print("==================================")

    # -----------------------------
    # Check availability
    # -----------------------------
    if not is_slot_free(day, time):

        return {
            "reply": f"""
Hello,

Unfortunately,

{day} at {time} is unavailable.

Please suggest another preferred date and time.

Regards,
SmartMeetingAI
"""
        }
    # ----------------------------------------
    # Reschedule -> Don't create meeting yet
    # ----------------------------------------
    if email_data["intent"] == "reschedule":

        pending["day"] = day
        pending["date"] = date
        pending["time"] = time

        from services.pending_meeting_service import save_pending_meeting

        save_pending_meeting(pending)

        return {
            "reply": f"""
Hello,

Your requested schedule is available.

Meeting Details

Date : {date}

Time : {time}

Please reply:

YES

to confirm your meeting.

Regards,
SmartMeetingAI
"""
    }
    attendees = [pending["sender"]]

    if "participants" in pending:
       attendees.extend(pending["participants"])

# Remove duplicates
    attendees = list(dict.fromkeys(attendees))

    print("Pending Date :", date)
    print("Pending Day  :", day)
    print("Pending Time :", time)
    print("Attendees    :", attendees)

    # Meeting title
    summary = pending.get("topic", "").strip()

    if summary == "":
        summary = "SmartMeetingAI Meeting"
    print("\n===== FINAL DATA SENT TO CALENDAR =====")
    print("Day  :", day)
    print("Date :", date)
    print("Time :", time)
    print("=======================================\n")

    # -----------------------------
    # Create Meeting
    # -----------------------------
    meeting = create_meeting(
        summary,
        attendees,
        date,
        time
    )

    print("\n===== MEETING CREATED =====")
    print(meeting)
    print("===========================\n")

    clear_pending_meeting()

    return {
        "reply": f"""
Hello,

Your meeting has been scheduled successfully.

Date : {day}

Time : {time}

Google Meet Link:

{meeting["meet_link"]}

Regards,
SmartMeetingAI
""",
        "meeting_link": meeting["meet_link"]
    }