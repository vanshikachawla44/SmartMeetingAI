from config import (
    DEFAULT_TIMEZONE,
    MEETING_DURATION,
    CALENDAR_ID
)


import uuid
from datetime import datetime, timedelta, timezone

from googleapiclient.discovery import build

from services.gmail_service import gmail_login
from utils.date_parser import get_datetime


IST = timezone(timedelta(hours=5, minutes=30))


def get_calendar_service():

    creds = gmail_login()._http.credentials

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    return service


# --------------------------------------------------
# Get all busy slots from Google Calendar
# --------------------------------------------------
def get_busy_slots(days=7):

    service = get_calendar_service()

    now = datetime.now(IST)
    end = now + timedelta(days=days)

    events = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    busy_slots = []

    for event in events.get("items", []):

        start = event.get("start", {}).get("dateTime")

        if not start:
            continue

        dt = datetime.fromisoformat(start)

        busy_slots.append(
            dt.strftime("%A %I:%M %p")
        )
        print("\n===== BUSY SLOTS =====")
        for slot in busy_slots:
            print(slot)
            print("======================\n")

    return busy_slots


# --------------------------------------------------
# Check whether a slot is free
# --------------------------------------------------

def is_slot_free(day, time):

    service = get_calendar_service()

    print("Meeting Day :", day)
    print("Meeting Time:", time)

    start_time = get_datetime(day, time)
    start_time = start_time.replace(tzinfo=IST)

    end_time = start_time + timedelta(minutes=MEETING_DURATION)

    print("Start:", start_time)
    print("End  :", end_time)

    events = service.events().list(
        calendarId="primary",
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return len(events.get("items", [])) == 0

def create_meeting(
    summary,
    attendees,
    meeting_date,
    time
):

    service = get_calendar_service()
    print("Meeting Date:", meeting_date)
    print("Meeting Time:", time)
    start_time = get_datetime(meeting_date, time)
    start_time = start_time.replace(tzinfo=IST)
    print("Start Time:", start_time)
    end_time = start_time + timedelta(minutes=MEETING_DURATION)
    event = {

    "summary": summary if summary else "SmartMeetingAI Meeting",

    "description": f"""
    Meeting Details
    Title:
    {summary}
    Organizer:
    smartmeetingai.demos@gmail.com
    Participants:
{", ".join(attendees)}
    Platform:
    Google Meet

This meeting was scheduled automatically using SmartMeetingAI.
""",

    "location": "Google Meet",
    "visibility": "default",
    "guestsCanModify": False,
    "guestsCanInviteOthers": False,
    "guestsCanSeeOtherGuests": True,

    "start": {
        "dateTime": start_time.isoformat(),
         "timeZone": DEFAULT_TIMEZONE
    },

    "end": {
        "dateTime": end_time.isoformat(),
         "timeZone": DEFAULT_TIMEZONE
    },

    "attendees": [
    {
        "email": email,
        "responseStatus": "needsAction"
    }
    for email in attendees
],

   
    "conferenceData": {
        "createRequest": {
            "requestId": str(uuid.uuid4())
        }
    }
}
    event = service.events().insert(
        calendarId="primary",
        body=event,
        conferenceDataVersion=1,
        sendUpdates="all"
    ).execute()
    calendars = service.calendarList().list().execute()
    print("\n===== CALENDARS =====")
    for cal in calendars["items"]:
        print(
        "ID:", cal.get("id"),
        "| Summary:", cal.get("summary"),
        "| Primary:", cal.get("primary")
    )
    print("=====================\n")
    event_id = event["id"]
    saved_event = service.events().get(
    calendarId="primary",
    eventId=event_id
).execute()

    print("Calendar ID:", saved_event.get("organizer", {}).get("email"))
    print("Event Status:", saved_event.get("status"))
    print("Event HTML:", saved_event.get("htmlLink"))

    print("\n===== EVENT CREATED =====")
    print("Event ID:", event.get("id"))
    print("Organizer:", event.get("organizer"))
    print("Creator:", event.get("creator"))
    print("Attendees:", event.get("attendees"))
    print("Meet Link:", event.get("hangoutLink"))

    event_id = event["id"]

    saved_event = service.events().get(
        calendarId="primary",
        eventId=event_id
    ).execute()

    print("Saved Event Summary:", saved_event.get("summary"))
    print("Saved Event Start:", saved_event.get("start"))
    print("Saved Event HTML Link:", saved_event.get("htmlLink"))
    print("=========================\n")

    return {
        "meet_link": event["hangoutLink"],
        "organizer": event.get("organizer"),
        "creator": event.get("creator"),
        "attendees": event.get("attendees")
    }