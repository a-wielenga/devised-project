import mysql.connector
import tkinter as tk
from tkinter import messagebox # https://docs.python.org/3/library/tkinter.messagebox.html
from argon2 import PasswordHasher
from tkinter import ttk
from datetime import datetime, timedelta
from PIL import Image, ImageTk

# Login Page
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure 2 equal columns
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Left side
        left_frame = tk.Frame(self, bg="#48567F")
        left_frame.grid(row=0, column=0, sticky="nsew")

        welcome_label = tk.Label(
            left_frame,
            text="Welcome to {name TBC}",
            fg="white",
            bg="#48567F",
            font=("Arial", 25, "bold"),
        )
        welcome_label.place(relx=0.5, rely=0.2, anchor="center")  # horizontally middle, 1/5 down

        # Right side
        right_frame = tk.Frame(self, bg="#89ABCD")
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Title
        sign_in_label = tk.Label(
            right_frame,
            text="Sign In",
            font=("Arial", 25, "bold"),
            bg="#89ABCD"
        )
        sign_in_label.place(relx=0.5, rely=0.2, anchor="center")  # horizontally middle, 1/5 down

        # Container for form
        form_frame = tk.Frame(right_frame, bg="#89ABCD")
        form_frame.place(relx=0.5, rely=0.35, anchor="n")

        # Email
        self.email_entry = PlaceholderEntry(form_frame, placeholder="Email address", width=50)
        self.email_entry.grid(row=1, column=0, pady=5)

        # Password
        self.password_entry = PlaceholderEntry(
            form_frame,
            placeholder="Password",
            width=50,
            is_password=True
        )

        self.password_entry.grid(row=3, column=0, pady=15)

        # Eye toggle button
        self.show_password = False
        toggle_btn = tk.Button(
            form_frame,
            text="👁",
            command=self.toggle_password,
            relief="flat",
            bg="#89ABCD"
        )
        toggle_btn.grid(row=3, column=1, padx=15)

        # Login button
        login_button = tk.Button(
            form_frame,
            text="Login",
            command=self.login,
            width=20,
            bg="#48567F",
            fg="white"
        )
        login_button.grid(row=4, column=0, columnspan=2, pady=20)

    # Toggle password visibility
    def toggle_password(self):
        self.show_password = not self.show_password
        self.password_entry.config(show="" if self.show_password else "*")

    # Login process inc SQL
    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        sql = "SELECT password_hash FROM Users WHERE email_address = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()

        if result is None:
            messagebox.showerror("Login Failed", "Email not found")
            return

        stored_hash = result[0]

        try:
            if ph.verify(stored_hash, password):
                messagebox.showinfo("Success", "Login successful")
                self.controller.show_frame("Dashboard")
            else:
                messagebox.showerror("Login Failed", "Incorrect password")
        except:
            messagebox.showerror("Login Failed", "Incorrect password")

# Dashboard
class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#228097")
        self.controller = controller

        # Sidebar
        sidebar = Sidebar(self, controller)
        sidebar.pack(side="left", fill="y")

        # Main content
        main = tk.Frame(self, bg="#228097")
        main.pack(side="left", fill="both", expand=True)

        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=3)
        main.grid_rowconfigure(0, weight=1)

        # Shift list
        shift_list = ShiftList(main)
        shift_list.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Add shifts
        shifts = [
            ("Example Shift", "Fri, 1 May 2026", "09:00 - 17:00"),
        ] * 10

        for role, date, time_range in shifts:
            shift_list.add_shift(role, date, time_range)
        
        # Calendar
        calendar = MyShiftCalendar(
            main,
            start_date=datetime(2026, 5, 1),
            num_days=14)
        calendar.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        calendar.add_shift_to_calendar(
                1, # column (day)
                9, # start hour
                17, # finish hour
                "#89ABCD",
                "Example Shift",
                "09:00 - 17:00"
        )

class MyShiftsListPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Sidebar
        sidebar = Sidebar(self, controller)
        sidebar.pack(side="left", fill="y")

        # Main container / background
        main = tk.Frame(self, bg="#228097")
        main.pack(fill="both", expand=True)

        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # White container
        left_container = tk.Frame(main, bg="white")
        left_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Shift List class
        shift_list = ShiftList(left_container)
        shift_list.pack(fill="both", expand=True)

        # Add example shifts
        shifts = [
            ("Example Shift", "Fri, 1 May 2026", "09:00 - 17:00"),
        ] * 10

        for role, date, time_range in shifts:
            shift_list.add_shift(role, date, time_range)

class MyShiftsCalendarPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Sidebar
        sidebar = Sidebar(self, controller)
        sidebar.pack(side="left", fill="y")

        # Main container / background
        main = tk.Frame(self, bg="#228097")
        main.pack(fill="both", expand=True)

        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)
        
        # Calendar
        calendar = MyShiftCalendar(
            main,
            start_date=datetime(2026, 5, 1),
            num_days=14)
        calendar.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        calendar.add_shift_to_calendar(
                1, # column (day)
                9, # start hour
                17, # finish hour
                "#89ABCD",
                "Example Shift",
                "09:00 - 17:00"
        )

class ShiftCategoryCalendarPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Sidebar
        sidebar = Sidebar(self, controller)
        sidebar.pack(side="left", fill="y")

        # Main container / background
        main = tk.Frame(self, bg="#228097")
        main.pack(side="left", fill="both", expand=True)

        # Allows areas to be expandable (horizontally & vertically)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # Outer container
        outer_container = tk.Frame(main, bg="white")
        outer_container.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        outer_container.grid_columnconfigure(0, weight=1)
        outer_container.grid_rowconfigure(0, weight=1)
        
        # Add spacing around content
        inner_container = tk.Frame(outer_container, bg="white")
        inner_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        tk.Label(inner_container, text="Calendar",
            font=("Arial", 16, "bold")).pack(anchor="w")

        # Scrollable calendar area
        calendar_outer = tk.Frame(inner_container)
        calendar_outer.pack(fill="both", expand=True, pady=20)

        cal_canvas = tk.Canvas(calendar_outer)
        cal_canvas.grid(row=0, column=0, sticky="nsew")

        # Scroll bars
        cal_y_scroll = ttk.Scrollbar(calendar_outer, orient="vertical", command=cal_canvas.yview)
        cal_y_scroll.grid(row=0, column=1, sticky="ns")

        cal_x_scroll = ttk.Scrollbar(calendar_outer, orient="horizontal", command=cal_canvas.xview)
        cal_x_scroll.grid(row=1, column=0, sticky="ew")

        # Actual calendar frame
        calendar_frame = tk.Frame(cal_canvas)
        cal_canvas.create_window((0, 0), window=calendar_frame, anchor="nw")

        cal_canvas.configure(yscrollcommand=cal_y_scroll.set, xscrollcommand=cal_x_scroll.set)

        calendar_outer.grid_columnconfigure(0, weight=1)
        calendar_outer.grid_rowconfigure(0, weight=1)

        # Categories
        self.categories = ["Team Leader", "Team Member"]

        start_date = datetime(2026, 5, 1)
        num_days = 14

        dates = [
            (start_date + timedelta(days=i)).strftime("%a %d %b")
            for i in range(num_days)
        ]

        # Date headers
        for col, d in enumerate(dates):
            tk.Label(calendar_frame, text=d, borderwidth=1, relief="flat",
                     height=2, width=12).grid(row=0, column=col, sticky="nsew")

        # Build category rows
        current_row = 1
        self.category_shift_rows = {}
        self.calendar_cells = {}


        for cat in self.categories:
            tk.Label(calendar_frame, text=cat, bg="#d9d9d9",
                     font=("Arial", 11, "bold"), anchor="w",
                     borderwidth=1, relief="solid").grid(
                         row=current_row, column=0, columnspan=len(dates),
                         sticky="nsew"
                     )
            current_row += 1

            # Adds a cell under each header
            for col in range(len(dates)):
                cell = tk.Frame(calendar_frame, borderwidth=1, relief="solid")
                cell.grid(row=current_row, column=col, sticky="nsew")
                self.calendar_cells[(current_row, col)] = cell

            self.category_shift_rows[cat] = current_row
            current_row += 1

        # Example shifts
        # cat, day_col, times, employee
        self.add_shift(0, 1, "09:00 - 17:00", "Example User")
        self.add_shift(1, 1, "09:30 - 17:00", "Example User")
        self.add_shift(1, 1, "09:30 - 17:00", "Example User")
        self.add_shift(1, 1, "09:30 - 17:00", "Example User")

    def add_shift(self, category_index, day_col, time_text, employee, colour="#8ecae6"):
        category = self.categories[category_index]
        row = self.category_shift_rows[category]
        cell = self.calendar_cells[(row, day_col)]

        # Checks if this is the first card so can create this spacing:
            # 2px
            # CARD
            # 2px
            # CARD
            # 2px
        is_first = not cell.winfo_children()
        top_pad = 2 if is_first else 0

        # Create the card
        block = tk.Frame(cell, bg=colour, bd=1, relief="solid")
        block.pack(fill="x", padx=2, pady=(top_pad, 2))

        # Add time label
        tk.Label(
            block, text=time_text, bg=colour,
            font=("Arial", 8, "bold"), anchor="w"
        ).pack(fill="x", padx=3, pady=(3, 0))

        # Add employee label
        tk.Label(
            block, text=employee, bg=colour,
            font=("Arial", 8), anchor="w"
        ).pack(fill="x", padx=3, pady=(0, 3))

class ShiftPositionsRotaPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Sidebar
        sidebar = Sidebar(self, controller)
        sidebar.pack(side="left", fill="y")

        # Main container / background
        main = tk.Frame(self, bg="#228097")
        main.pack(side="left", fill="both", expand=True)

        # Allows areas to be expandable (horizontally & vertically)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # Outer container
        outer_container = tk.Frame(main, bg="white")
        outer_container.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        outer_container.grid_columnconfigure(0, weight=1)
        outer_container.grid_rowconfigure(0, weight=1)
        
        # Add spacing around content
        inner_container = tk.Frame(outer_container, bg="white")
        inner_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        tk.Label(inner_container, text="Rota",
            font=("Arial", 16, "bold")).pack(anchor="w")

        calendar_outer = tk.Frame(inner_container)
        calendar_outer.pack(fill="both", expand=True, pady=10)

        # Positions column
        static_col = tk.Frame(calendar_outer)
        static_col.grid(row=0, column=0, sticky="ns")

        # Canvas for calendar
        cal_canvas = tk.Canvas(calendar_outer)
        cal_canvas.grid(row=0, column=1, sticky="nsew")

        # Scroll bars
        cal_y_scroll = ttk.Scrollbar(calendar_outer, orient="vertical", command=cal_canvas.yview)
        cal_y_scroll.grid(row=0, column=2, sticky="ns")

        cal_x_scroll = ttk.Scrollbar(calendar_outer, orient="horizontal", command=cal_canvas.xview)
        cal_x_scroll.grid(row=1, column=1, sticky="ew")

        calendar_outer.grid_columnconfigure(1, weight=1)
        calendar_outer.grid_rowconfigure(0, weight=1)

        # Time slots
        time_slots = []
        t = datetime(2026, 5, 1, 0, 0)
        for _ in range(49): # 00:00 to 00:00 (next day)
            time_slots.append(t.strftime("%H:%M"))
            t += timedelta(minutes=30)

        # Set default scroll position to roughly 09:00
        slot = time_slots.index("09:00")
        fraction = slot / len(time_slots)
        self.after(50, lambda: cal_canvas.xview_moveto(fraction)) # waits for 50ms until canvas drawn and then scrolls to 09:00

        # Frame for shifts
        calendar_frame = tk.Frame(cal_canvas)
        cal_canvas.create_window((0, 0), window=calendar_frame, anchor="nw")

        cal_canvas.configure(xscrollcommand=cal_x_scroll.set, yscrollcommand=cal_y_scroll.set)

        calendar_frame.bind(
            "<Configure>",
            lambda e: cal_canvas.configure(scrollregion=cal_canvas.bbox("all"))
        )

        # # Time slots
        # time_slots = []
        # t = datetime(2026, 5, 1, 0, 0)
        # for _ in range(49): # 00:00 to 00:00
        #     time_slots.append(t.strftime("%H:%M"))
        #     t += timedelta(minutes=30)

        # Positions
        positions = [
            "Position 1", "Position 2", "Position 3", "Position 4", "Position 5"
        ]

        # Moves position labels down (empty row)
        tk.Label(static_col, text="", width=15, height=2).grid(row=0, column=0)

        # Adds positions to each row
        for row, pos in enumerate(positions, start=1):
            tk.Label(static_col, text=pos, borderwidth=1, relief="flat",
                     width=15, height=3, anchor="w").grid(row=row, column=0, sticky="w", padx=10)

        # Adds the time slots
        for col, ts in enumerate(time_slots):
            tk.Label(calendar_frame, text=ts, borderwidth=1, relief="solid",
                     height=2, width=10).grid(row=0, column=col+1)
        
        # Creates the empty grid boxes
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

        # References for later
        self.calendar_frame = calendar_frame
        self.positions = positions
        self.time_slots = time_slots

        # Example shifts
        self.add_shift("Position 1", "10:30", "12:00", "#8ecae6", "Example User")
        self.add_shift("Position 2", "12:00", "13:00", "#8ecae6", "Example User")

    # Converts the time to a slot index
    def time_to_slot(self, time_str):
        h, m = map(int, time_str.split(":")) # split it from HH:MM so h=HH and m=MM
        return h * 2 + (1 if m >= 30 else 0)
        # each slot is 30m
        # 2 slots per hour
        # add 1 more slot if minutes are >= 30

    def add_shift(self, position, start, end, colour, employee):
        pos_index = self.positions.index(position) # gets the index of position for the suitable row
        start_slot = self.time_to_slot(start)
        end_slot = self.time_to_slot(end)
        span = end_slot - start_slot # how many boxes it should cover

        block = tk.Frame(self.calendar_frame, bg=colour, bd=1, relief="solid")

        tk.Label(block, text=employee, bg=colour,
                 font=("Arial", 10, "bold"), anchor="w").pack(fill="x", padx=3, pady=(3, 0))

        tk.Label(block, text=f"{start} - {end}", bg=colour,
                 font=("Arial", 8), anchor="w").pack(fill="x", padx=3, pady=(0, 3))

        block.grid(
            row=pos_index + 1, # increases index (considers time header row)
            column=start_slot + 1,
            columnspan=span,
            sticky="nsew",
            padx=1,
            pady=1
        )

class TimelineMapPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Sidebar
        sidebar = Sidebar(self, controller)
        sidebar.pack(side="left", fill="y")

        # Main container / background
        main = tk.Frame(self, bg="#228097")
        main.pack(side="left", fill="both", expand=True)

        # Allows areas to be expandable (horizontally & vertically)
        main.grid_columnconfigure(0, weight=1)
        main.grid_rowconfigure(0, weight=1)

        # Outer container
        outer_container = tk.Frame(main, bg="white")
        outer_container.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)

        outer_container.grid_columnconfigure(0, weight=1)
        outer_container.grid_rowconfigure(0, weight=1)
        
        # Add spacing around content
        inner_container = tk.Frame(outer_container, bg="white")
        inner_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        tk.Label(inner_container, text="Timeline Map",
            font=("Arial", 16, "bold")).pack(anchor="w")
                
        # Canvas for map
        self.map_canvas = tk.Canvas(inner_container, bg="white")
        self.map_canvas.pack(fill="both", expand=True, pady=10)

        # Load original map image
        self.original_map = Image.open("maps/amusement-park-map.png")

        # Draw initial map
        map_img = ImageTk.PhotoImage(self.original_map)
        self.map_canvas.image = map_img
        self.map_canvas.create_image(0, 0, anchor="nw", image=map_img, tags="map")

        # Store map scale + offset
        self.map_scale = 1
        self.map_offset_x = 0
        self.map_offset_y = 0

        # Define locations in original image coordinates
        self.locations = {
            "Admissions": (2100, 2850),
            "FerrisWheel": (2530, 2300),
            "HorseCarousel": (700, 1930),
            "CarsTrack": (1400, 1260),
            "RollerCoaster": (2050, 550),
            "BigSwing": (3660, 640)
        }


        self.staff_colours = {
            "Staff A": "red",
            "Staff B": "orange",
            "Staff C": "green",
            "Staff D": "blue",
            "Staff E": "purple"
        }


        self.schedule = {
            "Admissions": [
                ("09:30", "17:30", "Staff A"),
            ],
            "FerrisWheel": [
                ("10:30", "12:00", "Staff B"),
                ("12:00", "13:00", "Staff C")
            ],
            "HorseCarousel": [
                ("10:30", "12:30", "Staff D"),
                ("12:30", "16:30", "Staff E")
            ],
            "CarsTrack": [
                ("14:00", "16:00", "Staff B"),
            ]
        }


        def time_to_minutes(tstr):
            hours, minutes = map(int, tstr.split(":"))
            return hours * 60 + minutes

        def get_staff_for_location(location_name, t):
            if location_name not in self.schedule:
                return None

            for start_str, end_str, staff in self.schedule[location_name]:
                start = time_to_minutes(start_str)
                end = time_to_minutes(end_str)

                if end == 0:
                    end = 1440

                if start <= t < end:
                    return staff

            return None


        self.current_time = 0

        def draw_location_dots():
            self.map_canvas.delete("location_dot")
            self.map_canvas.delete("location_label")

            for location_name, (orig_x, orig_y) in self.locations.items():
                staff_name = get_staff_for_location(location_name, self.current_time)

                if staff_name is None:
                    continue

                x = self.map_offset_x + orig_x * self.map_scale
                y = self.map_offset_y + orig_y * self.map_scale

                r = 15
                colour = self.staff_colours.get(staff_name, "yellow")

                # Dot
                self.map_canvas.create_oval(
                    x - r, y - r, x + r, y + r,
                    fill=colour,
                    outline="black",
                    width=2,
                    tags="location_dot"
                )

                # Label above dot
                # Create the text first
                text_id = self.map_canvas.create_text(
                    x, y - 35,
                    text=staff_name,
                    fill="black",
                    font=("Arial", 12, "bold"),
                    tags="location_label"
                )

                # Get the bounding box of the text
                x1, y1, x2, y2 = self.map_canvas.bbox(text_id)

                # Add padding
                pad = 4

                # Draw rectangle behind the text
                rect_id = self.map_canvas.create_rectangle(
                    x1 - pad, y1 - pad, x2 + pad, y2 + pad,
                    fill="white",
                    outline="black",
                    tags="location_label"
                )

                # Make sure the text is above the rectangle
                self.map_canvas.tag_raise(text_id, rect_id)


        # Resize map
        def resize_map(event):
            canvas_width = event.width
            canvas_height = event.height

            # Original image size
            img_w, img_h = self.original_map.size

            # Fit to canvas while keeping aspect ratio
            scale = min(canvas_width / img_w, canvas_height / img_h)

            # New size
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)

            # Resize the image
            resized = self.original_map.resize((new_w, new_h), Image.LANCZOS) # LANCZOS keeps the image sharp when window resizes
            map_img_resized = ImageTk.PhotoImage(resized)

            # Update reference
            self.map_canvas.image = map_img_resized

            # Clear old map
            self.map_canvas.delete("map")

            # Centre the image
            x_offset = (canvas_width - new_w) // 2
            y_offset = (canvas_height - new_h) // 2

            self.map_canvas.create_image(
                x_offset, y_offset, anchor="nw",
                image=map_img_resized, tags="map")

            # Keep map behind markers
            self.map_canvas.tag_lower("map")

            self.map_scale = scale
            self.map_offset_x = x_offset
            self.map_offset_y = y_offset

            draw_location_dots()


        self.map_canvas.bind("<Configure>", resize_map)


        def update_positions(t):
            self.current_time = int(t)

            # If the scrubber hits 1440 (24:00), DISPLAY 00:00
            if self.current_time == 1440:
                display_hours = 0
                display_minutes = 0
            else:
                display_hours = self.current_time // 60
                display_minutes = self.current_time % 60

            # Update the time label using the display values
            time_display.config(text=f"{display_hours:02d}:{display_minutes:02d}")

            draw_location_dots()

        time_display = tk.Label(inner_container, text="00:00", font=("Arial", 14, "bold"))
        time_display.pack()

        # Scrubber
        scrubber = tk.Scale(
            inner_container,
            from_=0,
            to=1440,
            orient="horizontal",
            resolution=30,     # moves in 30-minute steps
            # tickinterval=30,   # optional: shows ticks every 30 minutes
            command=lambda v: update_positions(v),
            showvalue=False
        )
        scrubber.pack(fill="x", pady=10)

# Sidebar buttons
sidebar_buttons = [
    ("Dashboard", Dashboard),
    ("My Shifts List", MyShiftsListPage),
    ("Shift Calendar", MyShiftsCalendarPage),
    ("Rota", ShiftCategoryCalendarPage),
    ("Position Rota", ShiftPositionsRotaPage),
    ("Timeline Map", TimelineMapPage)
]

# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CreativeComputingMySQLROOT!",
    database="Application"
)

cursor = conn.cursor() # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor.html

# Hashing for Passwords - Argon2
ph = PasswordHasher()

# Place Holders
class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color="grey", is_password=False, **kwargs):
        super().__init__(master, **kwargs)
        # **kwargs = arbitrary keyword arguments - https://www.w3schools.com/python/python_args_kwargs.asp#:~:text=Arbitrary%20Keyword%20Arguments%20%2D%20**kwargs

        # Settings
        self.placeholder = placeholder
        self.placeholder_color = color # sets the placeholders to grey
        self.default_fg_color = self["fg"] # fg = foreground colour
        self.is_password = is_password
        self.show_char = "*" if is_password else "" # masks/unmasks password

        # Bind events
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        self.bind("<KeyRelease>", self._on_type)

        # Initially adds placeholder
        self._add_placeholder()

    # if the text is grey, delete the text, and if it's the password field, start password masking
    def _clear_placeholder(self, event=None):
        if self["fg"] == self.placeholder_color:
            self.delete(0, "end")
            self["fg"] = self.default_fg_color
            if self.is_password:
                self.config(show=self.show_char)

    # if entry is empty, show the placeholder and ensure the placeholder text isn't masked
    def _add_placeholder(self, event=None):
        if not self.get():
            self.config(show="")  # show text
            self.insert(0, self.placeholder)
            self["fg"] = self.placeholder_color

    # 
    def _on_type(self, event=None):
        if self["fg"] == self.placeholder_color: # checks if the foreground colour matches the colour for placeholder
            return  # stops the function if it the colours match (ignored typing until the placeholder text is clear)
        if self.is_password: # enabled masking when user enters text into password box
            self.config(show=self.show_char)

class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2c3e50", width=175)
        self.controller = controller
        self.pack_propagate(False)
        
        # # Side bar
        # sidebar = tk.Frame(self, bg="#2c3e50", width=175)
        # sidebar.pack(side="left", fill="y")
        # sidebar.pack_propagate(False)

        # Top buttons
        sidebar_frame = tk.Frame(self, bg="#2c3e50")
        sidebar_frame.pack(fill="x", pady=10)

        # for i, b in enumerate(buttons):
        #     tk.Button(
        #         sidebar_frame, text=b, bg="#34495e", fg="white",
        #         relief="flat", height=2
        #     ).pack(fill="x", padx=10, pady=(10 if i == 0 else 5, 5))

        for i, (label, page_class) in enumerate(sidebar_buttons):
            tk.Button(
                sidebar_frame,
                text=label,
                bg="#34495e",
                fg="white",
                relief="flat",
                height=2,
                command=lambda p=page_class: controller.show_frame(p)
            ).pack(fill="x", padx=10, pady=(10 if i == 0 else 5, 5))

        # Spacer pushes logout button to the bottom
        tk.Frame(self, bg="#2c3e50").pack(expand=True, fill="both")

        # Logout button
        tk.Button(
            self, text="Log Out", bg="#CA463A", fg="white",
            relief="flat", height=2,
            command=lambda: controller.show_frame("LoginPage")
        ).pack(fill="x", padx=10, pady=20)

class ShiftList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Left scrollable list
        left_container = tk.Frame(self, bg="white")
        left_container.grid(row=0, column=0, sticky="nswe", padx=20, pady=20)
        left_container.grid_rowconfigure(1, weight=1)
        left_container.grid_columnconfigure(0, weight=1)


        tk.Label(left_container, text="My Next Shifts",
                font=("Arial", 16, "bold")).pack(anchor="w")

        self.shift_frame = tk.Frame(left_container)
        self.shift_frame.pack(fill="both", expand=True)


        self.shift_canvas = tk.Canvas(self.shift_frame)
        shift_scrollbar = ttk.Scrollbar(self.shift_frame, orient="vertical", command=self.shift_canvas.yview)
        self.shift_list_frame = tk.Frame(self.shift_canvas)

        self.shift_list_frame.bind(
            "<Configure>",
            lambda e: self.shift_canvas.configure(scrollregion=self.shift_canvas.bbox("all"))
        )

        self.shift_canvas.create_window((0, 0), window=self.shift_list_frame, anchor="nw", tags="shift_window")
        self.shift_canvas.bind(
            "<Configure>",
            lambda e: self.shift_canvas.itemconfig("shift_window", width=e.width)
        )
        self.shift_canvas.configure(yscrollcommand=shift_scrollbar.set)

        self.shift_canvas.pack(side="left", fill="both", expand=True)
        shift_scrollbar.pack(side="right", fill="y")


    class ShiftBlock(tk.Frame):
        def __init__(self, parent, role, date, time_range, colour="#8ecae6"):
            super().__init__(parent, bg=colour, bd=1, relief="solid")

            tk.Label(self, text=role, bg=colour,
                     font=("Arial", 12, "bold")).pack(anchor="w", padx=6, pady=(6, 0))

            tk.Label(self, text=date, bg=colour,
                     font=("Arial", 10)).pack(anchor="w", padx=6)

            tk.Label(self, text=time_range, bg=colour,
                     font=("Arial", 10)).pack(anchor="w", padx=6, pady=(0, 6))

    # Public method to add shifts
    def add_shift(self, role, date, time_range, colour="#89ABCD"):
        block = self.ShiftBlock(self.shift_list_frame, role, date, time_range, colour)
        block.pack(fill="x", padx=10, pady=5)

# Calendar for Shifts
class MyShiftCalendar(tk.Frame):
    def __init__(self, parent, start_date, num_days=14):
        super().__init__(parent, bg="white")

        self.start_date = start_date
        self.num_days = num_days

        # Padding container for aesthetics to match padding of the shifts list
        padding_container = tk.Frame(self, bg="white")
        padding_container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(padding_container, text="Calendar",
                 font=("Arial", 16, "bold")).pack(anchor="w", pady=(0, 10))

        calendar_outer = tk.Frame(padding_container)
        calendar_outer.pack(fill="both", expand=True)

        # Left time column
        self.time_canvas = tk.Canvas(calendar_outer, width=80)
        self.time_canvas.grid(row=0, column=0, sticky="ns")

        self.time_frame = tk.Frame(self.time_canvas)
        self.time_canvas.create_window((0, 0), window=self.time_frame, anchor="nw")

        # Scrollable calendar section
        self.cal_canvas = tk.Canvas(calendar_outer)
        self.cal_canvas.grid(row=0, column=1, sticky="nsew")

        self.cal_y_scroll = ttk.Scrollbar(calendar_outer, orient="vertical")
        self.cal_y_scroll.grid(row=0, column=2, sticky="ns")

        self.cal_x_scroll = ttk.Scrollbar(calendar_outer, orient="horizontal", command=self.cal_canvas.xview)
        self.cal_x_scroll.grid(row=1, column=1, sticky="ew")

        self.calendar_frame = tk.Frame(self.cal_canvas)
        self.cal_canvas.create_window((0, 0), window=self.calendar_frame, anchor="nw")

        # Sync scrollbars
        def sync_scroll(*args): # https://www.w3schools.com/python/python_args_kwargs.asp
            self.cal_canvas.yview(*args)
            self.time_canvas.yview(*args)


        self.cal_canvas.configure(yscrollcommand=self.cal_y_scroll.set, xscrollcommand=self.cal_x_scroll.set)
        self.time_canvas.configure(yscrollcommand=self.cal_y_scroll.set)
        self.cal_y_scroll.configure(command=sync_scroll)


        def match_heights():
            cal_bbox = self.cal_canvas.bbox("all")
            time_bbox = self.time_canvas.bbox("all")

            if not cal_bbox or not time_bbox:
                return

            cal_h = cal_bbox[3]
            time_h = time_bbox[3]
            max_h = max(cal_h, time_h)

            self.cal_canvas.configure(scrollregion=(0, 0, cal_bbox[2], max_h))
            self.time_canvas.configure(scrollregion=(0, 0, time_bbox[2], max_h))


        self.calendar_frame.bind("<Configure>", lambda e: match_heights())
        self.time_frame.bind("<Configure>", lambda e: match_heights())

        calendar_outer.grid_columnconfigure(1, weight=1)
        calendar_outer.grid_rowconfigure(0, weight=1)

        # Calendar grid
        self.build_calendar_grid()

    def build_calendar_grid(self):
        dates = [
            (self.start_date + timedelta(days=i)).strftime("%a %d %b")
            for i in range(self.num_days)
        ]

        times = [f"{h:02d}:00" for h in range(24)]

        # Time column
        tk.Label(self.time_frame, text="", width=20, height=1).grid(row=0, column=0)

        for i, t in enumerate(times, start=1):
            tk.Label(self.time_frame, text=t, width=12, height=2).grid(row=i, column=0, sticky="w")

        # Date headers
        for col, d in enumerate(dates):
            tk.Label(self.calendar_frame, text=d, borderwidth=1, relief="flat",
                    height=2, width=12).grid(row=0, column=col)

        # Empty grid cells
        for row, t in enumerate(times, start=1):
            for col in range(len(dates)):
                tk.Label(self.calendar_frame, text="", borderwidth=1, relief="solid",
                        width=12, height=2).grid(row=row, column=col)

    # Add a shift to the calendar on the right
    def add_shift_to_calendar(self, column, start_hour, end_hour, colour, role, time_text):
        block = tk.Frame(self.calendar_frame, bg=colour, bd=1, relief="solid")

        # Role line
        tk.Label(
            block,
            text=role,
            bg=colour,
            font=("Arial", 10, "bold"),
            anchor="w",
            justify="left",
            wraplength=75
        ).pack(fill="x", padx=3, pady=(3, 0))

        # Time line
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



# Main App Class - main window, deals with switching pages
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title("Application")
        self.state("zoomed")
        self.minsize(800, 600)   # Prevent shrinking too small

        # Creates a container frame for each page and expands it for the whole window
        container = tk.Frame(self)
        container.pack(expand=True, fill="both")
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        # Creates frames/pages
        self.frames = {} # Dictionary to store all the screens/frames

        # Add all screens here
        for label, PageClass in sidebar_buttons:
            frame = PageClass(container, self)
            self.frames[PageClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

            frame.grid(row=0, column=0, sticky="nsew")

        # self.show_frame(LoginPage) # Default screen
        self.show_frame(Dashboard) # Default screen

    # Frames/page switching
    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()
        frame.focus_set()

        # Remove old Return bindings
        self.unbind_all("<Return>")

        # Only bind Return for LoginPage
        if page_class.__name__ == "LoginPage":
            self.bind_all("<Return>", lambda event: frame.login()) # pressing return triggers login process
            # lambda = command is not instant
            

# Run App
if __name__ == "__main__":
    app = App()
    app.mainloop() # keeps window running
