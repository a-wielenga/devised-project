import mysql.connector
import tkinter as tk
from tkinter import messagebox # https://docs.python.org/3/library/tkinter.messagebox.html
from argon2 import PasswordHasher
from tkinter import ttk
from datetime import datetime, timedelta

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

        buttons = [
            "Dashboard", "My Shifts List", "Shift Calendar", "Available Shifts", "Rotas", "Timesheets"
        ]

        pages = {
            "Dashboard": "Dashboard",
            "My Shifts List": "MyShiftsListPage",
            "Shift Calendar": "MyShiftsCalendarPage"
        }

        # for i, b in enumerate(buttons):
        #     tk.Button(
        #         sidebar_frame, text=b, bg="#34495e", fg="white",
        #         relief="flat", height=2
        #     ).pack(fill="x", padx=10, pady=(10 if i == 0 else 5, 5))

        for i, b in enumerate(buttons):
            tk.Button(
                sidebar_frame,
                text=b,
                bg="#34495e",
                fg="white",
                relief="flat",
                height=2,
                command=lambda name=b: controller.show_frame(pages[name])
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
        self.shift_frame.pack(fill="both", expand=True, pady=10)


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
        for F in (LoginPage, Dashboard, MyShiftsListPage, MyShiftsCalendarPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        # self.show_frame("LoginPage") # Default screen
        self.show_frame("Dashboard") # Default screen

    # Frames/page switching
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise() # brings frame to front
        frame.focus_set()

        # Remove any old Return bindings
        self.unbind_all("<Return>") # pressing return triggers login process

        # Re-bind only if the new page is LoginPage
        if page_name == "LoginPage":
            self.bind_all("<Return>", lambda event: frame.login()) # pressing return triggers login process
            # lambda = command is not instant
            

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

        # Main container
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

        # Main container
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

# Run App
if __name__ == "__main__":
    app = App()
    app.mainloop() # keeps window running
