from datetime import datetime, timedelta


def get_datetime(day, time_string):

    day = day.lower().strip()
    # Normalize common misspellings
    day_aliases = {
        "tommorow": "tomorrow",
        "tomorow": "tomorrow",
        "tmrw": "tomorrow",
        "tmr": "tomorrow",
        "todday": "today",
}

    day = day_aliases.get(day, day)
    today = datetime.now()

    # -----------------------------
    # today / tomorrow
    # -----------------------------
    # -----------------------------
    # Relative Dates
    # -----------------------------
        # -----------------------------
    # Relative Dates
    # -----------------------------

    meeting_date = None

    if day == "today":
        meeting_date = today

    elif day == "tomorrow":
        meeting_date = today + timedelta(days=1)

    elif day == "day after tomorrow":
        meeting_date = today + timedelta(days=2)

    elif day == "next week":
        meeting_date = today + timedelta(days=7)

    elif day == "next month":

        month = today.month + 1
        year = today.year

        if month > 12:
            month = 1
            year += 1

        meeting_date = today.replace(
            year=year,
            month=month,
            day=min(today.day, 28)
        )

    elif day == "next year":

        meeting_date = today.replace(
            year=today.year + 1
        )

    else:

        is_next = False
        is_this = False

        if day.startswith("next "):
            is_next = True
            day = day.replace("next ", "").strip()

        elif day.startswith("this "):
            is_this = True
            day = day.replace("this ", "").strip()

        short_days = {
            "mon": "monday",
            "tue": "tuesday",
            "tues": "tuesday",
            "wed": "wednesday",
            "thu": "thursday",
            "thur": "thursday",
            "thurs": "thursday",
            "fri": "friday",
            "sat": "saturday",
            "sun": "sunday"
        }

        if day in short_days:
            day = short_days[day]

    if meeting_date is None:

        date_formats = [
   
         "%A, %d %b %Y",
            "%A, %d %B %Y",

            "%d %b %Y",
            "%d %B %Y",

            "%d %b",
            "%d %B",

            "%Y-%m-%d",

            "%d/%m/%Y",
            "%d/%m/%y",

            "%d-%m-%Y",
            "%d-%m-%y",

            "%d.%m.%Y",
            "%d.%m.%y",

            "%m/%d/%Y",
            "%m/%d/%y"
    ] 
    for fmt in date_formats:
            try:
                meeting_date = datetime.strptime(day, fmt)
                # If year is not present, use current year
                if "%Y" not in fmt and "%y" not in fmt:
                    meeting_date = meeting_date.replace(year=today.year)

                # Convert 2-digit year to 20xx if needed
                elif "%y" in fmt and meeting_date.year < 2000:
                    meeting_date = meeting_date.replace(
                            year=2000 + (meeting_date.year % 100)
    )
                break

            except ValueError:
                pass

        # -----------------------------
        # Weekday handling
        # -----------------------------
    if meeting_date is None:

            weekdays = {
                "monday": 0,
                "tuesday": 1,
                "wednesday": 2,
                "thursday": 3,
                "friday": 4,
                "saturday": 5,
                "sunday": 6
            }

            if day not in weekdays:
                raise ValueError(f"Unsupported day: {day}")

            target_day = weekdays[day]

            days_ahead = target_day - today.weekday()
            

            if is_next:
                if days_ahead <= 0:
                    days_ahead += 7

            elif is_this:
                if days_ahead < 0:
                    days_ahead += 7

            else:
                if days_ahead <= 0:
                    days_ahead += 7

            meeting_date = today + timedelta(days=days_ahead)
 

    # -----------------------------
    # Time Parsing
    # -----------------------------
    time_string = time_string.upper().strip()

    formats = [
        "%I:%M %p",
        "%I %p",
        "%I:%M%p",
        "%I%p",
        "%H:%M",
        "%H"
    ]

    time_obj = None

    for fmt in formats:
        try:
            time_obj = datetime.strptime(time_string, fmt)
            break
        except ValueError:
            pass

    if time_obj is None:
        raise ValueError(
            f"Unsupported time format: {time_string}"
        )

    meeting_date = meeting_date.replace(
        hour=time_obj.hour,
        minute=time_obj.minute,
        second=0,
        microsecond=0
    )

    return meeting_date