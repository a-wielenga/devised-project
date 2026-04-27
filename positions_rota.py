import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

root = tk.Tk()
root.title("Shift Manager")
root.state("zoomed")
root.minsize(800, 600)

class ShiftBlock(tk.Frame):
    def __init__(self, parent, employee, date, time_range, colour="#8ecae6"):
        super().__init__(parent, bg=colour, bd=1, relief="solid")

        tk.Label(self, text=employee, bg=colour,
                 font=("Arial", 12, "bold")).pack(anchor="w", padx=6, pady=(6, 0))

        tk.Label(self, text=date, bg=colour,
                 font=("Arial", 10)).pack(anchor="w", padx=6)

        tk.Label(self, text=time_range, bg=colour,
                 font=("Arial", 10)).pack(anchor="w", padx=6, pady=(0, 6))


def time_to_slot(time_str):
    """Convert HH:MM into a 30-minute slot index."""
    h, m = map(int, time_str.split(":"))
    return h * 2 + (1 if m >= 30 else 0)


def add_shift_to_calendar(position, start, end, colour, employee):
    pos_index = positions.index(position)
    start_slot = time_to_slot(start)
    end_slot = time_to_slot(end)
    span = (end_slot - start_slot)

    block = tk.Frame(calendar_frame, bg=colour, bd=1, relief="solid")

    tk.Label(block, text=employee, bg=colour,
             font=("Arial", 10, "bold"), anchor="w").pack(fill="x", padx=3, pady=(3, 0))

    tk.Label(block, text=f"{start} - {end}", bg=colour,
             font=("Arial", 8), anchor="w").pack(fill="x", padx=3, pady=(0, 3))

    block.grid(
        row=pos_index + 1,
        column=start_slot + 1,
        columnspan=span,
        sticky="nsew",
        padx=1,
        pady=1
    )


sidebar = tk.Frame(root, bg="#2c3e50", width=175)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

buttons = [
    "My Shifts", "Calendar", "Available Shifts",
    "Staff", "Rotas", "Timesheet"
]

for i, b in enumerate(buttons):
    tk.Button(
        sidebar, text=b, bg="#34495e", fg="white",
        relief="flat", height=2
    ).pack(fill="x", padx=10, pady=(10 if i == 0 else 5, 5))

main = tk.Frame(root, bg="#228097")
main.pack(side="left", fill="both", expand=True)

main.grid_columnconfigure(0, weight=1)
main.grid_rowconfigure(0, weight=1)

right_container = tk.Frame(main, bg="white")
right_container.grid(row=0, column=0, sticky="nswe", padx=(20, 10), pady=20)

tk.Label(right_container, text="Rota",
         font=("Arial", 16, "bold")).pack(anchor="w")

calendar_outer = tk.Frame(right_container)
calendar_outer.pack(fill="both", expand=True, pady=10)

static_col = tk.Frame(calendar_outer)
static_col.grid(row=0, column=0, sticky="ns")


cal_canvas = tk.Canvas(calendar_outer)
cal_canvas.grid(row=0, column=1, sticky="nsew")

cal_y_scroll = ttk.Scrollbar(calendar_outer, orient="vertical", command=cal_canvas.yview)
cal_y_scroll.grid(row=0, column=2, sticky="ns")

cal_x_scroll = ttk.Scrollbar(calendar_outer, orient="horizontal", command=cal_canvas.xview)
cal_x_scroll.grid(row=1, column=1, sticky="ew")

calendar_outer.grid_columnconfigure(1, weight=1)
calendar_outer.grid_rowconfigure(0, weight=1)

calendar_frame = tk.Frame(cal_canvas)
cal_canvas.create_window((0, 0), window=calendar_frame, anchor="nw")

cal_canvas.configure(xscrollcommand=cal_x_scroll.set, yscrollcommand=cal_y_scroll.set)

calendar_frame.bind(
    "<Configure>",
    lambda e: cal_canvas.configure(scrollregion=cal_canvas.bbox("all"))
)

# 30‑minute time slots
time_slots = []
t = datetime(2026, 5, 1, 0, 0)
for _ in range(49):
    time_slots.append(t.strftime("%H:%M"))
    t += timedelta(minutes=30)

# Position labels
positions = [
    "Position 1", "Position 2", "Position 3", "Position 4", "Position 5"
]


tk.Label(static_col, text="", width=15, height=2).grid(row=0, column=0)

for row, pos in enumerate(positions, start=1):
    tk.Label(static_col, text=pos, borderwidth=1, relief="flat",
             width=15, height=3, anchor="w").grid(row=row, column=0, sticky="w", padx=10)


for col, ts in enumerate(time_slots):
    tk.Label(calendar_frame, text=ts, borderwidth=1, relief="solid",
             height=2, width=10).grid(row=0, column=col+1)

# Grid cells
cell_labels = []

for row, pos in enumerate(positions, start=1):

    row_cells = []

    for col in range(len(time_slots)):
        cell = tk.Label(
            calendar_frame,
            text="",
            borderwidth=1,
            relief="solid",
            width=10,
            height=3
        )
        cell.grid(row=row, column=col+1, sticky="nsew")
        row_cells.append(cell)

    cell_labels.append(row_cells)


add_shift_to_calendar(
    position="Position 1",
    start="10:30",
    end="12:00",
    colour="#8ecae6",
    employee="Example User"
)

add_shift_to_calendar(
    position="Position 2",
    start="12:00",
    end="13:00",
    colour="#8ecae6",
    employee="Example User"
)

root.mainloop()
