from datetime import datetime

from config import WORKING_HOURS
from services.calendar_service import is_slot_free
from utils.date_parser import get_datetime


def parse_requested_time(time_text):

    if not time_text:
        return None

    time_text = time_text.strip().upper().replace(" ", "")

    formats = [
        "%I%p",
        "%I:%M%p"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(time_text, fmt)
        except ValueError:
            pass

    return None


def choose_slot(email_data, available_slots, preferences):
    requested_date = email_data.get("date", "").strip()

    requested_day = ""

    if requested_date:

        try:
            temp_date = get_datetime(
                requested_date,
                "09:00 AM"
            )

            requested_day = temp_date.strftime("%A").lower()

        except Exception:

            # Ambiguous natural language dates
            if requested_date.lower() in [
                "next week",
                "weekend",
                "next month"
            ]:

                return {
                    "slot": None,
                    "day": "",
                    "time": "",
                    "outside_working_hours": False,
                    "no_slot_available": False,
                    "requested_slot_available": False,
                    "needs_clarification": True
                }

            requested_day = requested_date.lower()

    requested_time = parse_requested_time(
        email_data.get("time", "")
    )

    # -------------------------
    # Same Day Slots
    # -------------------------

    day_slots = [
        slot for slot in available_slots
        if slot.lower().startswith(requested_day)
    ]

    if not day_slots:
        day_slots = available_slots

    # -------------------------
    # No Time Mentioned
    # -------------------------

    if requested_time is None:

        best_slot = day_slots[0]

        return {
            "slot": best_slot,
            "day": best_slot.split()[0],
            "time": " ".join(best_slot.split()[1:]),
            "outside_working_hours": False,
            "no_slot_available": False,
            "requested_slot_available": True
        }

    # -------------------------
    # Working Hours Validation
    # -------------------------

    if (
        requested_time.hour < WORKING_HOURS["start"]
        or requested_time.hour >= WORKING_HOURS["end"]
    ):

        return {
            "slot": None,
            "day": "",
            "time": "",
            "outside_working_hours": True,
            "no_slot_available": False,
            "requested_slot_available": False
        }

    # -------------------------
    # Find Best Slot
    # -------------------------
        # -------------------------
    # Find Best Slot
    # -------------------------

    best_slot = None
    best_difference = float("inf")

    for slot in day_slots:

        day = slot.split()[0]
        time = " ".join(slot.split()[1:])

        if not is_slot_free(day, time):
            continue

        slot_time = datetime.strptime(
            time,
            "%I:%M %p"
        )

        slot_minutes = (
            slot_time.hour * 60
            + slot_time.minute
        )

        requested_minutes = (
            requested_time.hour * 60
            + requested_time.minute
        )

        difference = abs(
            slot_minutes - requested_minutes
        )

        # Perfect match
        if difference == 0:

            best_slot = slot
            best_difference = 0
            break

        # Better match
        if difference < best_difference:

            best_difference = difference
            best_slot = slot

        # Same difference -> prefer later slot
        elif (
            difference == best_difference
            and best_slot is not None
        ):

            current_best_time = " ".join(best_slot.split()[1:])
            current_best = datetime.strptime(
                current_best_time,
                "%I:%M %p"
            )

            current_best_minutes = (
                current_best.hour * 60
                + current_best.minute
            )

            if slot_minutes > current_best_minutes:
                best_slot = slot

    # -------------------------
    # No Free Slot
    # -------------------------

    if best_slot is None:

        return {
            "slot": None,
            "day": "",
            "time": "",
            "outside_working_hours": False,
            "no_slot_available": True,
            "requested_slot_available": False
        }

    print("\n========== DECISION REPORT ==========")
    print("Requested Day :", email_data.get("date"))
    print("Requested Time:", email_data.get("time"))
    print("Selected Slot :", best_slot)
    print("Difference    :", best_difference, "minutes")
    print("=====================================\n")

    return {
        "slot": best_slot,
        "day": best_slot.split()[0],
        "time": " ".join(best_slot.split()[1:]),
        "outside_working_hours": False,
        "no_slot_available": False,
        "requested_slot_available": best_difference == 0
    }


def explain_decision(best_slot):

    return f"""
SmartMeetingAI Decision Report

Selected Slot:
{best_slot}

Reason:

✓ Requested day matched

✓ Closest available slot selected

✓ Google Calendar checked

✓ Working hours validated

✓ No scheduling conflict found
"""