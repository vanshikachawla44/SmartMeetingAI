def generate_reply(
    best_slot,
    alternative_slots,
    date,
    time,
    requested_slot_available
):

    alternatives_text = ""

    for slot in alternative_slots:
        alternatives_text += f"• {slot}\n"

    # ------------------------------------
    # Requested slot is available
    # ------------------------------------
    if requested_slot_available:

        return f"""
Hello,

Thank you for your meeting request.

✅ Your requested meeting time is available.

Meeting Details

Date : {date}

Time : {time}

Please reply with:

YES

to confirm your meeting.

Regards,
SmartMeetingAI
"""

    # ------------------------------------
    # Requested slot is NOT available
    # ------------------------------------
    return f"""
Hello,

Thank you for your meeting request.

Requested Time

Date : {date}

Time : {time}

Unfortunately, your requested time is not available.

Best Available Slot

{best_slot}

Other Available Slots

{alternatives_text}

If the suggested time works for you, simply reply:

YES

Otherwise, reply with your preferred date and time.

Examples:

• Tomorrow 6 PM
• Tuesday 11 AM
• 10 July 4 PM

Regards,
SmartMeetingAI
"""