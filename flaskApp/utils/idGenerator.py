import random
import string

def idgen():
# Generate a random 10-digit number
    random_number = random.randint(10**9, (10**10)-1)

    return random_number

def codeGenerator():
    # Define the characters you want to include in the random string
    characters = string.ascii_letters + string.digits + '!@#$%^&*'

    # Specify the length of the random string
    string_length = 6  # You can change this to the desired length

    # Generate the random string
    random_string = ''.join(random.choice(characters) for _ in range(string_length))

    return random_string
