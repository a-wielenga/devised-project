import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

root = tk.Tk()
root.title("Shift Manager")
root.state("zoomed")
root.minsize(800, 600)


def add_shift_to_cell(cell, time_text, employee, colour="#8ecae6"):
    block = tk.Frame(cell, bg=colour, bd=1, relief="solid")
    block.pack(fill="x", padx=2, pady=2)

    tk.Label(
        block,
        text=time_text,
        bg=colour,
        font=("Arial", 8, "bold"),
        anchor="w"
    ).pack(fill="x", padx=3, pady=(3, 0))

    tk.Label(
        block,
        text=employee,
        bg=colour,
        font=("Arial", 8),
        anchor="w"
    ).pack(fill="x", padx=3, pady=(0, 3))


class ShiftBlock(tk.Frame):
    def __init__(self, parent, employee, date, time_range, colour="#8ecae6"):
        super().__init__(parent, bg=colour, bd=1, relief="solid")

        tk.Label(self, text=employee, bg=colour,
                 font=("Arial", 12, "bold")).pack(anchor="w", padx=6, pady=(6, 0))

        tk.Label(self, text=date, bg=colour,
                 font=("Arial", 10)).pack(anchor="w", padx=6)

        tk.Label(self, text=time_range, bg=colour,
                 font=("Arial", 10)).pack(anchor="w", padx=6, pady=(0, 6))


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

tk.Label(right_container, text="Calendar",
         font=("Arial", 16, "bold")).pack(anchor="w")

calendar_outer = tk.Frame(right_container)
calendar_outer.pack(fill="both", expand=True, pady=10)



cal_canvas = tk.Canvas(calendar_outer)
cal_canvas.grid(row=0, column=0, sticky="nsew")

cal_y_scroll = ttk.Scrollbar(calendar_outer, orient="vertical", command=cal_canvas.yview)
cal_y_scroll.grid(row=0, column=1, sticky="ns")

cal_x_scroll = ttk.Scrollbar(calendar_outer, orient="horizontal", command=cal_canvas.xview)
cal_x_scroll.grid(row=1, column=0, sticky="ew")

calendar_frame = tk.Frame(cal_canvas)
cal_canvas.create_window((20, 0), window=calendar_frame, anchor="nw")

cal_canvas.configure(yscrollcommand=cal_y_scroll.set, xscrollcommand=cal_x_scroll.set)

calendar_outer.grid_columnconfigure(0, weight=1)
calendar_outer.grid_rowconfigure(0, weight=1)



categories = [
    "Team Leader",
    "Team Member"
]

start_date = datetime(2026, 5, 1)
num_days = 14

dates = [
    (start_date + timedelta(days=i)).strftime("%a %d %b")
    for i in range(num_days)
]



for col, d in enumerate(dates):
    tk.Label(calendar_frame, text=d, borderwidth=1, relief="flat",
             height=2, width=12).grid(row=0, column=col, sticky="nsew")

current_row = 1
category_shift_rows = {}
calendar_cells = {}

for cat in categories:


    tk.Label(calendar_frame, text=cat, bg="#d9d9d9",
             font=("Arial", 11, "bold"), anchor="w",
             borderwidth=1, relief="solid").grid(
                 row=current_row, column=0, columnspan=len(dates),
                 sticky="nsew"
             )
    current_row += 1


    for col in range(len(dates)):
        cell = tk.Frame(calendar_frame, borderwidth=1, relief="solid")
        cell.grid(row=current_row, column=col, sticky="nsew")
        calendar_cells[(current_row, col)] = cell

    category_shift_rows[cat] = current_row
    current_row += 1


sat_col = 1


cell = calendar_cells[(category_shift_rows["Team Leader"], sat_col)]
add_shift_to_cell(cell, "09:00 - 17:00", "Example User")


cell = calendar_cells[(category_shift_rows["Team Member"], sat_col)]
add_shift_to_cell(cell, "09:30 - 17:00", "Example User")
add_shift_to_cell(cell, "09:30 - 17:00", "Example User")
add_shift_to_cell(cell, "09:30 - 17:00", "Example User")

root.mainloop()
