from agents.memory_agent import get_preferences

def find_best_slot(slots):

    preferences = get_preferences()

    if preferences["preferred_time"] == "morning":
        return slots[0]

    return slots[1]