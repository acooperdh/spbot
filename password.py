import random

lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
uppercase_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers = "0123456789"
special_characters = "!@#$%^&*()_+-=[]{}|;':,./<>?"
all = lowercase_letters + uppercase_letters + numbers + special_characters
characters = int(
    input("enter the number of characters you want in your password:"))
password = random.sample(all, characters)

password = "".join(password)

print(password)
