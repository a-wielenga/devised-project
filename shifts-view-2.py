import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Shift Manager")
root.state("zoomed")
root.minsize(800, 600)

# Make a shift block
class ShiftBlock(tk.Frame):
    def __init__(self, parent, role, date, time_range, colour="#8ecae6"):
        super().__init__(parent, bg=colour, bd=1, relief="solid")

        tk.Label(self, text=role, bg=colour,
                 font=("Arial", 12, "bold")).pack(anchor="w", padx=6, pady=(6, 0))

        tk.Label(self, text=date, bg=colour,
                 font=("Arial", 10)).pack(anchor="w", padx=6)

        tk.Label(self, text=time_range, bg=colour,
                 font=("Arial", 10)).pack(anchor="w", padx=6, pady=(0, 6))

# Sidebar
sidebar = tk.Frame(root, bg="#2c3e50", width=175)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)  # keep the 300px width

buttons = [
    "My Shifts", "Calendar", "Available Shifts",
    "Staff", "Rotas", "Timesheet"
]

for i, b in enumerate(buttons):
    tk.Button(
        sidebar, text=b, bg="#34495e", fg="white",
        relief="flat", height=2
    ).pack(fill="x", padx=10, pady=(10 if i == 0 else 5, 5))

# Main
main = tk.Frame(root, bg="#228097")
main.pack(side="left", fill="both", expand=True)

main.grid_columnconfigure(0, weight=1)
main.grid_rowconfigure(0, weight=1)

# Scrollable shift list
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


# Add shifts
shifts = [
    ("Example Shift", "Fri, 1 May 2026", "09:00 - 17:00"),
] * 10

shift_background_colour = "#8ecae6"

# Add to left list
for role, date, time_range in shifts:
    ShiftBlock(shift_list_frame, role, date, time_range, shift_background_colour).pack(fill="x", padx=10, pady=5)


root.mainloop()
