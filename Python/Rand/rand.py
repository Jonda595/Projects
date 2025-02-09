import random

number = 0
attempts = 0

while number != 150000:
    number = random.randrange(0,150001)
    print(number)
    attempts += 1
print(f"Attempts: {attempts}")
