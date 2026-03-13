from argon2 import PasswordHasher

ph = PasswordHasher()


# hashes and stores the hashed password
hashedPassword = ph.hash("password123")
print(hashedPassword)


#password entry
print("Please enter your password: ")
userEnteredPassword = input()


# verify the password
try:
    ph.verify(hashedPassword, userEnteredPassword)
    print("Password is correct")
except:
    print("Invalid password")
