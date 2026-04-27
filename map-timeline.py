import tkinter as tk
from tkinter import ttk
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

# Store map scale + offset
map_scale = 1
map_offset_x = 0
map_offset_y = 0

# Define locations in original image coordinates
locations = {
    "Admissions": (2100, 2850),
    "FerrisWheel": (2530, 2300),
    "HorseCarousel": (700, 1930),
    "CarsTrack": (1400, 1260),
    "RollerCoaster": (2050, 550),
    "BigSwing": (3660, 640)
}


staff_colours = {
    "Staff A": "red",
    "Staff B": "orange",
    "Staff C": "green",
    "Staff D": "blue",
    "Staff E": "purple"
}


schedule = {
    "Admissions": [
        ("09:30", "17:30", "Staff A"),
    ],
    "FerrisWheel": [
        ("10:30", "12:00", "Staff B"),
        ("12:00", "13:00", "Staff C")
    ],
    "HorseCarousel": [
        ("10:30", "12:30", "Staff D"),
        ("12:30", "00:00", "Staff E")
    ],
    "CarsTrack": [
        ("14:00", "16:00", "Staff B"),
    ]
}


def time_to_minutes(tstr):
    hours, minutes = map(int, tstr.split(":"))
    return hours * 60 + minutes

def get_staff_for_location(location_name, t):
    if location_name not in schedule:
        return None

    for start_str, end_str, staff in schedule[location_name]:
        start = time_to_minutes(start_str)
        end = time_to_minutes(end_str)

        if end == 0:
            end = 1440

        if start <= t < end:
            return staff

    return None


current_time = 0

def draw_location_dots():
    map_canvas.delete("location_dot")
    map_canvas.delete("location_label")

    for location_name, (orig_x, orig_y) in locations.items():
        staff_name = get_staff_for_location(location_name, current_time)

        if staff_name is None:
            continue

        x = map_offset_x + orig_x * map_scale
        y = map_offset_y + orig_y * map_scale

        r = 15
        colour = staff_colours.get(staff_name, "yellow")

        # Dot
        map_canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill=colour,
            outline="black",
            width=2,
            tags="location_dot"
        )

        # Label above dot
        map_canvas.create_text(
            x, y - 25,
            text=staff_name,
            fill="black",
            font=("Arial", 12, "bold"),
            tags="location_label"
        )

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
    resized = original_map.resize((new_w, new_h), Image.LANCZOS) # LANCZOS keeps the image sharp when window resizes
    map_img_resized = ImageTk.PhotoImage(resized)

    # Update reference
    map_canvas.image = map_img_resized

    # Clear old map
    map_canvas.delete("map")

    # Centre the image
    x_offset = (canvas_width - new_w) // 2
    y_offset = (canvas_height - new_h) // 2

    map_canvas.create_image(x_offset, y_offset, anchor="nw",
                            image=map_img_resized, tags="map")

    # Keep map behind markers
    map_canvas.tag_lower("map")

    global map_scale, map_offset_x, map_offset_y
    map_scale = scale
    map_offset_x = x_offset
    map_offset_y = y_offset

    draw_location_dots()


map_canvas.bind("<Configure>", resize_map)


def update_positions(t):
    global current_time
    current_time = int(t)

    # If the scrubber hits 1440 (24:00), DISPLAY 00:00
    if current_time == 1440:
        display_hours = 0
        display_minutes = 0
    else:
        display_hours = current_time // 60
        display_minutes = current_time % 60

    # Update the time label using the display values
    time_display.config(text=f"{display_hours:02d}:{display_minutes:02d}")

    draw_location_dots()

time_display = tk.Label(right_container, text="00:00", font=("Arial", 14, "bold"))
time_display.pack()

# Scrubber
scrubber = tk.Scale(
    right_container,
    from_=0,
    to=1440,
    orient="horizontal",
    resolution=30,     # moves in 30-minute steps
    # tickinterval=30,   # optional: shows ticks every 30 minutes
    command=lambda v: update_positions(v),
    showvalue=False
)
scrubber.pack(fill="x", pady=10)

root.mainloop()
