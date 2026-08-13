import random
import string

def generate_password(length):
    """Generates a random password of the specified length."""
    # Combine letters (upper/lower), numbers, and punctuation symbols
    all_characters = string.ascii_letters + string.digits + string.punctuation
    
    password = ""
    
    # Loop 'length' amount of times to build the password
    for _ in range(length):
        random_char = random.choice(all_characters)
        password += random_char # Add the random character to our password string
        
    return password

# --- Main Program ---
print("Welcome to the Python Password Generator!")

try:
    # Ask the user how long they want the password to be
    user_length = int(input("Enter the desired password length (e.g., 12): "))
    
    # Basic check to make sure the password isn't too short
    if user_length < 4:
        print("For better security, please choose a length of 4 or more.")
    else:
        # Call our function and print the result
        secure_password = generate_password(user_length)
        print(f"\nSuccess! Your new password is: {secure_password}")
        
except ValueError:
    # This handles the error if the user types a word instead of a number
    print("Invalid input. Please enter a whole number.")