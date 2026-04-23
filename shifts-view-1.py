import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Shift Manager")
root.state("zoomed")
root.minsize(800, 600)

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


main = tk.Frame(root, bg="#228097")
main.pack(side="left", fill="both", expand=True)

main.grid_columnconfigure(0, weight=1)
main.grid_rowconfigure(0, weight=1)

left_container = tk.Frame(main, bg="white")
left_container.grid(row=0, column=0, sticky="nswe", padx=(20, 10), pady=20)

tk.Label(left_container, text="My Next Shifts", font=("Arial", 16, "bold")).pack(anchor="w")

shift_frame = tk.Frame(left_container)
shift_frame.pack(fill="both", expand=True, pady=10)

shift_canvas = tk.Canvas(shift_frame)
shift_scrollbar = ttk.Scrollbar(shift_frame, orient="vertical", command=shift_canvas.yview)
shift_list_frame = tk.Frame(shift_canvas)

shift_list_frame.bind(
    "<Configure>",
    lambda e: shift_canvas.configure(scrollregion=shift_canvas.bbox("all"))
)

shift_canvas.create_window((0, 0), window=shift_list_frame, anchor="nw")
shift_canvas.configure(yscrollcommand=shift_scrollbar.set)

shift_canvas.pack(side="left", fill="both", expand=True)
shift_scrollbar.pack(side="right", fill="y")

for i in range(40):
    tk.Label(shift_list_frame, text=f"Shift: 09:00 - 17:00", anchor="w").pack(fill="x", pady=2)

root.mainloop()
