import mysql.connector
import tkinter as tk
from tkinter import messagebox # https://docs.python.org/3/library/tkinter.messagebox.html
from argon2 import PasswordHasher

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
        for F in (LoginPage, Dashboard):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage") # Default screen

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
        super().__init__(parent)

        tk.Label(self, text="Dashboard", font=("Arial", 18)).pack(pady=20)

        tk.Button(self, text="Log Out",
                  command=lambda: controller.show_frame("LoginPage")).pack(pady=10)


# Run App
if __name__ == "__main__":
    app = App()
    app.mainloop() # keeps window running

