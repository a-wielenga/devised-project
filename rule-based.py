# Rules:
# cannot use the same staff twice in a row
# pick the first staff member who is NOT the same as last used

import random

time_slots = ["10:30", "11:00", "11:30", "12:00"]

staff = ["A", "B", "C", "D", "E"]

schedule = {}
last_used = None

for slot in time_slots:
    for person in staff:
        if person != last_used:
            schedule[slot] = person
            last_used = person   # Reset this value
            # random.shuffle(staff) # Shuffles member of staff first in the list
            break

# Print the schedule
for slot, person in schedule.items():
    print(f"{slot} → {person}")
