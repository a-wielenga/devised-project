import random

time_slots = ["10:30", "11:00", "11:30", "12:00"]

staff = ["A", "B", "C", "D", "E"]

random.shuffle(staff)

# print(staff)

schedule = dict(zip(time_slots, staff))
# zip pairs items from two lists into tuples e.g. ("10:30", "A")
# dict converts those pairs into a dictionary
# combines the two lists into a dictionary

# print(schedule)

for time, staff in schedule.items():
    print(f"{time} -> {staff}") #f = formatted string
    # The 'f' tells Python to replace {time} with the value of the variable time



