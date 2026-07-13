import json

FILE_PATH = "data/meeting_history.json"

def get_all_meetings():

    with open(FILE_PATH, "r") as file:
        meetings = json.load(file)

    return meetings