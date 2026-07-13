import json
from datetime import datetime

FILE_PATH = "data/meeting_history.json"

def save_meeting(meeting_data):

    try:
        with open(FILE_PATH, "r") as file:
            meetings = json.load(file)

    except:
        meetings = []

    meeting_data["timestamp"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    meetings.append(meeting_data)

    with open(FILE_PATH, "w") as file:
        json.dump(meetings, file, indent=4)

    return True