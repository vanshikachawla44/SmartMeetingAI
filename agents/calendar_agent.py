# # from datetime import datetime, timedelta

# # from services.calendar_service import get_busy_slots
# # from config import (
# #     WORKING_HOURS,
# #     SEARCH_DAYS
# # )


# # def get_available_slots():

# #     slots = []
# #     busy_slots = get_busy_slots()

# #     today = datetime.now()

# #     for day_offset in range(SEARCH_DAYS):

# #         current_day = today + timedelta(days=day_offset)

# #         for hour in range(
# #             WORKING_HOURS["start"],
# #             WORKING_HOURS["end"]
# #         ):

# #             slot = datetime(
# #                 current_day.year,
# #                 current_day.month,
# #                 current_day.day,
# #                 hour,
# #                 0
# #             )

# #             formatted_slot = slot.strftime("%A %I:%M %p")

# #             if formatted_slot not in busy_slots:
# #                 slots.append(formatted_slot)

# #     print("\n===== AVAILABLE SLOTS =====")

# #     for slot in slots:
# #         print(slot)

# #     print("===========================\n")

# #     return slots


# # def get_alternative_slots(best_slot, available_slots):

# #     if best_slot not in available_slots:
# #         return available_slots[:3]

# #     index = available_slots.index(best_slot)

# #     alternatives = []

# #     for slot in available_slots[index + 1:]:

# #         alternatives.append(slot)

# #         if len(alternatives) == 3:
# #             break

# #     if len(alternatives) < 3:

# #         for slot in available_slots:

# #             if slot == best_slot:
# #                 continue

# #             if slot not in alternatives:
# #                 alternatives.append(slot)

# #             if len(alternatives) == 3:
# #                 break

# #     return alternatives



# from datetime import datetime, timedelta

# from services.calendar_service import get_busy_slots
# from config import (
#     WORKING_HOURS,
#     SEARCH_DAYS
# )


# def get_available_slots():

#     slots = []
#     busy_slots = get_busy_slots()

#     today = datetime.now()

#     for day_offset in range(SEARCH_DAYS):

#         current_day = today + timedelta(days=day_offset)

#         for hour in range(
#             WORKING_HOURS["start"],
#             WORKING_HOURS["end"]
#         ):

#             slot = datetime(
#                 current_day.year,
#                 current_day.month,
#                 current_day.day,
#                 hour,
#                 0
#             )

#             formatted_slot = slot.strftime("%A %I:%M %p")

#             if formatted_slot not in busy_slots:
#                 slots.append(formatted_slot)

#     print("\n===== AVAILABLE SLOTS =====")

#     for slot in slots:
#         print(slot)

#     print("===========================\n")

#     return slots


# def get_alternative_slots(best_slot, available_slots):

#     if best_slot not in available_slots:
#         return available_slots[:3]

#     index = available_slots.index(best_slot)

#     alternatives = []

#     for slot in available_slots[index + 1:]:

#         alternatives.append(slot)

#         if len(alternatives) == 3:
#             break

#     if len(alternatives) < 3:

#         for slot in available_slots:

#             if slot == best_slot:
#                 continue

#             if slot not in alternatives:
#                 alternatives.append(slot)

#             if len(alternatives) == 3:
#                 break

#     return alternatives


from datetime import datetime, timedelta

from services.calendar_service import get_busy_slots
from config import (
    WORKING_HOURS,
    SEARCH_DAYS
)


def get_available_slots():

    slots = []
    busy_slots = get_busy_slots()

    today = datetime.now()

    print("\n===== BUILDING AVAILABLE SLOTS =====")

    for day_offset in range(SEARCH_DAYS):

        current_day = today + timedelta(days=day_offset)

        for hour in range(
            WORKING_HOURS["start"],
            WORKING_HOURS["end"]
        ):

            slot_datetime = datetime(
                current_day.year,
                current_day.month,
                current_day.day,
                hour,
                0
            )

            display_slot = slot_datetime.strftime("%A %I:%M %p")

            if display_slot in busy_slots:
                continue

            slots.append(display_slot)

    print("\n===== AVAILABLE SLOTS =====")

    for slot in slots:
        print(slot)

    print("===========================\n")

    return slots


def get_alternative_slots(best_slot, available_slots):

    if not available_slots:
        return []

    if best_slot not in available_slots:
        return available_slots[:3]

    index = available_slots.index(best_slot)

    alternatives = []

    # Next available slots
    for slot in available_slots[index + 1:]:

        if slot == best_slot:
            continue

        alternatives.append(slot)

        if len(alternatives) == 3:
            break

    # Wrap around if required
    if len(alternatives) < 3:

        for slot in available_slots:

            if slot == best_slot:
                continue

            if slot not in alternatives:
                alternatives.append(slot)

            if len(alternatives) == 3:
                break

    return alternatives
