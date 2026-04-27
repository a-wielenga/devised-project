import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Shift Manager")
root.state("zoomed")
root.minsize(800, 600)

# Sidebar
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

# Main content area
main = tk.Frame(root, bg="#228097")
main.pack(side="left", fill="both", expand=True)

main.grid_columnconfigure(0, weight=1)
main.grid_rowconfigure(0, weight=1)

# Content container
right_container = tk.Frame(main, bg="white")
right_container.grid(row=0, column=0, sticky="nswe", padx=(20, 10), pady=20)

tk.Label(right_container, text="Map",
         font=("Arial", 16, "bold")).pack(anchor="w")

# Canvas for map
map_canvas = tk.Canvas(right_container, bg="white")
map_canvas.pack(fill="both", expand=True, pady=10)

# Load original map image
original_map = Image.open("maps/amusement-park-map.png")

# Draw initial map
map_img = ImageTk.PhotoImage(original_map)
map_canvas.image = map_img
map_canvas.create_image(0, 0, anchor="nw", image=map_img, tags="map")

# Resize map
def resize_map(event):
    canvas_width = event.width
    canvas_height = event.height

    # Original image size
    img_w, img_h = original_map.size

    # Fit to canvas while keeping aspect ratio
    scale = min(canvas_width / img_w, canvas_height / img_h)

    # New size
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    # Resize the image
    resized = original_map.resize((new_w, new_h), Image.LANCZOS)
    map_img_resized = ImageTk.PhotoImage(resized)

    # Update reference
    map_canvas.image = map_img_resized

    # Clear old map
    map_canvas.delete("map")

    # Center the image
    x_offset = (canvas_width - new_w) // 2
    y_offset = (canvas_height - new_h) // 2

    map_canvas.create_image(x_offset, y_offset, anchor="nw",
                            image=map_img_resized, tags="map")

    # Keep map behind markers
    map_canvas.tag_lower("map")


map_canvas.bind("<Configure>", resize_map)


def update_positions(t):
    t = int(t)

    # If the scrubber hits 1440 (24:00), DISPLAY 00:00
    if t == 1440:
        display_hours = 0
        display_minutes = 0
    else:
        display_hours = t // 60
        display_minutes = t % 60

    # Update the time label using the display values
    time_display.config(text=f"{display_hours:02d}:{display_minutes:02d}")

time_display = tk.Label(right_container, text="00:00", font=("Arial", 14, "bold"))
time_display.pack()

# Scrubber
scrubber = tk.Scale(
    right_container,
    from_=0,
    to=1440,
    orient="horizontal",
    command=lambda v: update_positions(v),
    showvalue=False
)
scrubber.pack(fill="x", pady=10)

root.mainloop()
