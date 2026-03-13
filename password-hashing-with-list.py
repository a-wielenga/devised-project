import mysql.connector
from argon2 import PasswordHasher

# SQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CreativeComputingMySQLROOT!",
    database="Application"
)

cursor = conn.cursor()

# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor.html


# Password hasher using Argon2
ph = PasswordHasher()

# Dummy Data for Users Table
emails = [
    "team_member1@email.com",
    "team_leader1@email.com",
    "department_lead1@email.com",
    "manager1@email.com",
    "admin1@email.com"
]

passwords = [
    "password1",
    "password2",
    "password3",
    "password4",
    "password5"
]

# Dummy Data for Profiles Table
user_first_name = [
    "Cheese",
    "Burger",
    "Salad",
    "Tomato",
    "Lettuce"
]

user_last_name = [
    "Burger",
    "Tomato",
    "Salad",
    "Muppet",
    "Beyuh"
]

phone_number = [
    "01234567890",
    "07500345784",
    "07314592653",
    "07676767676",
    "07589793238"
]

address = [
    "12 Something Road, Someplace, Some-other-Place, Whereabout, AB1 2AB",
    "69 Roady Road, Somewhere, Place, Placeth, PL12 5DA",
    "67 Rocky Lane, Rocksville, Rock, Rocketh, RO53 7GS",
    "2 Streety Street, Streetsville, Streetish, Streetsham, ST67 7AB",
    "90 Lost-all-Hope Lane, Dunnow, Fedupshire, Inturnalskreaming, WT67 3FU"
]

date_of_birth = [
    '1963-07-12',
    '1973-09-18',
    '1998-10-05',
    '2004-11-25',
    '2000-05-08'
]


# SQL templates
sql_users_insert = """
INSERT INTO Users (
    user_id, email_address, password_hash
)
VALUES (%s, %s, %s) 
"""

sql_profiles_insert = """
INSERT INTO Profiles (
    profile_id,
    user_id,
    user_first_name,
    user_last_name,
    phone_number,
    address,
    date_of_birth
)
VALUES (%s, %s, %s, %s, %s, %s, %s) 
"""

# %s = placeholders
# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

# Insert users
for i, (email, password) in enumerate(zip(emails, passwords), start=1):
    user_id = f"U{i:03d}"  # f-string formats U001, U002 etc.
    hashed = ph.hash(password)

    user_values = (user_id, email, hashed)
    cursor.execute(sql_users_insert, user_values) # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

# Insert profiles
for j, (user_first_name, user_last_name, phone_number, address, date_of_birth) in enumerate(
    zip(user_first_name, user_last_name, phone_number, address, date_of_birth),
    start=1 # starts counter at 1 for IDs
):
    profile_id = f"P{j:03d}"
    user_id = f"U{j:03d}"

    profile_values = (profile_id, user_id, user_first_name, user_last_name, phone_number, address, date_of_birth)
    cursor.execute(sql_profiles_insert, profile_values)

# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

# Commit the data to the database
conn.commit() # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html

# Debugging message
print("Inserted all data!")
