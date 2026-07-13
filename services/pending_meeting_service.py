import json
import os

FILE_PATH = "data/pending_meeting.json"


def save_pending_meeting(data):
    print("\nSaving Pending Meeting File...")
    print(data)

    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)
        print("Pending meeting saved successfully.")


def load_pending_meeting():

    if not os.path.exists(FILE_PATH):
        return {}

    with open(FILE_PATH, "r") as file:
        return json.load(file)


def clear_pending_meeting():

    with open(FILE_PATH, "w") as file:
        json.dump({}, file, indent=4)