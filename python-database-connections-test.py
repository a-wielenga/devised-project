import mysql.connector
import tkinter as tk

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CreativeComputingMySQLROOT!",
    database="Application"
)

cursor = conn.cursor()

# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor.html

sql_insert = """
INSERT INTO Users (
    user_id, email_address, password_hash
)
VALUES (%s, %s, %s) 
"""

values = (
    1,
    "example@email.com",
    "password123"
)

# %s = placeholders
# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

cursor.execute(sql_insert, values) # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
conn.commit() # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

print("Inserted user!")


sql_select = "SELECT email_address FROM Users;"
cursor.execute(sql_select)

rows = cursor.fetchall()

# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-fetchall.html

for row in rows:
    print("Email Address:", row[0])


# tkinter UI

root = tk.Tk() # creates a new window called root

label = tk.Label(root, text="Hello World", font=("Arial", 14))
label.pack(pady=20) # top AND bottom padding

# https://www.activestate.com/resources/quick-reads/how-to-use-pack-in-tkinter/

show_button = tk.Button(root, text="Press me", font=("Arial", 12))
show_button.pack(pady=10)

root.mainloop() # keeps window running

