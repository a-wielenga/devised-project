import mysql.connector
import tkinter as tk
from tkinter import messagebox # https://docs.python.org/3/library/tkinter.messagebox.html
from argon2 import PasswordHasher

# SQL connectiom
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CreativeComputingMySQLROOT!",
    database="Application"
)

cursor = conn.cursor()

# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor.html


## Password hash using Argon2 - security for passwords and verificiation
ph = PasswordHasher()


# Login function
def login():
    email = email_entry.get()
    user_entered_password = password_entry.get()

    # Query user by email
    sql_select = "SELECT password_hash FROM Users WHERE email_address = %s"
    cursor.execute(sql_select, (email,))
    result = cursor.fetchone() # fetches the row where the emails match - https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchone.html

    if result is None:
        messagebox.showerror("Login Failed", "Email not found")
        return

    stored_hash_password = result[0] # gives first value in result which is the stored password hash

    try:
        # Verify Argon2 password
        if ph.verify(stored_hash_password, user_entered_password):
            messagebox.showinfo("Login Successful", "Welcome!")
        else:
            messagebox.showerror("Login Failed", "Incorrect password")
    except:
        messagebox.showerror("Login Failed", "Incorrect password")


# tkinter UI

# Main window
root = tk.Tk()
root.title("Login Page")
root.geometry("350x200")
root.minsize(350, 200)   # Prevent shrinking too small

# Centre Frame
container = tk.Frame(root)
container.pack(expand=True)   # This keeps it centred on resize, puts the container inside the window, lets it expand to fill extra space and centres it

# https://www.activestate.com/resources/quick-reads/how-to-use-pack-in-tkinter/
# https://www.geeksforgeeks.org/python/python-grid-method-in-tkinter/
# https://www.pythonguis.com/faq/pack-place-and-grid-in-tkinter/

# Username row
tk.Label(container, text="Email:").grid(row=0, column=0, padx=10, pady=5, sticky="e") # e = East (right) keeps it with the entry field
email_entry = tk.Entry(container)
email_entry.grid(row=0, column=1, padx=10, pady=5)

# Password row
tk.Label(container, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry = tk.Entry(container, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Login button
login_button = tk.Button(container, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop() # keeps window running

