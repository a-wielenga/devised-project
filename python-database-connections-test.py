import mysql.connector

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

for row in rows:
    print("Email Address:", row[0])


