from passlib.hash import bcrypt

# User enters their password
input_password = "lukessecretpassword"

# You get this from your database
stored_hash = "$2b$12$JmsGgD9/p0D2VjYXJu3m4eax1utshZwp371bkM4Bbygygo0/y2rF."

# Now compare:
if bcrypt.verify(input_password, stored_hash):
    print("Password is correct!")
else:
    print("Password is incorrect.")