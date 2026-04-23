import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

root = tk.Tk()
root.title("Shift Manager")
root.state("zoomed")
root.minsize(800, 600)

class ShiftBlock(tk.Frame):
    def __init__(self, parent, role, date, time_range, colour="#8ecae6"):
        super().__init__(parent, bg=colour, bd=1, relief="solid")

        tk.Label(self, text=role, bg=colour,
                 font=("Arial", 12, "bold")).pack(anchor="w", padx=6, pady=(6, 0))

        tk.Label(self, text=date, bg=colour,
                 font=("Arial", 10)).pack(anchor="w", padx=6)

        tk.Label(self, text=time_range, bg=colour,
                 font=("Arial", 10)).pack(anchor="w", padx=6, pady=(0, 6))


def add_shift_to_calendar(parent, column, start_hour, end_hour, colour, role, time_text):
    block = tk.Frame(parent, bg=colour, bd=1, relief="solid")

    tk.Label(
        block,
        text=role,
        bg=colour,
        font=("Arial", 10, "bold"),
        anchor="w",
        justify="left",
        wraplength=75
    ).pack(fill="x", padx=3, pady=(3, 0))

    tk.Label(
        block,
        text=time_text,
        bg=colour,
        font=("Arial", 8),
        anchor="w",
        justify="left",
        wraplength=75
    ).pack(fill="x", padx=3, pady=(0, 3))

    block.grid(
        row=start_hour + 1,
        column=column,
        rowspan=(end_hour - start_hour),
        sticky="nsew",
        padx=1,
        pady=1
    )


sidebar = tk.Frame(root, bg="#2c3e50", width=175)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

buttons = [
    "My Shifts", "Calendar", "Available Shifts",
    "Staff", "Rotas", "Timesheets"
]

for i, b in enumerate(buttons):
    tk.Button(
        sidebar, text=b, bg="#34495e", fg="white",
        relief="flat", height=2
    ).pack(fill="x", padx=10, pady=(10 if i == 0 else 5, 5))


main = tk.Frame(root, bg="#228097")
main.pack(side="left", fill="both", expand=True)

main.grid_columnconfigure(0, weight=1)
main.grid_columnconfigure(1, weight=3)
main.grid_rowconfigure(0, weight=1)


left_container = tk.Frame(main, bg="white")
left_container.grid(row=0, column=0, sticky="nswe", padx=(20, 10), pady=20)

tk.Label(left_container, text="My Next Shifts",
         font=("Arial", 16, "bold")).pack(anchor="w")

shift_frame = tk.Frame(left_container)
shift_frame.pack(fill="both", expand=True, pady=10)

shift_canvas = tk.Canvas(shift_frame)
shift_scrollbar = ttk.Scrollbar(shift_frame, orient="vertical", command=shift_canvas.yview)
shift_list_frame = tk.Frame(shift_canvas)

shift_list_frame.bind(
    "<Configure>",
    lambda e: shift_canvas.configure(scrollregion=shift_canvas.bbox("all"))
)

shift_canvas.create_window((0, 0), window=shift_list_frame, anchor="nw", tags="shift_window")
shift_canvas.bind(
    "<Configure>",
    lambda e: shift_canvas.itemconfig("shift_window", width=e.width)
)
shift_canvas.configure(yscrollcommand=shift_scrollbar.set)

shift_canvas.pack(side="left", fill="both", expand=True)
shift_scrollbar.pack(side="right", fill="y")


right_container = tk.Frame(main, bg="white")
right_container.grid(row=0, column=1, sticky="nswe", padx=(10, 20), pady=20)

tk.Label(right_container, text="Calendar",
         font=("Arial", 16, "bold")).pack(anchor="w")

calendar_outer = tk.Frame(right_container)
calendar_outer.pack(fill="both", expand=True, pady=10)

time_canvas = tk.Canvas(calendar_outer, width=80)
time_canvas.grid(row=0, column=0, sticky="ns")

time_frame = tk.Frame(time_canvas)
time_canvas.create_window((0, 0), window=time_frame, anchor="nw")

cal_canvas = tk.Canvas(calendar_outer)
cal_canvas.grid(row=0, column=1, sticky="nsew")

cal_y_scroll = ttk.Scrollbar(calendar_outer, orient="vertical")
cal_y_scroll.grid(row=0, column=2, sticky="ns")

cal_x_scroll = ttk.Scrollbar(calendar_outer, orient="horizontal", command=cal_canvas.xview)
cal_x_scroll.grid(row=1, column=1, sticky="ew")

calendar_frame = tk.Frame(cal_canvas)
cal_canvas.create_window((0, 0), window=calendar_frame, anchor="nw")

def sync_scroll(*args): # https://www.w3schools.com/python/python_args_kwargs.asp
    cal_canvas.yview(*args)
    time_canvas.yview(*args)


cal_canvas.configure(yscrollcommand=cal_y_scroll.set, xscrollcommand=cal_x_scroll.set)
time_canvas.configure(yscrollcommand=cal_y_scroll.set)
cal_y_scroll.configure(command=sync_scroll)


def match_heights():
    cal_bbox = cal_canvas.bbox("all")
    time_bbox = time_canvas.bbox("all")

    if not cal_bbox or not time_bbox:
        return

    cal_h = cal_bbox[3]
    time_h = time_bbox[3]
    max_h = max(cal_h, time_h)

    cal_canvas.configure(scrollregion=(0, 0, cal_bbox[2], max_h))
    time_canvas.configure(scrollregion=(0, 0, time_bbox[2], max_h))


calendar_frame.bind("<Configure>", lambda e: match_heights())
time_frame.bind("<Configure>", lambda e: match_heights())

calendar_outer.grid_columnconfigure(1, weight=1)
calendar_outer.grid_rowconfigure(0, weight=1)


start_date = datetime(2026, 5, 1)   # 1st May 2026
num_days = 14                       # two weeks

dates = [
    (start_date + timedelta(days=i)).strftime("%a %d %b")
    for i in range(num_days)
]

times = [f"{h:02d}:00" for h in range(24)]



tk.Label(time_frame, text="", width=20, height=1).grid(row=0, column=0)

for i, t in enumerate(times, start=1):
    tk.Label(time_frame, text=t, width=12, height=2).grid(row=i, column=0, sticky="w")



for col, d in enumerate(dates):
    tk.Label(calendar_frame, text=d, borderwidth=1, relief="flat",
             height=2, width=12).grid(row=0, column=col)


for row, t in enumerate(times, start=1):
    for col in range(len(dates)):
        tk.Label(calendar_frame, text="", borderwidth=1, relief="solid",
                 width=12, height=2).grid(row=row, column=col)


shifts = [
    ("Example Shift", "Fri, 1 May 2026", "09:00 - 17:00"),
] * 10

shift_background_colour = "#89ABCD"


for role, date, time_range in shifts:
    ShiftBlock(shift_list_frame, role, date, time_range, shift_background_colour).pack(fill="x", padx=10, pady=5)


# Add to calendar (example positions)
add_shift_to_calendar(
    calendar_frame,
    1, # column (day)
    9, # start hour
    17, # finish hour
    shift_background_colour,
    "Example Shift",
    "09:00 - 17:00"
)


root.mainloop()
